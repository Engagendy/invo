import csv
import platform
import shutil
import subprocess
import sys
import threading
import uuid
import webbrowser
import zipfile
from datetime import datetime
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app_paths import bundled_web_dir, runtime_root, user_data_root
import invoice_processor as processor
from web_db import (
    AuthSession,
    DocumentRecord,
    Project,
    User,
    create_session_token,
    db_session,
    get_user_by_token,
    hash_password,
    init_db,
    verify_password,
)


BASE_DIR = runtime_root()
STATIC_DIR = bundled_web_dir()

OCR_BACKENDS = ["normal", "ai"]
HANDWRITING_BACKENDS = ["none", "trocr"]
OCR_PROFILES = ["printed", "handwriting", "mixed"]
EXPORT_IMAGE_MODES = ["original", "enhanced", "both"]
TROCR_MODELS = [
    "microsoft/trocr-base-handwritten",
    "microsoft/trocr-large-handwritten",
]


class AppSettings(BaseModel):
    source_dir: str = ""
    output_dir: str = ""
    debug_image_dir: str = ""
    archive_source_dir: str = ""
    project_name: str = "MyProject"
    ocr_backend: str = "normal"
    handwriting_backend: str = "none"
    trocr_model: str = TROCR_MODELS[0]
    ocr_profile: str = "mixed"
    export_image_mode: str = "original"
    naming_pattern: str = processor.DEFAULT_NAMING_PATTERN
    lang: str = "en"
    dpi: int = 300
    single_item_per_page: bool = True
    save_text: bool = True
    use_angle_cls: bool = True
    move_processed_source: bool = False
    video_sample_seconds: int = 2
    video_max_frames: int = 120
    excel_name: str = "document_summary.xlsx"


class ProcessRequest(AppSettings):
    project_id: Optional[int] = None


class AuthRequest(BaseModel):
    username: str
    password: str


class ProjectRequest(AppSettings):
    name: str
    description: str = ""


class DocumentUpdateRequest(BaseModel):
    doc_type: str
    date: str
    number: str
    company_name: str
    amount: str
    currency: str


@dataclass
class JobState:
    job_id: str
    user_id: int
    project_id: Optional[int] = None
    status: str = "queued"
    logs: List[str] = field(default_factory=list)
    generated_files: List[str] = field(default_factory=list)
    records: List[Dict[str, Any]] = field(default_factory=list)
    output_dir: str = ""
    excel_path: str = ""
    error: str = ""
    cancel_requested: bool = False


JOBS: Dict[str, JobState] = {}
JOBS_LOCK = threading.Lock()
MODEL_DOWNLOADS: Dict[str, Dict[str, str]] = {}
MODEL_LOCK = threading.Lock()


def append_job_log(job: JobState, message: str) -> None:
    with JOBS_LOCK:
        job.logs.append(message)


def job_should_cancel(job: JobState) -> bool:
    with JOBS_LOCK:
        return job.cancel_requested


def append_job_results(job: JobState, output_paths: List[Path], records: List[processor.ProcessedRecord]) -> None:
    with JOBS_LOCK:
        job.generated_files.extend(str(path) for path in output_paths)
        job.records.extend(asdict(record) for record in records)


def trocr_model_catalog() -> List[Dict[str, str]]:
    return [
        {
            "name": "microsoft/trocr-base-handwritten",
            "label": "Base Handwritten",
            "tier": "default",
            "size_hint": "smaller",
            "description": "Bundled default handwritten OCR model for balanced size and accuracy.",
        },
        {
            "name": "microsoft/trocr-large-handwritten",
            "label": "High Accuracy Handwritten",
            "tier": "optional",
            "size_hint": "larger",
            "description": "Optional larger handwritten OCR model with higher accuracy on difficult samples.",
        },
    ]


def get_model_status(model_name: str) -> Dict[str, str]:
    installed = processor.trocr_model_dir(model_name).exists() or processor.bundled_trocr_model_dir(model_name).exists()
    with MODEL_LOCK:
        download = MODEL_DOWNLOADS.get(model_name, {}).copy()
    status = download.get("status", "installed" if installed else "not_installed")
    message = download.get("message", "")
    return {
        "name": model_name,
        "installed": "true" if installed else "false",
        "status": status,
        "message": message,
        "removable": "true" if processor.trocr_model_dir(model_name).exists() else "false",
    }


def model_payload() -> Dict[str, Any]:
    items = []
    for item in trocr_model_catalog():
        status = get_model_status(item["name"])
        items.append({**item, **status})
    return {"models": items}


