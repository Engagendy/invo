import argparse
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, List, Optional, Sequence, Tuple

import cv2
import fitz
import numpy as np


BoundingBox = Tuple[int, int, int, int]


@dataclass
class DocumentFields:
    doc_type: str = "Unknown"
    date: str = "Unknown"
    number: str = "Unknown"
    company_name: str = "Unknown"
    amount: str = "Unknown"


def resolve_base_dir() -> Path:
    return Path(__file__).resolve().parent


def configure_model_cache() -> None:
    cache_home = resolve_base_dir() / "models"
    cache_home.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("PADDLE_PDX_CACHE_HOME", str(cache_home))


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
    denoised = cv2.fastNlMeansDenoising(gray, None, 20, 7, 21)
    return cv2.adaptiveThreshold(
        denoised,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        15,
    )


def normalize_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def sanitize_filename_part(value: str) -> str:
    value = normalize_whitespace(value)
    value = re.sub(r"[\\/:*?\"<>|]+", "", value)
    value = re.sub(r"\s+", "", value)
    return value or "Unknown"


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


def extract_text(image: np.ndarray, ocr_engines: Sequence[Any]) -> str:
    variants = [
        cv2.cvtColor(image, cv2.COLOR_BGR2RGB),
        cv2.cvtColor(preprocess_for_ocr(image), cv2.COLOR_GRAY2RGB),
    ]
    best_lines: List[str] = []
    best_score = -1

    for ocr_engine in ocr_engines:
        for variant in variants:
            result = ocr_engine.predict(variant)
            lines = result_to_lines(result)
            score = score_text(lines)
            if score > best_score:
                best_lines = lines
                best_score = score

    return "\n".join(best_lines)


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
    patterns = [
        r"(?i)\b(?:invoice|receipt|bill|voucher|document)\s*(?:no|#|number)?[:\s\-]*([A-Z0-9\-\/]+)",
        r"(?i)\b(?:inv|trx|ref)\s*(?:no|#|number)?[:\s\-]*([A-Z0-9\-\/]+)",
        r"(?i)\b(?:no|number)[:\s\-]*([A-Z0-9\-\/]{4,})",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            value = match.group(1).strip(" -:/")
            if any(char.isdigit() for char in value):
                return value
    return "Unknown"


def parse_amount(text: str) -> str:
    patterns = [
        r"(?i)\bAED\s*([0-9][0-9,]*\.?[0-9]{0,2})",
        r"(?i)\bTotal(?:\s+Amount)?[:\s\-]*([0-9][0-9,]*\.?[0-9]{0,2})",
        r"(?i)\bGrand\s+Total[:\s\-]*([0-9][0-9,]*\.?[0-9]{0,2})",
    ]
    values: List[float] = []
    for pattern in patterns:
        for match in re.finditer(pattern, text):
            candidate = match.group(1).replace(",", "").strip()
            try:
                values.append(float(candidate))
            except ValueError:
                continue
    if values:
        return f"{max(values):.2f}"
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
        return cleaned
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
    parts = [
        sanitize_filename_part(fields.doc_type),
        sanitize_filename_part(fields.date),
        sanitize_filename_part(fields.number),
        sanitize_filename_part(fields.company_name),
        sanitize_filename_part(fields.amount),
        sanitize_filename_part(project_name),
    ]
    return "_".join(parts) + ".pdf"


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


def iter_pdf_files(source_dir: Path) -> Iterable[Path]:
    yield from sorted(path for path in source_dir.glob("*.pdf") if path.is_file())


def process_pdf(
    pdf_path: Path,
    output_dir: Path,
    project_name: str,
    ocr_engines: Sequence[Any],
    dpi: int = 300,
    save_text: bool = False,
    single_item_per_page: bool = False,
) -> List[Path]:
    output_paths: List[Path] = []
    pages = render_pdf_to_images(pdf_path, dpi=dpi)

    for page_index, page_image in enumerate(pages, start=1):
        if single_item_per_page:
            boxes = [(0, 0, page_image.shape[1], page_image.shape[0])]
        else:
            boxes = detect_document_regions(page_image)

        for item_index, box in enumerate(boxes, start=1):
            cropped = crop_with_padding(page_image, box)
            text = extract_text(cropped, ocr_engines)
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

            image_to_pdf(cropped, output_path)
            output_paths.append(output_path)
            if save_text:
                text_path = output_path.with_suffix(".txt")
                text_path.write_text(text, encoding="utf-8")

    return output_paths


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
) -> List[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    ocr_engines = make_ocr_engines(
        language=language,
        use_angle_cls=use_angle_cls,
        ocr_profile=ocr_profile,
    )
    generated_files: List[Path] = []

    for pdf_path in iter_pdf_files(source_dir):
        try:
            generated_files.extend(
                process_pdf(
                    pdf_path=pdf_path,
                    output_dir=output_dir,
                    project_name=project_name,
                    ocr_engines=ocr_engines,
                    dpi=dpi,
                    save_text=save_text,
                    single_item_per_page=single_item_per_page,
                )
            )
            print(f"Processed: {pdf_path.name}")
        except Exception as exc:
            print(f"Failed: {pdf_path.name} -> {exc}")
    return generated_files


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
        "--single-item-per-page",
        action="store_true",
        help="Skip document splitting and treat each PDF page as one document.",
    )
    return parser


def main() -> None:
    validate_runtime()
    configure_model_cache()
    parser = build_parser()
    args = parser.parse_args()

    source_dir = args.source
    output_dir = args.processed

    if not source_dir.exists():
        raise FileNotFoundError(f"Source folder does not exist: {source_dir}")

    generated_files = process_folder(
        source_dir=source_dir,
        output_dir=output_dir,
        project_name=args.project_name,
        dpi=args.dpi,
        language=args.lang,
        use_angle_cls=not args.disable_angle_cls,
        save_text=args.save_text,
        ocr_profile=args.ocr_profile,
        single_item_per_page=args.single_item_per_page,
    )
    print(f"Generated {len(generated_files)} file(s) in {output_dir}")


if __name__ == "__main__":
    main()
