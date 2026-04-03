import argparse
import os
import re
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, List, Optional, Sequence, Tuple

import cv2
import fitz
import numpy as np
from openpyxl import Workbook
import pytesseract


BoundingBox = Tuple[int, int, int, int]


@dataclass
class DocumentFields:
    doc_type: str = "Unknown"
    date: str = "Unknown"
    number: str = "Unknown"
    company_name: str = "Unknown"
    amount: str = "Unknown"


@dataclass
class ProcessedRecord:
    source_file: str
    output_file: str
    doc_type: str
    date: str
    number: str
    company_name: str
    amount: str
    currency: str
    project_name: str


def resolve_base_dir() -> Path:
    return Path(__file__).resolve().parent


def configure_model_cache() -> None:
    cache_home = resolve_base_dir() / "models"
    cache_home.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("PADDLE_PDX_CACHE_HOME", str(cache_home))


def detect_tesseract_cmd() -> Optional[str]:
    candidates = [
        shutil.which("tesseract"),
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return str(candidate)
    return None


def validate_runtime() -> None:
    if sys.version_info >= (3, 12):
        raise RuntimeError(
            "PaddleOCR packaging is not available in this project on Python "
            f"{sys.version_info.major}.{sys.version_info.minor}. "
            "Use Python 3.10 or 3.11."
        )


def render_pdf_to_images(pdf_path: Path, dpi: int = 300) -> List[np.ndarray]:
    zoom = dpi / 72.0
    matrix = fitz.Matrix(zoom, zoom)
    images: List[np.ndarray] = []

    with fitz.open(pdf_path) as pdf:
        for page in pdf:
            pix = page.get_pixmap(matrix=matrix, alpha=False)
            image = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
                pix.height, pix.width, pix.n
            )
            if pix.n == 4:
                image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
            else:
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            images.append(image)

    return images