def download_model_worker(model_name: str) -> None:
    try:
        with MODEL_LOCK:
            MODEL_DOWNLOADS[model_name] = {"status": "downloading", "message": "Downloading model files."}
        processor.configure_model_cache()
        from transformers import TrOCRProcessor, VisionEncoderDecoderModel

        target_dir = processor.trocr_model_dir(model_name)
        target_dir.parent.mkdir(parents=True, exist_ok=True)
        trocr_processor = TrOCRProcessor.from_pretrained(model_name)
        trocr_model = VisionEncoderDecoderModel.from_pretrained(model_name, use_safetensors=True)
        trocr_processor.save_pretrained(target_dir)
        trocr_model.save_pretrained(target_dir, safe_serialization=True)
        with MODEL_LOCK:
            MODEL_DOWNLOADS[model_name] = {"status": "installed", "message": "Model installed."}
    except Exception as exc:
        with MODEL_LOCK:
            MODEL_DOWNLOADS[model_name] = {"status": "error", "message": str(exc)}


def require_user(x_auth_token: str = Header(default="")) -> User:
    if not x_auth_token:
        raise HTTPException(status_code=401, detail="Missing auth token")
    with db_session() as session:
        user = get_user_by_token(session, x_auth_token)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid auth token")
        session.expunge(user)
        return user


def unique_target_path(target: Path) -> Path:
    if not target.exists():
        return target
    stem = target.stem
    suffix = target.suffix
    parent = target.parent
    counter = 2
    while True:
        candidate = parent / f"{stem}_{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def project_to_payload(project: Project) -> Dict[str, Any]:
    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "settings": {
            "source_dir": project.source_dir,
            "output_dir": project.output_dir,
            "debug_image_dir": project.debug_image_dir,
            "archive_source_dir": project.archive_source_dir,
            "project_name": project.project_name,
            "ocr_backend": project.ocr_backend,
            "handwriting_backend": project.handwriting_backend,
            "trocr_model": project.trocr_model,
            "ocr_profile": project.ocr_profile,
            "export_image_mode": project.export_image_mode,
            "naming_pattern": project.naming_pattern,
            "lang": project.lang,
            "dpi": project.dpi,
            "single_item_per_page": project.single_item_per_page,
            "save_text": project.save_text,
            "use_angle_cls": project.use_angle_cls,
            "move_processed_source": project.move_processed_source,
            "video_sample_seconds": getattr(project, "video_sample_seconds", 2),
            "video_max_frames": getattr(project, "video_max_frames", 120),
            "excel_name": project.excel_name,
        },
    }


def build_runtime_payload() -> Dict[str, Any]:
    report = processor.get_runtime_report()
    messages = []
    if not report["normal_backend_ready"]:
        messages.append("Install requirements-normal.txt for the base OCR runtime.")
    if not report["ai_backend_ready"]:
        if not report["ai_backend_supported_python"]:
            messages.append("AI OCR needs Python 3.10 or 3.11 in a separate environment.")
        if report["missing_ai_dependencies"]:
            messages.append(
                "Missing AI dependencies: " + ", ".join(report["missing_ai_dependencies"]) + "."
            )
        if report["missing_ai_models"]:
            messages.append(
                "AI models not cached yet: " + ", ".join(report["missing_ai_models"]) + "."
            )
    if not report["trocr_ready"]:
        messages.append(
            "Missing TrOCR dependencies: "
            + ", ".join(report["missing_trocr_dependencies"])
            + "."
        )
    report["messages"] = messages
    report["first_run_ready"] = report["normal_backend_ready"]
    report["app_root"] = str(BASE_DIR)
    report["data_root"] = str(user_data_root())
    report["trocr_models"] = model_payload()["models"]
    return report


