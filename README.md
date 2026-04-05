# ULTRA FORCE

ULTRA FORCE is a local OCR system for scanned PDFs and source videos. It has:

1. A CLI pipeline in `invoice_processor.py`
2. A local browser app in `web_app.py`
3. Per-user projects, saved OCR settings, and stored document history in `web_db.py`

The system can:

1. Convert PDF pages to images
2. Sample source videos and OCR transaction-style frames
3. Detect one or many documents on a page
4. Run normal OCR or AI OCR
5. Use TrOCR as a handwritten fallback
6. Extract type, date, number, company, and amount
7. Save original and enhanced PDF outputs
8. Save original and enhanced PNG debug images
9. Store projects, runs, and document metadata for later review
10. Track source mode, source origin, and source timestamp per stored result

## Files

- `invoice_processor.py`: main processing script
- `requirements.txt`: Windows-oriented packaged AI dependencies
- `requirements-normal.txt`: cross-platform normal OCR dependencies
- `requirements-ai.txt`: AI extras including TrOCR dependencies
- `requirements-web.txt`: local browser UI backend dependencies
- `setup_ai_env.sh`: macOS/Linux Python 3.11 AI environment bootstrap
- `setup_ai_env.bat`: Windows Python 3.11 AI environment bootstrap
- `web_app.py`: local FastAPI server and job runner for the browser UI
- `web_db.py`: users, projects, sessions, and OCR document metadata storage
- `run_web_app.sh`: launch the local browser app on macOS/Linux
- `run_web_app.bat`: launch the local browser app on Windows
- `build_web_app.sh`: package the local web app for macOS/Linux
- `build_web_app.bat`: package the local web app for Windows
- `WEBAPP_PLAN.md`: local web app and packaging plan
- `app_paths.py`: runtime paths for bundled assets, models, and user data

## Python Setup

Install normal OCR dependencies:

```powershell
pip install -r requirements-normal.txt
pip install -r requirements-web.txt
```

Recommended Python version for PaddleOCR packaging on Windows:

```text
Python 3.10 or 3.11
```

The `normal` backend works on newer Python versions.
The `ai` backend still requires a compatible Python 3.10 or 3.11 setup.
ULTRA FORCE uses the TrOCR safetensors path and keeps a platform-aware Torch pin because `torch==2.6.0` is not published for some Intel macOS Python 3.11 environments.

## Storage

By default, ULTRA FORCE stores app data in the user profile:

- macOS: `~/Library/Application Support/ULTRA_FORCE`
- Linux: `~/.ultra_force`
- Windows: `%APPDATA%\ULTRA_FORCE`

That includes:

- `ultra_force.db`
- downloaded optional models under `models/`

If you want PostgreSQL instead of SQLite, set:

```bash
DATABASE_URL=postgresql+psycopg://user:password@host:5432/ultra_force
```

## OCR Runtime Notes

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

On macOS, the currently available PaddlePaddle build may differ. Use:

```bash
./setup_ai_env.sh
```

On Windows, use:

```powershell
setup_ai_env.bat
```

If you want GPU acceleration, use the matching PaddlePaddle GPU package for your CUDA version from the official Paddle installation guide.

### First Run Model Download

On the first run, PaddleOCR may download detection and recognition model files.

If you want a fully bundled app for sharing, run the app once on your machine, locate the downloaded PaddleOCR model directories, and package those model files with the app.
The build scripts also copy cached Paddle models into the packaged `models/official_models/` folder when available.

## Bundled App Layout

The packaging scripts create a distributable local app and place beside the executable:

```text
ULTRA_FORCE/
  ULTRA_FORCE(.exe)
  web/
  models/
  source/
  processed/
  debug_images/
```

Bundled PaddleOCR model files should live under `models/official_models/`.
Bundled TrOCR model files now live under `models/trocr/`.

## Source Modes

Projects can now run in:

- `pdf`: process a folder of PDFs
- `video`: process a single local source video and extract purchase-style rows with timestamps

For video mode, configure:

- `Video File`
- `Video Sample Every N Seconds`
- `Video Max Sampled Frames`

Video OCR stores:

- source type
- source origin
- source timestamp
- extracted row text

The first video milestone is designed for scrolling purchase or transaction history clips such as Tabby-, Amazon-, or WhatsApp-shared payment history videos.

## Release Builds

### macOS

Build a native macOS release:

```bash
bash build_release_mac.sh
```

Outputs:

- `dist/ULTRA_FORCE-macos-<version>.dmg`
- `dist/ULTRA_FORCE-macos-<version>-sha256.txt`

Install flow for customers:

1. Open the DMG
2. Drag `ULTRA_FORCE.app` to `Applications`
3. Launch `ULTRA FORCE`

### Windows

Build a Windows release on a Windows machine:

```powershell
build_release_windows.bat
```

Outputs:

- `dist\ULTRA_FORCE-windows-<version>.zip`
- `dist\ULTRA_FORCE-windows-<version>-setup.exe`
- `dist\ULTRA_FORCE-windows-<version>-sha256.txt`

