# ULTRA FORCE

ULTRA FORCE is a local OCR, reconciliation, review, and construction-accounting workspace for Ultra Force. It ingests PDFs, videos, and multi-sheet bank statements, extracts structured transaction and document data, links supporting evidence, and pushes that data into company-level accounting and project-costing workflows.

The repo now includes:

1. OCR and ingestion pipeline in `invoice_processor.py`
2. Local FastAPI browser app in `web_app.py`
3. Persistent data models in `web_db.py`
4. Browser UI in `web/index.html` and `web/assets/app.js`

## What It Does

### OCR And Ingestion

- OCR PDFs with normal OCR, AI OCR, and TrOCR handwritten fallback
- Sample videos and extract transaction-like rows from frames
- Parse multi-sheet Excel bank statements
- Detect multiple receipt regions on a page
- Track source type, source origin, source file, and source timestamp
- Save processed outputs and debug assets

### Reconciliation And Review

- Reconcile bank transactions against PDF and video extracted documents
- Flag `matched`, `missing_receipt`, and `not_applicable` bank rows
- Show linked record detail with output preview
- Provide `Reconciliation`, `Review Queue`, `Exceptions`, `Feedback`, and `Evidence` workspaces
- Persist review notes, comments, assignments, and activity history

### Dashboards And Analytics

- Server-side bank analytics and drill-down
- Monthly debit, credit, coverage, unresolved aging, and exception views
- Filterable dashboard drill-down with server-side pagination
- Processed resources center with diagnostics, quality scoring, source activity, and rerun

### Company And Accounting

- Company directory and company settings
- Company-level chart of accounts
- Quarterly accounting periods and draft-quarter seeding
- Rule-based journal draft generation from parsed data
- Manual journals
- Posted journal entries, trial balance, and general ledger
- Supplier and customer masters
- AP/AR aging and settlement allocation
- Company auto-posting rules

### Construction Accounting

- Company projects with job code, client, site, contract, and budget fields
- Cost centers and cost codes
- Job costing summary by project
- Billing events for claims, milestones, variations, retention, debit notes, and credit notes
- Purchase orders, receipts, and procurement control
- Procurement exception queue with review state and assignment

## Main Workspaces

### Project-Level

- `Overview`
- `Reconciliation`
- `Review Queue`
- `Exceptions`
- `Feedback`
- `Vendors`
- `Rules`
- `Tags`
- `Stored Documents`
- `Previous Results`
- `Processed Resources`
- `Search`
- `Evidence`
- `Activity`
- `Close`

### Top-Level

- `Companies`
- `Accounting`

## Data Model Direction

The product now follows this accounting boundary:

- company owns accounting books
- project belongs to company
- project is used for job costing and operational attribution
- documents, journal lines, AP/AR, and procurement records can reference both company accounting structures and project dimensions

This means:

- chart of accounts is company-level
- accounting periods are company-level
- journals, trial balance, and ledger are company-level
- project code, cost center, and cost code are dimensions

## Python Setup

ULTRA FORCE currently works best with two local virtual environments:

- `.venv`: lightweight environment for web stack and normal OCR
- `.venv311`: Python `3.11` environment for AI OCR, PaddleOCR, and TrOCR

Recommended setup:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements-normal.txt
pip install -r requirements-web.txt
```

```bash
./setup_ai_env.sh
./.venv311/bin/pip install -r requirements-web.txt
```

Windows:

```powershell
py -3.11 -m venv .venv311
setup_ai_env.bat
.\.venv311\Scripts\pip install -r requirements-web.txt
```

### Recommended Runtime

If you want the browser app with full AI OCR and TrOCR support, run it from `.venv311`:

```bash
./.venv311/bin/python web_app.py
```

Windows:

```powershell
.\.venv311\Scripts\python web_app.py
```

## OCR Runtime Notes

This version uses:

- `PyMuPDF` to render PDF pages
- `PaddleOCR` for AI OCR
- `pytesseract` for faster normal OCR when available
- `RapidOCR` as fallback when Tesseract is missing
- `OpenCV` for document splitting

`ai` OCR and `trocr` require Python `3.10` or `3.11`.

### TrOCR Model Detection

The app treats a TrOCR model as installed if it exists in either:

- `models/trocr/`
- `models/huggingface/hub/`

That means previously downloaded Hugging Face cache entries such as `microsoft/trocr-large-handwritten` are treated as installed without requiring another download.

## Storage

By default, app data is stored in the user profile:

- macOS: `~/Library/Application Support/ULTRA_FORCE`
- Linux: `~/.ultra_force`
- Windows: `%APPDATA%\\ULTRA_FORCE`

That includes:

- `ultra_force.db`
- downloaded models under `models/`

If you want PostgreSQL instead of SQLite:

```bash
DATABASE_URL=postgresql+psycopg://user:password@host:5432/ultra_force
```

## Source Types

Projects can process:

- `pdf`
- `video`
- `sheet`

Bank workbooks support multiple sheets in the same Excel file. Each sheet is inspected independently and imported when a recognizable bank-statement header is found.

Video extraction stores:

- source type
- source origin
- source timestamp
- extracted row content

## Accounting And Procurement Notes

The current accounting system supports:

- company chart of accounts
- accounting periods with `open`, `closed`, and `locked`
- auto-posting rules
- journal drafts from parsed data
- manual journals
- posting and unposting
- trial balance
- general ledger
- AP/AR aging
- settlement allocation
- purchase orders
- goods/service receipts
- procurement control
- procurement exceptions

Current automation level:

- parsed records can generate journal drafts automatically through seeded and manual rules
- undated drafts are skipped during posting
- missing draft quarters can be seeded automatically
- account displays now use `code · name` format in the accounting UI

## Packaging

### macOS

```bash
bash build_release_mac.sh
```

Outputs:

- `dist/ULTRA_FORCE-macos-<version>.dmg`
- `dist/ULTRA_FORCE-macos-<version>-sha256.txt`

### Windows

```powershell
build_release_windows.bat
```

Outputs:

- `dist\\ULTRA_FORCE-windows-<version>.zip`
- `dist\\ULTRA_FORCE-windows-<version>-setup.exe`
- `dist\\ULTRA_FORCE-windows-<version>-sha256.txt`

## Roadmaps

- Product roadmap: `ROADMAP.md`
- Construction accounting roadmap: `CONSTRUCTION_ACCOUNTING_ROADMAP.md`

## Current Gaps

The app is now beyond OCR-only, but it is still evolving toward a fuller accounting system. The next major accounting layers are:

- VAT engine and tax codes
- financial statements
- stronger AP approval/payment workflow
- stronger AR invoicing/collection workflow
- close controls and accounting approvals
- deeper construction ledgers for retention, advances, and WIP rollforward