def choose_folder_native(prompt: str) -> str:
    system = platform.system()
    if system == "Darwin":
        result = subprocess.run(
            [
                "osascript",
                "-e",
                f'POSIX path of (choose folder with prompt "{prompt}")',
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    if system == "Windows":
        script = (
            "Add-Type -AssemblyName System.Windows.Forms; "
            "$dialog = New-Object System.Windows.Forms.FolderBrowserDialog; "
            f'$dialog.Description = "{prompt}"; '
            "if ($dialog.ShowDialog() -eq 'OK') { $dialog.SelectedPath }"
        )
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", script],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    for tool in ("zenity", "kdialog"):
        if shutil_which(tool):
            if tool == "zenity":
                result = subprocess.run(
                    ["zenity", "--file-selection", "--directory", "--title", prompt],
                    check=True,
                    capture_output=True,
                    text=True,
                )
                return result.stdout.strip()
            result = subprocess.run(
                ["kdialog", "--getexistingdirectory", str(BASE_DIR), "--title", prompt],
                check=True,
                capture_output=True,
                text=True,
            )
            return result.stdout.strip()
    raise RuntimeError("No native folder picker is available on this system.")


def choose_file_native(prompt: str, extensions: Optional[List[str]] = None) -> str:
    system = platform.system()
    extensions = extensions or []
    if system == "Darwin":
        type_clause = ""
        if extensions:
            joined = ", ".join(f'"{ext}"' for ext in extensions)
            type_clause = f" of type {{{joined}}}"
        result = subprocess.run(
            [
                "osascript",
                "-e",
                f'POSIX path of (choose file with prompt "{prompt}"{type_clause})',
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    if system == "Windows":
        filter_text = "All files (*.*)|*.*"
        if extensions:
            wildcard = ";".join(f"*.{ext}" for ext in extensions)
            filter_text = f"Supported files ({wildcard})|{wildcard}|All files (*.*)|*.*"
        script = (
            "Add-Type -AssemblyName System.Windows.Forms; "
            "$dialog = New-Object System.Windows.Forms.OpenFileDialog; "
            f'$dialog.Title = "{prompt}"; '
            f'$dialog.Filter = "{filter_text}"; '
            "if ($dialog.ShowDialog() -eq 'OK') { $dialog.FileName }"
        )
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", script],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    for tool in ("zenity", "kdialog"):
        if shutil_which(tool):
            if tool == "zenity":
                result = subprocess.run(
                    ["zenity", "--file-selection", "--title", prompt],
                    check=True,
                    capture_output=True,
                    text=True,
                )
                return result.stdout.strip()
            result = subprocess.run(
                ["kdialog", "--getopenfilename", str(BASE_DIR), "--title", prompt],
                check=True,
                capture_output=True,
                text=True,
            )
            return result.stdout.strip()
    raise RuntimeError("No native file picker is available on this system.")


def shutil_which(name: str) -> Optional[str]:
    from shutil import which

    return which(name)


def run_job(job: JobState, request: ProcessRequest) -> None:
    generated_files: List[Path] = []
    records: List[processor.ProcessedRecord] = []
    processed_source_paths: List[Path] = []
    duplicate_hashes: set[str] = set()
    try:
        with JOBS_LOCK:
            job.status = "running"
            job.output_dir = request.output_dir

        processor.validate_runtime(request.ocr_backend)
        processor.validate_runtime_requirements(
            request.ocr_backend,
            handwriting_backend=request.handwriting_backend,
        )
        processor.configure_model_cache()

        output_dir = Path(request.output_dir).expanduser().resolve()
        debug_dir = (
            Path(request.debug_image_dir).expanduser().resolve()
            if request.debug_image_dir
            else None
        )

        with db_session() as session:
            if job.project_id:
                duplicate_hashes = {
                    row[0]
                    for row in session.query(DocumentRecord.source_hash)
                    .filter(DocumentRecord.project_id == job.project_id, DocumentRecord.source_hash != "")
                    .all()
                }

        source_dir = Path(request.source_dir).expanduser().resolve()
        if not source_dir.exists():
            raise FileNotFoundError(f"Source folder does not exist: {source_dir}")
        generated_files, records = processor.process_folder(
            source_dir=source_dir,
            output_dir=output_dir,
            project_name=request.project_name,
            dpi=request.dpi,
            language=request.lang,
            use_angle_cls=request.use_angle_cls,
            save_text=request.save_text,
            ocr_profile=request.ocr_profile,
            single_item_per_page=request.single_item_per_page,
            ocr_backend=request.ocr_backend,
            export_image_mode=request.export_image_mode,
            debug_image_dir=debug_dir,
            handwriting_backend=request.handwriting_backend,
            trocr_model=request.trocr_model,
            video_sample_seconds=request.video_sample_seconds,
            video_max_frames=request.video_max_frames,
            naming_pattern=request.naming_pattern,
            log_message=lambda message: append_job_log(job, message),
            item_complete=lambda _path, output_paths, completed_records: append_job_results(
                job, output_paths, completed_records
            ),
            should_cancel=lambda: job_should_cancel(job),
            should_skip=lambda file_path: processor.compute_file_sha256(file_path) in duplicate_hashes,
        )
        processed_source_paths = sorted(
            {
                Path(record.source_path).expanduser().resolve()
                for record in records
                if record.source_path and record.source_type == "pdf"
            }
        )
        if job_should_cancel(job):
            with JOBS_LOCK:
                job.status = "cancelled"
            return

        excel_path = output_dir / request.excel_name
        processor.write_excel_summary(records, excel_path)

        with db_session() as session:
            project = None
            if job.project_id:
                project = (
                    session.query(Project)
                    .filter(Project.id == job.project_id, Project.user_id == job.user_id)
                    .first()
                )
            if project:
                project.source_dir = request.source_dir
                project.output_dir = request.output_dir
                project.debug_image_dir = request.debug_image_dir
                project.archive_source_dir = request.archive_source_dir
                project.project_name = request.project_name
                project.ocr_backend = request.ocr_backend
                project.handwriting_backend = request.handwriting_backend
                project.trocr_model = request.trocr_model
                project.ocr_profile = request.ocr_profile
                project.export_image_mode = request.export_image_mode
                project.naming_pattern = request.naming_pattern
                project.lang = request.lang
                project.dpi = request.dpi
                project.single_item_per_page = request.single_item_per_page
                project.save_text = request.save_text
                project.use_angle_cls = request.use_angle_cls
                project.move_processed_source = request.move_processed_source
                project.video_sample_seconds = request.video_sample_seconds
                project.video_max_frames = request.video_max_frames
                project.excel_name = request.excel_name

                existing_records = (
                    session.query(DocumentRecord)
                    .filter(DocumentRecord.project_id == project.id)
                    .all()
                )
                existing_by_key = {
                    (
                        record.source_file,
                        getattr(record, "source_type", "pdf"),
                        getattr(record, "source_origin", "pdf_upload"),
                        getattr(record, "source_timestamp", ""),
                        record.doc_type,
                        record.date,
                        record.number,
                        record.company_name,
                        record.amount,
                    ): record
                    for record in existing_records
                }
                debug_base_dir = debug_dir if debug_dir is not None else None

                for record, output_file in zip(records, generated_files):
                    record_key = (
                        record.source_file,
                        record.source_type,
                        record.source_origin,
                        record.source_timestamp,
                        record.doc_type,
                        record.date,
                        record.number,
                        record.company_name,
                        record.amount,
                    )
                    db_record = existing_by_key.get(record_key)
                    if not db_record:
                        db_record = DocumentRecord(
                            user_id=job.user_id,
                            project_id=project.id,
                        )
                        session.add(db_record)
                        existing_by_key[record_key] = db_record
                    db_record.source_file = record.source_file
                    db_record.source_path = record.source_path
                    db_record.source_hash = record.source_hash
                    db_record.source_type = record.source_type
                    db_record.source_origin = record.source_origin
                    db_record.source_timestamp = record.source_timestamp
                    db_record.doc_type = record.doc_type
                    db_record.date = record.date
                    db_record.number = record.number
                    db_record.company_name = record.company_name
                    db_record.amount = record.amount
                    db_record.currency = record.currency
                    db_record.confidence_score = record.confidence_score
                    db_record.confidence_label = record.confidence_label
                    db_record.raw_text = record.raw_text
                    if output_file.stem.endswith("_enhanced"):
                        db_record.enhanced_output_path = str(output_file)
                    else:
                        db_record.output_file = record.output_file
                        db_record.output_path = str(output_file)
                    if debug_base_dir is not None:
                        stem = Path(record.source_file).stem
                        db_record.original_debug_image = str(debug_base_dir / f"{stem}_p1_i1_original.png")
                        db_record.enhanced_debug_image = str(debug_base_dir / f"{stem}_p1_i1_enhanced.png")

        if request.move_processed_source and processed_source_paths:
            archive_dir = (
                Path(request.archive_source_dir).expanduser().resolve()
                if request.archive_source_dir
                else output_dir / "_processed_source"
            )
            archive_dir.mkdir(parents=True, exist_ok=True)
            for source_path in processed_source_paths:
                if not source_path.exists() or not source_path.is_file():
                    continue
                target_path = unique_target_path(archive_dir / source_path.name)
                source_path.rename(target_path)
                append_job_log(job, f"Archived source: {source_path.name} -> {target_path}")

        with JOBS_LOCK:
            job.status = "completed"
            job.generated_files = [str(path) for path in generated_files]
            job.records = [asdict(record) for record in records]
            job.excel_path = str(excel_path)
    except Exception as exc:
        with JOBS_LOCK:
            job.status = "cancelled" if job.cancel_requested else "failed"
            job.error = str(exc)
            job.logs.append(f"Error: {exc}")


init_db()

app = FastAPI(title="ULTRA FORCE")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/auth/register")
def register(payload: AuthRequest) -> Dict[str, Any]:
    with db_session() as session:
        existing = session.query(User).filter(User.username == payload.username.strip()).first()
        if existing:
            raise HTTPException(status_code=400, detail="Username already exists")
        user = User(
            username=payload.username.strip(),
            password_hash=hash_password(payload.password),
        )
        session.add(user)
        session.flush()
        token = create_session_token()
        session.add(AuthSession(token=token, user_id=user.id))
        return {"token": token, "user": {"id": user.id, "username": user.username}}


@app.post("/api/auth/login")
def login(payload: AuthRequest) -> Dict[str, Any]:
    with db_session() as session:
        user = session.query(User).filter(User.username == payload.username.strip()).first()
        if not user or not verify_password(payload.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid username or password")
        token = create_session_token()
        session.add(AuthSession(token=token, user_id=user.id))
        return {"token": token, "user": {"id": user.id, "username": user.username}}


@app.post("/api/auth/logout")
def logout(x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    with db_session() as session:
        auth_session = session.query(AuthSession).filter(AuthSession.token == x_auth_token).first()
        if auth_session:
            session.delete(auth_session)
    return {"ok": True}


@app.get("/api/me")
def me(x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    return {"id": user.id, "username": user.username}


@app.get("/api/settings")
def get_settings() -> Dict[str, Any]:
    return {
        "settings": AppSettings().model_dump(),
        "runtime": build_runtime_payload(),
        "models": model_payload(),
        "options": {
            "ocr_backends": OCR_BACKENDS,
            "handwriting_backends": HANDWRITING_BACKENDS,
            "ocr_profiles": OCR_PROFILES,
            "export_image_modes": EXPORT_IMAGE_MODES,
            "trocr_models": TROCR_MODELS,
            "naming_tokens": [
                "doc_type",
                "date",
                "number",
                "company_name",
                "amount",
                "amount_aed",
                "project_name",
            ],
        },
    }


@app.get("/api/models")
def list_models() -> Dict[str, Any]:
    return model_payload()


@app.post("/api/models/download")
def download_model(payload: Dict[str, str], x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    require_user(x_auth_token)
    model_name = payload.get("name", "").strip()
    if model_name not in TROCR_MODELS:
        raise HTTPException(status_code=400, detail="Unsupported model")
    status = get_model_status(model_name)
    if status["status"] == "downloading":
        return {"ok": True, "status": "downloading"}
    thread = threading.Thread(target=download_model_worker, args=(model_name,), daemon=True)
    thread.start()
    return {"ok": True, "status": "downloading"}


@app.delete("/api/models/{model_name:path}")
def delete_model(model_name: str, x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    require_user(x_auth_token)
    if model_name not in TROCR_MODELS:
        raise HTTPException(status_code=400, detail="Unsupported model")
    target_dir = processor.trocr_model_dir(model_name)
    if not target_dir.exists():
        return {"ok": True, "deleted": False}
    shutil.rmtree(target_dir, ignore_errors=True)
    with MODEL_LOCK:
        MODEL_DOWNLOADS.pop(model_name, None)
    return {"ok": True, "deleted": True}


@app.get("/api/projects")
def list_projects(x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        projects = (
            session.query(Project)
            .filter(Project.user_id == user.id)
            .order_by(Project.updated_at.desc())
            .all()
        )
        return {"projects": [project_to_payload(project) for project in projects]}


@app.post("/api/projects")
def create_project(project_request: ProjectRequest, x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        project = Project(
            user_id=user.id,
            name=project_request.name.strip(),
            description=project_request.description.strip(),
            source_dir=project_request.source_dir,
            output_dir=project_request.output_dir,
            debug_image_dir=project_request.debug_image_dir,
            archive_source_dir=project_request.archive_source_dir,
            project_name=project_request.project_name,
            ocr_backend=project_request.ocr_backend,
            handwriting_backend=project_request.handwriting_backend,
            trocr_model=project_request.trocr_model,
            ocr_profile=project_request.ocr_profile,
            export_image_mode=project_request.export_image_mode,
            naming_pattern=project_request.naming_pattern,
            lang=project_request.lang,
            dpi=project_request.dpi,
            single_item_per_page=project_request.single_item_per_page,
            save_text=project_request.save_text,
            use_angle_cls=project_request.use_angle_cls,
            move_processed_source=project_request.move_processed_source,
            video_sample_seconds=project_request.video_sample_seconds,
            video_max_frames=project_request.video_max_frames,
            excel_name=project_request.excel_name,
        )
        session.add(project)
        session.flush()
        session.refresh(project)
        return {"project": project_to_payload(project)}


@app.put("/api/projects/{project_id}")
def update_project(
    project_id: int,
    project_request: ProjectRequest,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        project = (
            session.query(Project)
            .filter(Project.id == project_id, Project.user_id == user.id)
            .first()
        )
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        project.name = project_request.name.strip()
        project.description = project_request.description.strip()
        project.source_dir = project_request.source_dir
        project.output_dir = project_request.output_dir
        project.debug_image_dir = project_request.debug_image_dir
        project.archive_source_dir = project_request.archive_source_dir
        project.project_name = project_request.project_name
        project.ocr_backend = project_request.ocr_backend
        project.handwriting_backend = project_request.handwriting_backend
        project.trocr_model = project_request.trocr_model
        project.ocr_profile = project_request.ocr_profile
        project.export_image_mode = project_request.export_image_mode
        project.naming_pattern = project_request.naming_pattern
        project.lang = project_request.lang
        project.dpi = project_request.dpi
        project.single_item_per_page = project_request.single_item_per_page
        project.save_text = project_request.save_text
        project.use_angle_cls = project_request.use_angle_cls
        project.move_processed_source = project_request.move_processed_source
        project.video_sample_seconds = project_request.video_sample_seconds
        project.video_max_frames = project_request.video_max_frames
        project.excel_name = project_request.excel_name
        session.flush()
        session.refresh(project)
        return {"project": project_to_payload(project)}


@app.delete("/api/projects/{project_id}")
def delete_project(project_id: int, x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        project = (
            session.query(Project)
            .filter(Project.id == project_id, Project.user_id == user.id)
            .first()
        )
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        session.delete(project)
        return {"deleted": True, "project_id": project_id}


@app.put("/api/documents/{document_id}")
def update_document(
    document_id: int,
    request: DocumentUpdateRequest,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        document = (
            session.query(DocumentRecord)
            .join(Project, Project.id == DocumentRecord.project_id)
            .filter(DocumentRecord.id == document_id, Project.user_id == user.id)
            .first()
        )
        if not document:
            raise HTTPException(status_code=404, detail="Stored document not found")

        project = session.query(Project).filter(Project.id == document.project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        fields = processor.DocumentFields(
            doc_type=request.doc_type.strip() or "Unknown",
            date=request.date.strip() or "Unknown",
            number=request.number.strip() or "Unknown",
            company_name=request.company_name.strip() or "Unknown",
            amount=request.amount.strip() or "Unknown",
        )
        new_output_name = processor.build_output_name(
            fields,
            project.project_name,
            project.naming_pattern,
        )
        confidence_score, confidence_label = processor.compute_confidence(fields)

        current_output_path = Path(document.output_path).expanduser() if document.output_path else None
        if current_output_path and current_output_path.exists():
            target_output_path = unique_target_path(current_output_path.with_name(new_output_name))
            if target_output_path != current_output_path:
                current_output_path.rename(target_output_path)
            document.output_path = str(target_output_path)
            document.output_file = target_output_path.name
        else:
            document.output_file = new_output_name

        if document.enhanced_output_path:
            current_enhanced_path = Path(document.enhanced_output_path).expanduser()
            if current_enhanced_path.exists():
                enhanced_name = f"{Path(new_output_name).stem}_enhanced.pdf"
                target_enhanced_path = unique_target_path(current_enhanced_path.with_name(enhanced_name))
                if target_enhanced_path != current_enhanced_path:
                    current_enhanced_path.rename(target_enhanced_path)
                document.enhanced_output_path = str(target_enhanced_path)

        document.doc_type = fields.doc_type
        document.date = fields.date
        document.number = fields.number
        document.company_name = fields.company_name
        document.amount = fields.amount
        document.currency = request.currency.strip() or "Unknown"
        document.confidence_score = confidence_score
        document.confidence_label = confidence_label
        session.flush()
        session.refresh(document)

        return {
            "document": {
                "id": document.id,
                "created_at": document.created_at.isoformat() if document.created_at else "",
                "source_file": document.source_file,
                "source_path": document.source_path,
                "source_hash": document.source_hash,
                "source_type": document.source_type,
                "source_origin": document.source_origin,
                "source_timestamp": document.source_timestamp,
                "output_file": document.output_file,
                "output_path": document.output_path,
                "enhanced_output_path": document.enhanced_output_path,
                "original_debug_image": document.original_debug_image,
                "enhanced_debug_image": document.enhanced_debug_image,
                "doc_type": document.doc_type,
                "date": document.date,
                "number": document.number,
                "company_name": document.company_name,
                "amount": document.amount,
                "currency": document.currency,
                "confidence_score": document.confidence_score,
                "confidence_label": document.confidence_label,
                "raw_text": document.raw_text,
            }
        }


@app.get("/api/projects/{project_id}/documents")
def project_documents(project_id: int, x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        project = (
            session.query(Project)
            .filter(Project.id == project_id, Project.user_id == user.id)
            .first()
        )
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        documents = (
            session.query(DocumentRecord)
            .filter(DocumentRecord.project_id == project.id)
            .order_by(DocumentRecord.created_at.desc())
            .all()
        )
        payload = []
        for document in documents:
            payload.append(
                {
                    "id": document.id,
                    "created_at": document.created_at.isoformat() if document.created_at else "",
                    "source_file": document.source_file,
                    "source_path": document.source_path,
                    "source_hash": document.source_hash,
                    "source_type": document.source_type,
                    "source_origin": document.source_origin,
                    "source_timestamp": document.source_timestamp,
                    "output_file": document.output_file,
                    "output_path": document.output_path,
                    "enhanced_output_path": document.enhanced_output_path,
                    "original_debug_image": document.original_debug_image,
                    "enhanced_debug_image": document.enhanced_debug_image,
                    "doc_type": document.doc_type,
                    "date": document.date,
                    "number": document.number,
                    "company_name": document.company_name,
                    "amount": document.amount,
                    "currency": document.currency,
                    "confidence_score": document.confidence_score,
                    "confidence_label": document.confidence_label,
                    "raw_text": document.raw_text,
                }
            )
        return {"documents": payload}


@app.get("/api/projects/{project_id}/export-results")
def export_project_results(
    project_id: int,
    format: Literal["csv", "xlsx"] = "csv",
    token: str = "",
    x_auth_token: str = Header(default=""),
) -> FileResponse:
    user = require_user(x_auth_token or token)
    with db_session() as session:
        project = (
            session.query(Project)
            .filter(Project.id == project_id, Project.user_id == user.id)
            .first()
        )
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        documents = (
            session.query(DocumentRecord)
            .filter(DocumentRecord.project_id == project.id)
            .order_by(DocumentRecord.created_at.desc())
            .all()
        )
        if not documents:
            raise HTTPException(status_code=404, detail="No stored results found for this project")

        export_dir = user_data_root() / "exports"
        export_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        safe_name = processor.sanitize_filename(project.name or "ULTRA_FORCE_Project")

        headers = [
            "CreatedAt",
            "SourceFile",
            "SourcePath",
            "SourceType",
            "SourceOrigin",
            "SourceTimestamp",
            "OutputFile",
            "OutputPath",
            "EnhancedOutputPath",
            "Type",
            "Date",
            "Number",
            "CompanyName",
            "Amount",
            "Currency",
            "ProjectName",
        ]

        if format == "csv":
            target = export_dir / f"{safe_name}_previous_results_{stamp}.csv"
            with target.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.writer(handle)
                writer.writerow(headers)
                for document in documents:
                    writer.writerow(
                        [
                            document.created_at.isoformat() if document.created_at else "",
                            document.source_file,
                            document.source_path,
                            document.source_type,
                            document.source_origin,
                            document.source_timestamp,
                            document.output_file,
                            document.output_path,
                            document.enhanced_output_path,
                            document.doc_type,
                            document.date,
                            document.number,
                            document.company_name,
                            document.amount,
                            document.currency,
                            project.project_name,
                        ]
                    )
            media_type = "text/csv"
        else:
            target = export_dir / f"{safe_name}_previous_results_{stamp}.xlsx"
            records = [
                processor.ProcessedRecord(
                    source_file=document.source_file,
                    source_path=document.source_path,
                    source_hash=document.source_hash,
                    source_type=document.source_type,
                    source_origin=document.source_origin,
                    source_timestamp=document.source_timestamp,
                    output_file=document.output_file,
                    doc_type=document.doc_type,
                    date=document.date,
                    number=document.number,
                    company_name=document.company_name,
                    amount=document.amount,
                    currency=document.currency,
                    project_name=project.project_name,
                    confidence_score=document.confidence_score,
                    confidence_label=document.confidence_label,
                    raw_text=document.raw_text,
                )
                for document in documents
            ]
            processor.write_excel_summary(records, target)
            media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    return FileResponse(target, media_type=media_type, filename=target.name)


@app.get("/api/projects/{project_id}/download-results")
def download_project_results(
    project_id: int,
    scope: Literal["all", "selected"] = "all",
    ids: str = "",
    token: str = "",
    x_auth_token: str = Header(default=""),
) -> FileResponse:
    user = require_user(x_auth_token or token)
    with db_session() as session:
        project = (
            session.query(Project)
            .filter(Project.id == project_id, Project.user_id == user.id)
            .first()
        )
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        query = session.query(DocumentRecord).filter(DocumentRecord.project_id == project.id)
        if scope == "selected":
            selected_ids = [int(value) for value in ids.split(",") if value.strip().isdigit()]
            if not selected_ids:
                raise HTTPException(status_code=400, detail="No result rows were selected")
            query = query.filter(DocumentRecord.id.in_(selected_ids))

        documents = query.order_by(DocumentRecord.created_at.desc()).all()
        if not documents:
            raise HTTPException(status_code=404, detail="No matching results found for download")

        export_dir = user_data_root() / "exports"
        export_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        safe_name = processor.sanitize_filename(project.name or "ULTRA_FORCE_Project")
        target = export_dir / f"{safe_name}_output_pdfs_{scope}_{stamp}.zip"

        added = 0
        with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for document in documents:
                output_path = Path(document.output_path or "").expanduser()
                if not output_path.exists() or not output_path.is_file():
                    continue
                archive_name = processor.sanitize_filename(document.output_file or output_path.name)
                archive.write(output_path, arcname=archive_name)
                added += 1

        if added == 0:
            target.unlink(missing_ok=True)
            raise HTTPException(status_code=404, detail="No output PDF files were available for download")

    return FileResponse(target, media_type="application/zip", filename=target.name)


@app.get("/api/file")
def get_file(path: str, token: str = "", x_auth_token: str = Header(default="")) -> FileResponse:
    auth_token = x_auth_token or token
    require_user(auth_token)
    target = Path(path).expanduser().resolve()
    if not target.exists() or not target.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(target)


class PickFolderRequest(BaseModel):
    purpose: Literal["source", "output", "debug", "archive"] = "source"


@app.post("/api/pick-folder")
def pick_folder(request: PickFolderRequest) -> Dict[str, str]:
    prompt = {
        "source": "Choose source folder",
        "output": "Choose output folder",
        "debug": "Choose debug image folder",
        "archive": "Choose processed source archive folder",
    }[request.purpose]
    try:
        path = choose_folder_native(prompt)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return {"path": path}


class PickFileRequest(BaseModel):
    purpose: Literal["video"] = "video"


@app.post("/api/pick-file")
def pick_file(request: PickFileRequest) -> Dict[str, str]:
    prompt = {
        "video": "Choose video file",
    }[request.purpose]
    extensions = {
        "video": ["mp4", "mov", "m4v", "avi"],
    }[request.purpose]
    try:
        path = choose_file_native(prompt, extensions)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return {"path": path}


@app.get("/api/runtime")
def runtime_report() -> Dict[str, Any]:
    return build_runtime_payload()


@app.post("/api/jobs")
def create_job(request: ProcessRequest, x_auth_token: str = Header(default="")) -> Dict[str, str]:
    user = require_user(x_auth_token)
    job = JobState(job_id=str(uuid.uuid4()), user_id=user.id, project_id=request.project_id)
    with JOBS_LOCK:
        JOBS[job.job_id] = job
    thread = threading.Thread(target=run_job, args=(job, request), daemon=True)
    thread.start()
    return {"job_id": job.job_id}


@app.post("/api/jobs/{job_id}/cancel")
def cancel_job(job_id: str, x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with JOBS_LOCK:
        job = JOBS.get(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        if job.user_id != user.id:
            raise HTTPException(status_code=403, detail="Not allowed")
        if job.status not in {"queued", "running"}:
            return {"job_id": job_id, "status": job.status}
        job.cancel_requested = True
        job.status = "cancelling"
        job.logs.append("Cancellation requested. ULTRA FORCE will stop after the current file.")
        return {"job_id": job_id, "status": job.status}


@app.get("/api/jobs/{job_id}")
def get_job(job_id: str, x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with JOBS_LOCK:
        job = JOBS.get(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        if job.user_id != user.id:
            raise HTTPException(status_code=403, detail="Not allowed")
        return asdict(job)


@app.get("/api/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


if STATIC_DIR.exists():
    app.mount("/assets", StaticFiles(directory=STATIC_DIR / "assets"), name="assets")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


def main() -> None:
    import uvicorn

    host = "127.0.0.1"
    port = 8765
    if not sys.stdout.isatty():
        threading.Timer(1.0, lambda: webbrowser.open(f"http://{host}:{port}")).start()
    uvicorn.run(app, host=host, port=port, reload=False)


if __name__ == "__main__":
    main()
