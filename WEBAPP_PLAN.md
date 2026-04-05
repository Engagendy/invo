# Web App Plan

## Goal

Ship a local-first invoice OCR app that any user can install on macOS, Windows, or Linux, open in a browser, select folders and options, and run extraction without a cloud dependency.

## Recommended Architecture

### 1. Backend

Use the current Python OCR engine as the core processing service.

- Wrap `process_folder(...)` in a local HTTP API.
- Use `FastAPI` for the service layer.
- Use `uvicorn` as the local server.
- Keep OCR, PDF rendering, file output, Excel export, and model management in Python.
- Store users, projects, project configs, and OCR document metadata in a database.
- Keep the database Postgres-ready, but default to a local embedded DB for standalone installs.

This avoids rewriting the OCR stack and keeps the existing CLI usable.

### 2. Frontend

Use a browser UI served locally by the backend.

- React + Vite for the frontend.
- Static build output embedded into the Python app.
- Open the default browser to `http://127.0.0.1:<port>` when the app starts.

### 3. Local App Behavior

The packaged app should:

1. Start the local Python backend.
2. Bind only to `127.0.0.1`.
3. Open the default browser automatically.
4. Let the user choose:
   - source folder
   - processed folder
   - project name
   - OCR backend
   - handwriting fallback
   - export mode
   - debug image export
   - naming pattern
5. Show job progress, logs, and output files.
6. Require user login and load project-specific settings.

## UI Scope

### First UI version

- Login and registration
- Project list per user
- Save/load project configuration
- Folder picker for source and output
- Project name field
- OCR mode selector:
  - `normal`
  - `ai`
- Handwriting fallback selector:
  - `none`
  - `trocr`
- Export selector:
  - original
  - enhanced
  - both
- Start button
- Live log panel
- Results table with output filename, extracted fields, and status
- Stored document list per project
- Original/enhanced PDF and image links

### Quality/debug view

- Show original page preview
- Show enhanced OCR image preview
- Show OCR text
- Show extracted fields

This is important for tuning difficult invoices.

## Packaging Strategy

### Cross-platform packaging

Use a local-server bundle instead of Electron first.

- Package Python backend as a desktop runtime with `PyInstaller` or `Nuitka`
- Bundle frontend static files into the Python package
- Bundle OCR models into a `models/` directory beside the executable
- Launch browser automatically

This gives a browser-based UX without shipping Chromium.

## Per-platform output

### Windows

- `InvoiceProcessor.exe`
- `models/`
- `web/`
- `source/`
- `processed/`

### macOS

- `InvoiceProcessor.app` or a signed folder app
- same sidecar folders for models and data

### Linux

- AppImage or tarball
- same sidecar folders for models and data

## Why not Electron first

- Larger downloads
- More packaging complexity
- No direct benefit yet because the app only needs a local browser shell

Electron or Tauri can be added later if a native desktop shell becomes necessary.

## Delivery Phases

### Phase 1

- Finish CLI accuracy work
- Stabilize `normal`, `ai`, and `trocr` setup flows
- Create sample-based regression checks

### Phase 2

- Add FastAPI wrapper around the current processor
- Add job queue and progress endpoint
- Add structured JSON results
- Add auth sessions
- Add projects and document persistence

### Phase 3

- Build React/Vite frontend
- Add preview/debug workflow
- Add settings persistence
- Add project dashboard and document history

### Phase 4

- Package per OS
- Bundle models
- Add first-run diagnostics
- Add installer docs

## Immediate Next Step

Build the local backend API first, not the final desktop bundle.

That keeps the OCR core and the future web UI aligned, while preserving the CLI for testing.