def preprocess_for_detection(image: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(
        blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    return cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)


def merge_boxes(boxes: Sequence[BoundingBox], gap: int = 25) -> List[BoundingBox]:
    merged: List[BoundingBox] = []
    for box in sorted(boxes, key=lambda item: (item[1], item[0])):
        x, y, w, h = box
        expanded = (x - gap, y - gap, w + 2 * gap, h + 2 * gap)
        merged_this_round = False
        for index, current in enumerate(merged):
            cx, cy, cw, ch = current
            if not (
                expanded[0] > cx + cw
                or expanded[0] + expanded[2] < cx
                or expanded[1] > cy + ch
                or expanded[1] + expanded[3] < cy
            ):
                nx = min(x, cx)
                ny = min(y, cy)
                nw = max(x + w, cx + cw) - nx
                nh = max(y + h, cy + ch) - ny
                merged[index] = (nx, ny, nw, nh)
                merged_this_round = True
                break
        if not merged_this_round:
            merged.append(box)
    return merged


def detect_document_regions(
    image: np.ndarray, min_area_ratio: float = 0.08
) -> List[BoundingBox]:
    processed = preprocess_for_detection(image)
    contours, _ = cv2.findContours(
        processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    image_area = image.shape[0] * image.shape[1]
    min_area = int(image_area * min_area_ratio)
    candidates: List[BoundingBox] = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = w * h
        if area < min_area:
            continue
        if w < 150 or h < 150:
            continue
        candidates.append((x, y, w, h))

    merged = merge_boxes(candidates)
    if not merged:
        return [(0, 0, image.shape[1], image.shape[0])]
    return sorted(merged, key=lambda item: (item[1], item[0]))


def crop_with_padding(
    image: np.ndarray, box: BoundingBox, padding: int = 20
) -> np.ndarray:
    x, y, w, h = box
    height, width = image.shape[:2]
    x1 = max(0, x - padding)
    y1 = max(0, y - padding)
    x2 = min(width, x + w + padding)
    y2 = min(height, y + h + padding)
    return image[y1:y2, x1:x2]


def preprocess_for_ocr(image: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    normalized = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    contrast = clahe.apply(normalized)
    denoised = cv2.fastNlMeansDenoising(contrast, None, 18, 7, 21)
    sharpened = cv2.addWeighted(denoised, 1.4, cv2.GaussianBlur(denoised, (0, 0), 3), -0.4, 0)
    binary = cv2.adaptiveThreshold(
        sharpened,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        11,
    )
    return deskew_binary_image(binary)


def preprocess_for_tesseract(image: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    normalized = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    contrast = clahe.apply(normalized)
    denoised = cv2.fastNlMeansDenoising(contrast, None, 12, 7, 21)
    binary = cv2.adaptiveThreshold(
        denoised,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        9,
    )
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    cleaned = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    return deskew_binary_image(cleaned)


def preprocess_for_tesseract_strong(image: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    upscaled = cv2.resize(gray, None, fx=1.8, fy=1.8, interpolation=cv2.INTER_CUBIC)
    normalized = cv2.normalize(upscaled, None, 0, 255, cv2.NORM_MINMAX)
    clahe = cv2.createCLAHE(clipLimit=3.5, tileGridSize=(8, 8))
    contrast = clahe.apply(normalized)
    denoised = cv2.fastNlMeansDenoising(contrast, None, 18, 7, 21)
    blur = cv2.medianBlur(denoised, 3)
    binary = cv2.adaptiveThreshold(
        blur,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        41,
        7,
    )
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    return deskew_binary_image(cleaned)


def deskew_binary_image(binary: np.ndarray) -> np.ndarray:
    coords = np.column_stack(np.where(binary < 250))
    if coords.size == 0:
        return binary
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle += 90
    if -0.5 < angle < 0.5:
        return binary
    height, width = binary.shape[:2]
    matrix = cv2.getRotationMatrix2D((width // 2, height // 2), angle, 1.0)
    return cv2.warpAffine(
        binary,
        matrix,
        (width, height),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE,
    )


def normalize_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def contains_arabic(value: str) -> bool:
    return any("\u0600" <= char <= "\u06FF" for char in value)


def contains_latin(value: str) -> bool:
    return any(("A" <= char <= "Z") or ("a" <= char <= "z") for char in value)


def alpha_ratio(value: str) -> float:
    if not value:
        return 0.0
    alnum = sum(char.isalnum() for char in value)
    alpha = sum(char.isalpha() for char in value)
    if alnum == 0:
        return 0.0
    return alpha / alnum


def sanitize_filename_part(value: str) -> str:
    value = normalize_whitespace(value)
    value = re.sub(r"[\\/:*?\"<>|]+", "", value)
    value = re.sub(r"\s+", "", value)
    return value or "Unknown"


def normalize_number_candidate(value: str) -> str:
    value = normalize_whitespace(value).strip(" -:/._")
    value = re.sub(r"[^A-Za-z0-9\-\/]", "", value)
    prefix_match = re.match(r"^([A-Za-z]{2,}[-\/]?)(.*)$", value)
    prefix = ""
    suffix = value
    if prefix_match and any(char.isdigit() for char in prefix_match.group(2)):
        prefix = prefix_match.group(1)
        suffix = prefix_match.group(2)
    substitutions = str.maketrans(
        {
            "O": "0",
            "o": "0",
            "I": "1",
            "l": "1",
            "S": "5",
            "B": "8",
            "Z": "2",
        }
    )
    suffix = suffix.translate(substitutions)
    value = prefix + suffix
    return value or "Unknown"


def choose_number_by_type(text: str, doc_type: str) -> str:
    lines = [normalize_whitespace(line) for line in text.splitlines() if normalize_whitespace(line)]

    invoice_patterns = [
        r"(?i)\binvoice\s*(?:no|#|number)?\s*[:;\-]?\s*([A-Z0-9OISBZl\-\/]{4,})",
        r"(?i)\btax\s+invoice\b.*?(?:no|#|number)?\s*[:;\-]?\s*([A-Z0-9OISBZl\-\/]{4,})",
    ]
    receipt_patterns = [
        r"(?i)\breceipt\s*(?:no|#|number)?\s*[:;\-]?\s*([A-Z0-9OISBZl\-\/]{4,})",
    ]
    generic_patterns = [
        r"(?i)\b(?:bill|voucher|document|inv|trx|ref|serial)\s*(?:no|#|number)?\s*[:;\-]?\s*([A-Z0-9OISBZl\-\/]{3,})",
        r"(?i)\b(?:no|number)\b\s*[:;\-]?\s*([A-Z0-9OISBZl\-\/]{3,})",
    ]

    def collect(patterns: Sequence[str]) -> List[str]:
        values: List[str] = []
        for line in lines:
            for pattern in patterns:
                for match in re.finditer(pattern, line):
                    value = normalize_number_candidate(match.group(1))
                    if any(char.isdigit() for char in value):
                        values.append(value)
        return values

    invoice_values = collect(invoice_patterns)
    receipt_values = collect(receipt_patterns)
    generic_values = collect(generic_patterns)

    if doc_type == "Invoice" and invoice_values:
        return max(invoice_values, key=lambda item: (sum(char.isdigit() for char in item), len(item)))
    if doc_type == "Receipt" and receipt_values:
        return max(receipt_values, key=lambda item: (sum(char.isdigit() for char in item), len(item)))
    if invoice_values:
        return max(invoice_values, key=lambda item: (sum(char.isdigit() for char in item), len(item)))
    if receipt_values:
        return max(receipt_values, key=lambda item: (sum(char.isdigit() for char in item), len(item)))

    for index, line in enumerate(lines):
        if re.search(r"(?i)\b(?:invoice|receipt|bill|voucher|document|inv|trx|ref)\b", line):
            for offset in range(0, 3):
                if index + offset >= len(lines):
                    continue
                candidates = re.findall(r"[A-Z0-9OISBZl][A-Z0-9OISBZl\-\/]{2,}", lines[index + offset])
                for candidate in candidates:
                    value = normalize_number_candidate(candidate)
                    if any(char.isdigit() for char in value):
                        return value

    if generic_values:
        return max(generic_values, key=lambda item: (sum(char.isdigit() for char in item), len(item)))
    return "Unknown"


def make_ocr_engine(
    language: str = "en",
    use_angle_cls: bool = True,
    text_recognition_model_name: Optional[str] = None,
) -> Any:
    try:
        from paddleocr import PaddleOCR
    except ImportError as exc:
        raise RuntimeError(
            "PaddleOCR is not installed. Run 'pip install paddleocr paddlepaddle'."
        ) from exc
    os.environ.setdefault("DISABLE_MODEL_SOURCE_CHECK", "True")
    os.environ.setdefault("PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK", "True")
    kwargs = {
        "use_textline_orientation": use_angle_cls,
    }
    if text_recognition_model_name:
        kwargs["text_recognition_model_name"] = text_recognition_model_name
    else:
        kwargs["lang"] = language
    return PaddleOCR(**kwargs)


def make_ocr_engines(
    language: str = "en",
    use_angle_cls: bool = True,
    ocr_profile: str = "mixed",
) -> List[Any]:
    if ocr_profile == "printed":
        return [make_ocr_engine(language=language, use_angle_cls=use_angle_cls)]
    if ocr_profile == "handwriting":
        return [
            make_ocr_engine(
                language=language,
                use_angle_cls=use_angle_cls,
                text_recognition_model_name="PP-OCRv5_server_rec",
            )
        ]
    return [
        make_ocr_engine(language=language, use_angle_cls=use_angle_cls),
        make_ocr_engine(
            language=language,
            use_angle_cls=use_angle_cls,
            text_recognition_model_name="PP-OCRv5_server_rec",
        ),
    ]


def extract_text_with_tesseract(image: np.ndarray) -> Tuple[str, np.ndarray]:
    variants = [
        cv2.cvtColor(image, cv2.COLOR_BGR2RGB),
        cv2.cvtColor(preprocess_for_tesseract(image), cv2.COLOR_GRAY2RGB),
        cv2.cvtColor(preprocess_for_tesseract_strong(image), cv2.COLOR_GRAY2RGB),
    ]
    best_text = ""
    best_variant = variants[0]
    best_score = -1
    config = "--oem 3 --psm 6"
    for variant in variants:
        text = pytesseract.image_to_string(variant, config=config)
        lines = [normalize_whitespace(line) for line in text.splitlines() if normalize_whitespace(line)]
        score = score_text(lines)
        if score > best_score:
            best_text = "\n".join(lines)
            best_variant = variant
            best_score = score
    return best_text, best_variant


def extract_text_with_rapidocr(image: np.ndarray) -> Tuple[str, np.ndarray]:
    try:
        from rapidocr_onnxruntime import RapidOCR
    except ImportError as exc:
        raise RuntimeError(
            "RapidOCR is not installed. Run 'pip install rapidocr-onnxruntime'."
        ) from exc
    variants = [
        image,
        cv2.cvtColor(preprocess_for_tesseract(image), cv2.COLOR_GRAY2BGR),
        cv2.cvtColor(preprocess_for_tesseract_strong(image), cv2.COLOR_GRAY2BGR),
    ]
    engine = RapidOCR()
    best_text = ""
    best_variant = variants[0]
    best_score = -1
    for variant in variants:
        result, _ = engine(variant)
        lines: List[str] = []
        if result:
            for item in result:
                if len(item) >= 2:
                    cleaned = normalize_whitespace(str(item[1]))
                    if cleaned:
                        lines.append(cleaned)
        score = score_text(lines)
        if score > best_score:
            best_text = "\n".join(lines)
            best_variant = variant
            best_score = score
    return best_text, best_variant


def flatten_paddle_result(result: object) -> List[str]:
    texts: List[str] = []
    if result is None:
        return texts
    if isinstance(result, str):
        cleaned = normalize_whitespace(result)
        if cleaned:
            texts.append(cleaned)
        return texts
    if isinstance(result, (list, tuple)):
        if len(result) == 2 and isinstance(result[0], str):
            cleaned = normalize_whitespace(result[0])
            if cleaned:
                texts.append(cleaned)
            return texts
        for item in result:
            texts.extend(flatten_paddle_result(item))
    return texts


def result_to_lines(result: Any) -> List[str]:
    lines: List[str] = []
    for item in result:
        if hasattr(item, "get"):
            rec_texts = item.get("rec_texts", [])
            for text in rec_texts:
                cleaned = normalize_whitespace(str(text))
                if cleaned:
                    lines.append(cleaned)
        else:
            lines.extend(flatten_paddle_result(item))
    return lines


def score_text(lines: Sequence[str]) -> int:
    text = "\n".join(lines)
    digit_bonus = sum(char.isdigit() for char in text) * 2
    alpha_bonus = sum(char.isalpha() for char in text)
    return len(text) + digit_bonus + alpha_bonus


def extract_text(image: np.ndarray, ocr_engines: Sequence[Any]) -> Tuple[str, np.ndarray]:
    variants = [
        cv2.cvtColor(image, cv2.COLOR_BGR2RGB),
        cv2.cvtColor(preprocess_for_ocr(image), cv2.COLOR_GRAY2RGB),
        cv2.cvtColor(preprocess_for_tesseract_strong(image), cv2.COLOR_GRAY2RGB),
    ]
    best_lines: List[str] = []
    best_variant = variants[0]
    best_score = -1

    for ocr_engine in ocr_engines:
        for variant in variants:
            result = ocr_engine.predict(variant)
            lines = result_to_lines(result)
            score = score_text(lines)
            if score > best_score:
                best_lines = lines
                best_variant = variant
                best_score = score

    return "\n".join(best_lines), best_variant


def extract_text_by_backend(
    image: np.ndarray, ocr_backend: str, ocr_engines: Sequence[Any]
) -> Tuple[str, np.ndarray]:
    if ocr_backend == "normal":
        tesseract_cmd = detect_tesseract_cmd()
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
            try:
                return extract_text_with_tesseract(image)
            except Exception:
                pass
        return extract_text_with_rapidocr(image)
    return extract_text(image, ocr_engines)


def infer_doc_type(text: str) -> str:
    lowered = text.lower()
    if "invoice" in lowered or "tax invoice" in lowered:
        return "Invoice"
    if "receipt" in lowered or "cash sale" in lowered:
        return "Receipt"
    if "document" in lowered:
        return "Document"
    return "Document"


def parse_date(text: str) -> str:
    patterns = [
        r"\b(\d{4}[/-]\d{1,2}[/-]\d{1,2})\b",
        r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b",
        r"\b(\d{1,2}\s+[A-Za-z]{3,9}\s+\d{2,4})\b",
        r"\b([A-Za-z]{3,9}\s+\d{1,2},\s*\d{4})\b",
    ]
    formats = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%m-%d-%Y",
        "%m/%d/%Y",
        "%d-%m-%y",
        "%d/%m/%y",
        "%d %b %Y",
        "%d %B %Y",
        "%d %b %y",
        "%d %B %y",
        "%b %d, %Y",
        "%B %d, %Y",
    ]

    for pattern in patterns:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            raw = normalize_whitespace(match.group(1).replace(".", "/"))
            for fmt in formats:
                try:
                    parsed = datetime.strptime(raw, fmt)
                    return parsed.strftime("%Y-%m-%d")
                except ValueError:
                    continue
    return "Unknown"


def parse_number(text: str) -> str:
    doc_type = infer_doc_type(text)
    return choose_number_by_type(text, doc_type)


def parse_amount(text: str) -> str:
    lines = [normalize_whitespace(line) for line in text.splitlines() if normalize_whitespace(line)]

    def line_values(line: str) -> List[str]:
        found: List[str] = []
        for token in re.findall(r"\d[\d,]*(?:\.\d+)+|\d[\d,]*", line):
            cleaned = token.replace(",", "")
            if cleaned.count(".") <= 1:
                if re.fullmatch(r"\d+\.\d{1,2}", cleaned):
                    found.append(cleaned)
                continue
            parts = cleaned.split(".")
            for index in range(len(parts) - 1):
                left = parts[index]
                right = parts[index + 1]
                if not left or not right:
                    continue
                if 1 <= len(right) <= 2:
                    found.append(f"{left}.{right}")
                    if len(left) > 3:
                        found.append(f"{left[-3:]}.{right}")
                        found.append(f"{left[-2:]}.{right}")
        return found

    scores: dict[str, int] = {}
    counts: dict[str, int] = {}

    for line in lines:
        values = line_values(line)
        lowered = line.lower()
        line_bonus = 0
        if re.search(r"(?i)\bgrand\s+total\b|\btotal\s+amount\b|\btotal\s+aed\b|\btotal\b|\bamount\s+due\b", line):
            line_bonus += 100
        if re.search(r"(?i)\bpayment\b|\bpaid\b|\bmembership\b", line):
            line_bonus += 60
        if re.search(r"(?i)\bsubtotal\b|\bsub\s*total\b", line):
            line_bonus += 30
        if re.search(r"(?i)\bvat\b|\btax\b", line):
            line_bonus -= 15
        if re.search(r"(?i)\bqty\b|\bprice\b", line):
            line_bonus -= 10

        for value in values:
            try:
                amount = float(value)
            except ValueError:
                continue
            if amount <= 0:
                continue
            normalized = f"{amount:.2f}"
            counts[normalized] = counts.get(normalized, 0) + 1
            scores[normalized] = scores.get(normalized, 0) + line_bonus

    if scores:
        ranked = []
        for value, score in scores.items():
            amount = float(value)
            frequency_bonus = (counts.get(value, 1) - 1) * 60
            ranked.append((score + frequency_bonus, counts.get(value, 1), amount, value))
        ranked.sort(key=lambda item: (item[0], item[1], item[2]), reverse=True)
        return ranked[0][3]
    return "Unknown"


def parse_company_name(text: str) -> str:
    blacklist = {
        "invoice",
        "tax invoice",
        "receipt",
        "document",
        "bill to",
        "ship to",
        "customer copy",
        "original",
        "duplicate",
    }
    preferred_terms = {
        "distribution",
        "trading",
        "company",
        "co",
        "corp",
        "corporation",
        "llc",
        "l.l.c",
        "limited",
        "ltd",
        "services",
        "station",
        "building",
        "materials",
        "transport",
        "industries",
        "group",
        "market",
        "store",
        "shop",
        "adnoc",
    }
    candidates: List[Tuple[int, str]] = []

    for line in text.splitlines():
        cleaned = normalize_whitespace(line)
        if len(cleaned) < 3 or len(cleaned) > 60:
            continue
        lowered = cleaned.lower()
        if lowered in blacklist:
            continue
        if re.search(r"\b(?:invoice|receipt|total|date|no\.?|number)\b", lowered):
            continue
        if re.search(r"\d{3,}", cleaned):
            continue
        if sum(char.isalpha() for char in cleaned) < 4:
            continue
        score = 0
        words = re.findall(r"[A-Za-z]+", cleaned.lower())
        score += min(len(words), 6) * 3
        if contains_latin(cleaned) and not contains_arabic(cleaned):
            score += 25
        if contains_latin(cleaned):
            score += 10
        if alpha_ratio(cleaned) > 0.75:
            score += 8
        score += sum(12 for word in words if word in preferred_terms)
        if len(cleaned) >= 8:
            score += 5
        if len(words) == 1 and len(words[0]) <= 5:
            score -= 20
        if "_" in cleaned:
            score -= 15
        if re.search(r"(?i)^[a-z]{2,4}_[a-z]{2,6}$", cleaned):
            score -= 25
        if re.search(r"(?i)^[a-z]{2,8}$", cleaned) and cleaned.lower() not in preferred_terms:
            score -= 18
        candidates.append((score, cleaned))

    if candidates:
        candidates.sort(key=lambda item: item[0], reverse=True)
        return candidates[0][1]
    return "Unknown"


def extract_fields(text: str) -> DocumentFields:
    return DocumentFields(
        doc_type=infer_doc_type(text),
        date=parse_date(text),
        number=parse_number(text),
        company_name=parse_company_name(text),
        amount=parse_amount(text),
    )


def build_output_name(fields: DocumentFields, project_name: str) -> str:
    amount_part = fields.amount
    if amount_part != "Unknown":
        amount_part = f"{amount_part}AED"
    parts = [
        sanitize_filename_part(fields.doc_type),
        sanitize_filename_part(fields.date),
        sanitize_filename_part(fields.number),
        sanitize_filename_part(fields.company_name),
        sanitize_filename_part(amount_part),
        sanitize_filename_part(project_name),
    ]
    return "_".join(parts) + ".pdf"


def write_excel_summary(records: Sequence[ProcessedRecord], output_path: Path) -> None:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Documents"
    headers = [
        "SourceFile",
        "OutputFile",
        "Type",
        "Date",
        "Number",
        "CompanyName",
        "Amount",
        "Currency",
        "ProjectName",
    ]
    sheet.append(headers)
    for record in records:
        sheet.append(
            [
                record.source_file,
                record.output_file,
                record.doc_type,
                record.date,
                record.number,
                record.company_name,
                record.amount,
                record.currency,
                record.project_name,
            ]
        )
    workbook.save(output_path)


def image_to_pdf(image: np.ndarray, output_path: Path) -> None:
    height, width = image.shape[:2]
    success, encoded = cv2.imencode(".png", image)
    if not success:
        raise RuntimeError("Failed to encode image for PDF output.")
    pdf = fitz.open()
    page = pdf.new_page(width=width, height=height)
    page.insert_image(page.rect, stream=encoded.tobytes())
    pdf.save(output_path)
    pdf.close()


def ensure_bgr(image: np.ndarray) -> np.ndarray:
    if len(image.shape) == 2:
        return cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    return image


def iter_pdf_files(source_dir: Path) -> Iterable[Path]:
    yield from sorted(path for path in source_dir.glob("*.pdf") if path.is_file())


def process_pdf(
    pdf_path: Path,
    output_dir: Path,
    project_name: str,
    ocr_engines: Sequence[Any],
    ocr_backend: str,
    dpi: int = 300,
    save_text: bool = False,
    single_item_per_page: bool = False,
    export_image_mode: str = "original",
) -> Tuple[List[Path], List[ProcessedRecord]]:
    output_paths: List[Path] = []
    records: List[ProcessedRecord] = []
    pages = render_pdf_to_images(pdf_path, dpi=dpi)

    for page_index, page_image in enumerate(pages, start=1):
        if single_item_per_page:
            boxes = [(0, 0, page_image.shape[1], page_image.shape[0])]
        else:
            boxes = detect_document_regions(page_image)

        for item_index, box in enumerate(boxes, start=1):
            cropped = crop_with_padding(page_image, box)
            text, enhanced_image = extract_text_by_backend(cropped, ocr_backend, ocr_engines)
            fields = extract_fields(text)

            filename = build_output_name(fields, project_name)
            output_path = output_dir / filename

            duplicate_counter = 1
            while output_path.exists():
                output_path = output_dir / (
                    filename[:-4]
                    + f"_p{page_index}_i{item_index}_{duplicate_counter}.pdf"
                )
                duplicate_counter += 1

            exports: List[Tuple[np.ndarray, Path]] = []
            if export_image_mode in {"original", "both"}:
                exports.append((cropped, output_path))
            if export_image_mode in {"enhanced", "both"}:
                enhanced_output = output_path
                if export_image_mode == "both":
                    enhanced_output = output_dir / (output_path.stem + "_enhanced.pdf")
                exports.append((ensure_bgr(enhanced_image), enhanced_output))

            for export_image, export_path in exports:
                image_to_pdf(export_image, export_path)
                output_paths.append(export_path)
                records.append(
                    ProcessedRecord(
                        source_file=pdf_path.name,
                        output_file=export_path.name,
                        doc_type=fields.doc_type,
                        date=fields.date,
                        number=fields.number,
                        company_name=fields.company_name,
                        amount=fields.amount,
                        currency="AED" if fields.amount != "Unknown" else "Unknown",
                        project_name=project_name,
                    )
                )
            if save_text:
                text_path = output_path.with_suffix(".txt")
                text_path.write_text(text, encoding="utf-8")

    return output_paths, records


def process_folder(
    source_dir: Path,
    output_dir: Path,
    project_name: str,
    dpi: int = 300,
    language: str = "en",
    use_angle_cls: bool = True,
    save_text: bool = False,
    ocr_profile: str = "mixed",
    single_item_per_page: bool = False,
    ocr_backend: str = "ai",
    export_image_mode: str = "original",
) -> Tuple[List[Path], List[ProcessedRecord]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    ocr_engines: Sequence[Any] = []
    if ocr_backend == "ai":
        ocr_engines = make_ocr_engines(
            language=language,
            use_angle_cls=use_angle_cls,
            ocr_profile=ocr_profile,
        )
    generated_files: List[Path] = []
    records: List[ProcessedRecord] = []

    for pdf_path in iter_pdf_files(source_dir):
        try:
            pdf_outputs, pdf_records = process_pdf(
                pdf_path=pdf_path,
                output_dir=output_dir,
                project_name=project_name,
                ocr_engines=ocr_engines,
                ocr_backend=ocr_backend,
                    dpi=dpi,
                    save_text=save_text,
                    single_item_per_page=single_item_per_page,
                    export_image_mode=export_image_mode,
                )
            generated_files.extend(pdf_outputs)
            records.extend(pdf_records)
            print(f"Processed: {pdf_path.name}")
        except Exception as exc:
            print(f"Failed: {pdf_path.name} -> {exc}")
    return generated_files, records


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Split scanned invoice PDFs, OCR each item, extract fields, and save renamed PDFs."
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=Path("source"),
        help="Folder containing source PDF files.",
    )
    parser.add_argument(
        "--processed",
        type=Path,
        default=Path("processed"),
        help="Folder where processed PDF files will be written.",
    )
    parser.add_argument(
        "--project-name",
        required=True,
        help="Project name appended to every output filename.",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="Render DPI used when converting PDF pages to images.",
    )
    parser.add_argument(
        "--lang",
        default="en",
        help="PaddleOCR language code, for example en or ar.",
    )
    parser.add_argument(
        "--disable-angle-cls",
        action="store_true",
        help="Disable PaddleOCR angle classification.",
    )
    parser.add_argument(
        "--save-text",
        action="store_true",
        help="Write OCR text to a .txt file beside each generated PDF.",
    )
    parser.add_argument(
        "--ocr-profile",
        choices=["printed", "handwriting", "mixed"],
        default="mixed",
        help="OCR strategy: printed, handwriting, or mixed ensemble.",
    )
    parser.add_argument(
        "--ocr-backend",
        choices=["normal", "ai"],
        default="ai",
        help="Use normal OCR for faster processing or ai OCR for stronger extraction.",
    )
    parser.add_argument(
        "--tesseract-cmd",
        default="",
        help="Optional absolute path to tesseract.exe when using --ocr-backend normal.",
    )
    parser.add_argument(
        "--excel-name",
        default="document_summary.xlsx",
        help="Excel filename written into the processed folder.",
    )
    parser.add_argument(
        "--single-item-per-page",
        action="store_true",
        help="Skip document splitting and treat each PDF page as one document.",
    )
    parser.add_argument(
        "--export-image-mode",
        choices=["original", "enhanced", "both"],
        default="original",
        help="Export original pages, enhanced OCR images, or both.",
    )
    return parser


def main() -> None:
    validate_runtime()
    configure_model_cache()
    parser = build_parser()
    args = parser.parse_args()

    if args.ocr_backend == "normal" and args.tesseract_cmd:
        pytesseract.pytesseract.tesseract_cmd = args.tesseract_cmd

    source_dir = args.source
    output_dir = args.processed

    if not source_dir.exists():
        raise FileNotFoundError(f"Source folder does not exist: {source_dir}")

    generated_files, records = process_folder(
        source_dir=source_dir,
        output_dir=output_dir,
        project_name=args.project_name,
        dpi=args.dpi,
        language=args.lang,
        use_angle_cls=not args.disable_angle_cls,
        save_text=args.save_text,
        ocr_profile=args.ocr_profile,
        single_item_per_page=args.single_item_per_page,
        ocr_backend=args.ocr_backend,
        export_image_mode=args.export_image_mode,
    )
    write_excel_summary(records, output_dir / args.excel_name)
    print(f"Generated {len(generated_files)} file(s) in {output_dir}")


if __name__ == "__main__":
    main()
