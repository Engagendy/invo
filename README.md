# Invoice PDF Processor

This script processes scanned PDFs containing invoices, receipts, or other documents.

It will:

1. Convert each PDF page to an image.
2. Detect multiple document regions on a single scanned page.
3. Crop each detected item.
4. Run OCR with PaddleOCR.
5. Extract key fields from the text.
6. Save each item as a separate PDF in the required filename format.

## Files

- `invoice_processor.py`: main processing script
- `requirements.txt`: Python dependencies

## Python Setup

Install Python dependencies:

```powershell
pip install -r requirements.txt
```

Recommended Python version for PaddleOCR packaging on Windows:

```text
Python 3.10 or 3.11
```

The current script will stop with a clear error on Python 3.12+ because Paddle runtime availability is inconsistent there.

## PaddleOCR Runtime Notes

This version uses:

- `PyMuPDF` to render PDF pages
- `PaddleOCR` for AI OCR
- `pytesseract` for a faster normal OCR mode
- `RapidOCR` as a bundled fallback when Tesseract is missing
- `OpenCV` for splitting multiple receipts on a page

There is no dependency on Tesseract or Poppler anymore.
The `ai` backend does not depend on Tesseract or Poppler.
The `normal` backend uses Tesseract if available and falls back to RapidOCR if Tesseract is missing.

### PaddlePaddle

`PaddleOCR` also requires `paddlepaddle`.

Install CPU runtime:

```powershell
pip install paddlepaddle==3.2.0 paddleocr==3.3.3
```

If you want GPU acceleration, use the matching PaddlePaddle GPU package for your CUDA version from the official Paddle installation guide.

### First Run Model Download

On the first run, PaddleOCR may download detection and recognition model files.

If you want a fully bundled app for sharing, run the app once on your machine, locate the downloaded PaddleOCR model directories, and package those model files with the app.

## Bundled App Direction

For a shareable Windows app, the recommended structure is:

```text
invoice_processor.py
models/
source/
processed/
```

Or, after packaging:

```text
InvoiceProcessor/
  InvoiceProcessor.exe
  models/
  source/
  processed/
```

This is more portable than relying on separate Tesseract or Poppler installations.

The script uses a local model cache folder at:

```text
models/
```

Bundled PaddleOCR model files should live under:

```text
models/official_models/
```

## Folder Layout

Create these folders under the working directory:

```text
source/
processed/
```

Put source PDFs into `source/`.

## Usage

Basic run:

```powershell
python invoice_processor.py --source source --processed processed --project-name MyProject --ocr-backend ai
```

Recommended Windows setup with Python 3.11:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python invoice_processor.py --source source --processed processed --project-name MyProject
```

With Arabic or another PaddleOCR language code:

```powershell
python invoice_processor.py --source source --processed processed --project-name MyProject --lang ar
```

Faster OCR mode with Tesseract:

```powershell
python invoice_processor.py --source source --processed processed --project-name MyProject --ocr-backend normal --tesseract-cmd "C:\Program Files\Tesseract-OCR\tesseract.exe"
```

Faster OCR mode with automatic fallback:

```powershell
python invoice_processor.py --source source --processed processed --project-name MyProject --ocr-backend normal
```

Single-item rename mode for one document per page:

```powershell
python invoice_processor.py --source source_single --processed processed_single --project-name MyProject --single-item-per-page --ocr-backend normal
```

Export cleaned OCR images as PDFs:

```powershell
python invoice_processor.py --source source_single --processed processed_single --project-name MyProject --single-item-per-page --ocr-backend normal --export-image-mode enhanced
```

Export both original and enhanced PDFs:

```powershell
python invoice_processor.py --source source_single --processed processed_single --project-name MyProject --single-item-per-page --ocr-backend normal --export-image-mode both
```

With custom DPI:

```powershell
python invoice_processor.py --source source --processed processed --project-name MyProject --dpi 300
```

## Output Filename Format

Each extracted item is saved as:

```text
[Type]_[Date]_[Number]_[CompanyName]_[AmountAED]_[ProjectName].pdf
```

If a field cannot be extracted, the script uses `Unknown`.

Example:

```text
Invoice_2026-04-03_INV-1023_ACMETrading_125.00AED_MyProject.pdf
```

## Notes

- Document splitting is contour-based using OpenCV.
- OCR is handled by PaddleOCR, which is generally stronger than Tesseract on varied document layouts.
- `normal` mode now tries multiple preprocessing variants for noisy photos before OCR.
- Field extraction uses heuristics and regex, so unusual invoice formats may still require tuning.
- If two files resolve to the same output name, the script appends page and item suffixes.
- The first execution may take longer because OCR models may be downloaded and initialized.

## Main Functions

- `detect_document_regions(...)`: finds separate receipts/invoices on a scanned page
- `extract_text(...)`: OCR step using PaddleOCR
- `extract_fields(...)`: parses type, date, number, company, and amount
- `process_folder(...)`: iterates through the `source` folder and writes to `processed`

## Packaging

For a distributable Windows app, use:

```powershell
build_app.bat
```

This expects Python 3.11 to be available through `py -3.11`.

The build script will:

- create a dedicated build virtual environment
- install runtime dependencies
- install pinned OCR dependencies and `pyinstaller`
- build a one-folder app into `dist\InvoiceProcessor`
- create `source` and `processed` folders in the output
- copy cached PaddleOCR models into `dist\InvoiceProcessor\models\official_models`