Customer install flow:

1. Download `ULTRA_FORCE-windows-<version>-setup.exe`
2. Run the installer
3. Launch `ULTRA FORCE` from Start Menu or Desktop shortcut

## Release Size Notes

The main bundle-size drivers are:

- PyInstaller collection of large OCR and ML runtimes
- PaddleOCR model files
- bundled TrOCR model cache

This repo now reduces release size by default through:

- bundling only `microsoft/trocr-base-handwritten`
- not warming or copying `trocr-large-handwritten`
- copying only the selected Hugging Face model cache instead of the full cache
- narrowing the PyInstaller Transformer collection to the TrOCR path instead of `--collect-all transformers`

If you want to override the bundled handwritten model during build:

```bash
TROCR_MODEL_NAME=microsoft/trocr-base-handwritten bash build_release_mac.sh
```

```powershell
set TROCR_MODEL_NAME=microsoft/trocr-base-handwritten
build_release_windows.bat
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

Normal OCR with handwritten fallback:

```powershell
python invoice_processor.py --source source_single --processed processed_single --project-name MyProject --single-item-per-page --ocr-backend normal --handwriting-backend trocr
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

Export original and enhanced PNG debug images:

```powershell
python invoice_processor.py --source source_single --processed processed_single --project-name MyProject --single-item-per-page --ocr-backend normal --debug-image-dir debug_images
```

## Web App

The project now includes a local browser UI backed by FastAPI.

Features in the current web app:

- login and registration
- per-user projects
- saved project configuration
- default naming pattern auto-filled in the UI
- choose source folder
- choose output folder
- choose debug image folder
- configure project name
- choose OCR backend and OCR profile
- choose handwritten fallback and TrOCR model
- configure export mode
- configure output naming pattern
- keep document history per project
- view original and enhanced PDFs/images from stored metadata
- run jobs and watch logs/results live
- runtime diagnostics and first-run setup guidance

Launch on macOS/Linux:

```bash
./run_web_app.sh
```

Launch on Windows:

```powershell
run_web_app.bat
```

## Automated Releases

The repo now includes GitHub Actions automation in [.github/workflows/release.yml](/Users/engagendy/RiderProjects/invo/.github/workflows/release.yml).

It builds:

- macOS DMG: `dist/ULTRA_FORCE-macos-<version>.dmg`
- macOS checksum: `dist/ULTRA_FORCE-macos-<version>-sha256.txt`
- Windows zip: `dist/ULTRA_FORCE-windows-<version>.zip`
- Windows installer: `dist/ULTRA_FORCE-windows-<version>-setup.exe`
- Windows checksum: `dist/ULTRA_FORCE-windows-<version>-sha256.txt`

Triggers:

- manual run with `workflow_dispatch`
- automatic run when you push a tag like `v1.0.0`

On tagged builds, the workflow publishes the generated files as GitHub release assets automatically.

Local release commands:

```bash
bash build_release_mac.sh
```

Native Apple Silicon macOS build:

```bash
MAC_BUILD_ARCH=arm64 PYTHON_BIN=/opt/homebrew/bin/python3.11 bash build_release_mac.sh
```

If the machine is currently running under Rosetta and `/opt/homebrew/bin/python3.11` is not installed, a true native `arm64` build is not possible yet.

macOS install flow after build:

- open the DMG
- drag `ULTRA_FORCE.app` into `Applications`
- launch `ULTRA_FORCE.app`

```powershell
build_release_windows.bat
```

Version source:

- `RELEASE_VERSION` env var if set
- otherwise the pushed Git tag such as `v1.0.0`
- otherwise `dev` locally

Windows installer:

- local and CI Windows releases use [installer_windows.iss](/Users/engagendy/RiderProjects/invo/installer_windows.iss)
- GitHub Actions installs Inno Setup automatically before building the installer

Direct Python launch:

```powershell
python web_app.py
```

The server binds to:

```text
http://127.0.0.1:8765
```

Database:

```text
ultra_force.db
```

The database defaults to local SQLite for standalone installs.
If you want PostgreSQL, set:

```text
DATABASE_URL
```

Naming pattern tokens:

```text
{doc_type} {date} {number} {company_name} {amount} {amount_aed} {project_name}
```

## Packaging

Build the packaged browser app on macOS/Linux:

```bash
./build_web_app.sh
```

Build on Windows:

```powershell
build_web_app.bat
```

The build output bundles:

- local Python backend executable
- `web/` static UI assets
- `models/` sidecar folder
- `source/`
- `processed/`
- `debug_images/`

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
- `trocr` can be enabled as a handwritten fallback for missing fields.
- Field extraction uses heuristics and regex, so unusual invoice formats may still require tuning.
- The browser app is local-first and does not require a cloud service.
- The browser app now reports runtime readiness for normal OCR, AI OCR, TrOCR, and cached models on first load.
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
