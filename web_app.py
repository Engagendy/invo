import csv
import calendar
import hashlib
import json
import platform
import shutil
import io
import subprocess
import sys
import threading
import uuid
import webbrowser
import zipfile
import re
from datetime import datetime
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Tuple

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy import func, or_

from app_paths import bundled_web_dir, runtime_root, user_data_root
import invoice_processor as processor
from web_db import (
    AccountingAccount,
    AccountingPeriod,
    AuthSession,
    CompanyAllocation,
    CompanyAccountingRule,
    CompanyBillingEvent,
    Company,
    CompanyDimension,
    CompanyParty,
    CompanyPurchaseOrder,
    CompanyProcurementReview,
    CompanyReceipt,
    DocumentRecord,
    DocumentAttachment,
    JournalEntry,
    JournalEntryLine,
    Project,
    ProjectComment,
    ProjectMember,
    ProjectRule,
    SavedSearch,
    User,
    VendorAlias,
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

ACCOUNTING_EXPORT_PRESETS = {
    "ultra_force": {
        "label": "ULTRA FORCE",
        "description": "Full internal export with reconciliation and tagging fields.",
    },
    "odoo_vendor_bills": {
        "label": "Odoo Vendor Bills",
        "description": "Vendor-bill oriented export for Odoo-style accounting import.",
    },
    "quickbooks_expenses": {
        "label": "QuickBooks Expenses",
        "description": "Expense-oriented export with vendor, class, and customer/project columns.",
    },
    "sap_ap": {
        "label": "SAP AP",
        "description": "Accounts payable style export with assignment and cost center fields.",
    },
}


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
    job_code: str = ""
    client_name: str = ""
    site_name: str = ""
    contract_number: str = ""
    budget_amount: str = ""
    contract_value: str = ""
    variation_amount: str = ""
    billed_to_date: str = ""
    certified_progress_pct: str = ""
    retention_percent: str = ""
    advance_received: str = ""
    project_status: str = "active"


class DocumentUpdateRequest(BaseModel):
    doc_type: str
    date: str
    number: str
    company_name: str
    amount: str
    currency: str


class ReviewUpdateRequest(BaseModel):
    review_state: str
    review_note: str = ""


class DocumentTagsUpdateRequest(BaseModel):
    canonical_company_name: str = ""
    category: str = ""
    subcategory: str = ""
    account_code: str = ""
    offset_account_code: str = ""
    cost_code: str = ""
    cost_center: str = ""
    project_code: str = ""
    purchase_order_id: int | None = None
    payment_method: str = ""
    vat_flag: bool = False


class ProjectRuleRequest(BaseModel):
    keyword: str
    source_type: str = ""
    status: str = ""
    category: str = ""
    subcategory: str = ""
    account_code: str = ""
    offset_account_code: str = ""
    project_code: str = ""
    cost_code: str = ""
    cost_center: str = ""
    payment_method: str = ""
    vat_flag: bool = False
    auto_post: bool = True


class FeedbackApplyRequest(BaseModel):
    suggestion_type: str
    normalized_key: str = ""
    canonical_name: str = ""
    keyword: str = ""
    source_type: str = ""
    status: str = ""
    category: str = ""
    subcategory: str = ""


class VendorAliasRequest(BaseModel):
    normalized_key: str
    canonical_name: str


class ProjectCommentRequest(BaseModel):
    body: str
    document_id: Optional[int] = None


class ProjectMemberRequest(BaseModel):
    username: str
    role: str = "reviewer"


class DocumentAssignmentRequest(BaseModel):
    assigned_user_id: Optional[int] = None


class AttachmentRequest(BaseModel):
    attachment_type: str = "supporting_document"
    label: str = ""
    file_path: str
    note: str = ""


class SavedSearchRequest(BaseModel):
    name: str
    scope: str = "global_search"
    query: Dict[str, Any] = {}


class ResourceRerunRequest(BaseModel):
    source_path: str


class AccountingAccountRequest(BaseModel):
    code: str
    name: str
    account_type: str
    subtype: str = ""
    is_active: bool = True


class AccountingPeriodRequest(BaseModel):
    name: str
    start_date: str
    end_date: str
    status: str = "open"


class QuarterSeedRequest(BaseModel):
    year: int
    status: str = "open"


class MissingPeriodSeedRequest(BaseModel):
    status: str = "open"


class CompanyUpdateRequest(BaseModel):
    name: str = ""
    base_currency: str = "AED"
    fiscal_year_start_month: int = 1
    vat_registration_number: str = ""
    vat_rate: str = "5.00"


class CompanyCreateRequest(BaseModel):
    name: str


class CompanyAccountingRuleRequest(BaseModel):
    keyword: str
    source_type: str = ""
    status: str = ""
    category: str = ""
    subcategory: str = ""
    account_code: str = ""
    offset_account_code: str = ""
    project_code: str = ""
    cost_code: str = ""
    cost_center: str = ""
    payment_method: str = ""
    vat_flag: bool = False
    auto_post: bool = True


class CompanyPartyRequest(BaseModel):
    party_type: str = "supplier"
    name: str
    tax_registration_number: str = ""
    contact_email: str = ""
    contact_phone: str = ""
    default_account_code: str = ""
    payment_terms_days: int = 30


class CompanyDimensionRequest(BaseModel):
    dimension_type: str = "project_code"
    code: str
    name: str = ""
    is_active: bool = True


class CompanyAllocationRequest(BaseModel):
    allocation_type: str = "payable"
    payment_document_id: int
    target_document_id: int
    amount: str
    note: str = ""


class CompanyBillingEventRequest(BaseModel):
    project_id: int
    event_type: str = "progress_claim"
    label: str = ""
    event_date: str
    amount: str
    status: str = "draft"
    note: str = ""


class CompanyPurchaseOrderRequest(BaseModel):
    project_id: int
    supplier_party_id: int | None = None
    cost_code: str = ""
    po_number: str = ""
    po_date: str
    amount: str
    status: str = "open"
    note: str = ""


class CompanyReceiptRequest(BaseModel):
    purchase_order_id: int
    receipt_type: str = "goods_receipt"
    receipt_number: str = ""
    receipt_date: str
    amount: str
    status: str = "received"
    note: str = ""


class CompanyProcurementReviewRequest(BaseModel):
    project_id: int
    supplier_name: str
    match_flag: str
    assigned_user_id: int | None = None
    review_state: str = "open"
    note: str = ""


class ManualJournalLineRequest(BaseModel):
    account_code: str
    debit: str = ""
    credit: str = ""
    project_code: str = ""
    cost_center: str = ""


class ManualJournalRequest(BaseModel):
    entry_date: str
    reference: str = ""
    memo: str = ""
    lines: List[ManualJournalLineRequest]


class JournalPostRequest(BaseModel):
    document_ids: List[int] = []


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


def enqueue_job(user_id: int, request: ProcessRequest) -> JobState:
    job = JobState(job_id=str(uuid.uuid4()), user_id=user_id, project_id=request.project_id)
    with JOBS_LOCK:
        JOBS[job.job_id] = job
    thread = threading.Thread(target=run_job, args=(job, request), daemon=True)
    thread.start()
    return job


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
    installed = any(
        path.exists()
        for path in (
            processor.trocr_model_dir(model_name),
            processor.bundled_trocr_model_dir(model_name),
            processor.trocr_model_cache_dir(model_name),
            processor.bundled_trocr_model_cache_dir(model_name),
        )
    )
    with MODEL_LOCK:
        download = MODEL_DOWNLOADS.get(model_name, {}).copy()
    status = download.get("status", "installed" if installed else "not_installed")
    message = download.get("message", "")
    return {
        "name": model_name,
        "installed": "true" if installed else "false",
        "status": status,
        "message": message,
        "removable": "true" if (
            processor.trocr_model_dir(model_name).exists()
            or processor.trocr_model_cache_dir(model_name).exists()
        ) else "false",
    }


def model_payload() -> Dict[str, Any]:
    items = []
    for item in trocr_model_catalog():
        status = get_model_status(item["name"])
        items.append({**item, **status})
    return {"models": items}


def accounting_export_metadata() -> List[Dict[str, str]]:
    return [
        {"key": key, **value}
        for key, value in ACCOUNTING_EXPORT_PRESETS.items()
    ]


def ensure_user_company(session, user: User) -> Company:
    company = None
    company_id = getattr(user, "company_id", None)
    if company_id:
        company = session.query(Company).filter(Company.id == company_id).first()
    if not company:
        company = session.query(Company).filter(Company.user_id == user.id).order_by(Company.id.asc()).first()
    if not company:
        company = Company(user_id=user.id, name=f"{user.username} Company")
        session.add(company)
        session.flush()
    user.company_id = company.id
    session.query(Project).filter(Project.user_id == user.id, Project.company_id.is_(None)).update(
        {"company_id": company.id},
        synchronize_session=False,
    )
    session.query(AccountingAccount).filter(AccountingAccount.user_id == user.id, AccountingAccount.company_id.is_(None)).update(
        {"company_id": company.id},
        synchronize_session=False,
    )
    session.query(AccountingPeriod).filter(AccountingPeriod.user_id == user.id, AccountingPeriod.company_id.is_(None)).update(
        {"company_id": company.id},
        synchronize_session=False,
    )
    session.query(JournalEntry).filter(JournalEntry.user_id == user.id, JournalEntry.company_id.is_(None)).update(
        {"company_id": company.id},
        synchronize_session=False,
    )
    session.flush()
    return company


def ensure_project_company(session, project: Project, user: User) -> Company:
    company = ensure_user_company(session, user)
    if getattr(project, "company_id", None) != company.id:
        project.company_id = company.id
        session.flush()
    return company


def require_current_company(session, user: User) -> Company:
    return ensure_user_company(session, user)


def require_company_anchor_project(session, company: Company, user: User) -> Project:
    project = (
        session.query(Project)
        .filter(Project.company_id == company.id)
        .order_by(Project.created_at.asc(), Project.id.asc())
        .first()
    )
    if not project:
        raise HTTPException(status_code=400, detail="Create at least one project before using company accounting setup")
    if getattr(project, "company_id", None) != company.id:
        project.company_id = company.id
        session.flush()
    return project


def default_construction_accounts() -> List[Dict[str, str]]:
    return [
        {"code": "1000", "name": "Cash On Hand", "account_type": "asset", "subtype": "cash"},
        {"code": "1010", "name": "Bank Current Account", "account_type": "asset", "subtype": "bank"},
        {"code": "1100", "name": "Accounts Receivable", "account_type": "asset", "subtype": "receivable"},
        {"code": "1110", "name": "Retention Receivable", "account_type": "asset", "subtype": "receivable"},
        {"code": "1200", "name": "Inventory Materials", "account_type": "asset", "subtype": "inventory"},
        {"code": "1300", "name": "Prepaid Expenses", "account_type": "asset", "subtype": "prepaid"},
        {"code": "1500", "name": "Fixed Assets", "account_type": "asset", "subtype": "fixed_asset"},
        {"code": "2000", "name": "Accounts Payable", "account_type": "liability", "subtype": "payable"},
        {"code": "2010", "name": "Retention Payable", "account_type": "liability", "subtype": "payable"},
        {"code": "2100", "name": "Accrued Expenses", "account_type": "liability", "subtype": "accrual"},
        {"code": "2200", "name": "VAT Payable", "account_type": "liability", "subtype": "tax"},
        {"code": "3000", "name": "Owner Equity", "account_type": "equity", "subtype": "equity"},
        {"code": "4000", "name": "Contract Revenue", "account_type": "revenue", "subtype": "contract_revenue"},
        {"code": "4010", "name": "Variation Order Revenue", "account_type": "revenue", "subtype": "variation_revenue"},
        {"code": "5000", "name": "Direct Materials", "account_type": "expense", "subtype": "materials"},
        {"code": "5010", "name": "Direct Labor", "account_type": "expense", "subtype": "labor"},
        {"code": "5020", "name": "Subcontractor Cost", "account_type": "expense", "subtype": "subcontractor"},
        {"code": "5030", "name": "Equipment And Tools", "account_type": "expense", "subtype": "equipment"},
        {"code": "5040", "name": "Site Overheads", "account_type": "expense", "subtype": "site_overhead"},
        {"code": "5050", "name": "Vehicle And Fuel", "account_type": "expense", "subtype": "vehicle"},
        {"code": "5060", "name": "Office Overheads", "account_type": "expense", "subtype": "office_overhead"},
        {"code": "5070", "name": "Bank Charges", "account_type": "expense", "subtype": "bank_charges"},
    ]


def seeded_accounting_rule_specs() -> List[Dict[str, Any]]:
    return [
        {"keyword": "salary", "source_type": "sheet", "status": "not_applicable", "category": "Payroll", "subcategory": "Salary", "account_code": "5010", "offset_account_code": "1010", "payment_method": "bank"},
        {"keyword": "payroll", "source_type": "sheet", "status": "not_applicable", "category": "Payroll", "subcategory": "Salary", "account_code": "5010", "offset_account_code": "1010", "payment_method": "bank"},
        {"keyword": "bank charge", "source_type": "sheet", "status": "not_applicable", "category": "Banking", "subcategory": "Bank Charges", "account_code": "5070", "offset_account_code": "1010", "payment_method": "bank"},
        {"keyword": "charge", "source_type": "sheet", "status": "not_applicable", "category": "Banking", "subcategory": "Bank Charges", "account_code": "5070", "offset_account_code": "1010", "payment_method": "bank"},
        {"keyword": "fee", "source_type": "sheet", "status": "not_applicable", "category": "Banking", "subcategory": "Bank Charges", "account_code": "5070", "offset_account_code": "1010", "payment_method": "bank"},
        {"keyword": "adnoc", "source_type": "", "status": "", "category": "Operations", "subcategory": "Fuel", "account_code": "5050", "offset_account_code": "1010", "payment_method": "bank"},
        {"keyword": "enoc", "source_type": "", "status": "", "category": "Operations", "subcategory": "Fuel", "account_code": "5050", "offset_account_code": "1010", "payment_method": "bank"},
        {"keyword": "emarat", "source_type": "", "status": "", "category": "Operations", "subcategory": "Fuel", "account_code": "5050", "offset_account_code": "1010", "payment_method": "bank"},
        {"keyword": "cafu", "source_type": "", "status": "", "category": "Operations", "subcategory": "Fuel", "account_code": "5050", "offset_account_code": "1010", "payment_method": "bank"},
        {"keyword": "amazon", "source_type": "", "status": "", "category": "Purchasing", "subcategory": "Materials", "account_code": "5000", "offset_account_code": "2000", "payment_method": "credit_card"},
        {"keyword": "ace", "source_type": "", "status": "", "category": "Purchasing", "subcategory": "Materials", "account_code": "5000", "offset_account_code": "2000", "payment_method": "credit_card"},
        {"keyword": "danube", "source_type": "", "status": "", "category": "Purchasing", "subcategory": "Materials", "account_code": "5000", "offset_account_code": "2000", "payment_method": "credit_card"},
        {"keyword": "dragon mart", "source_type": "", "status": "", "category": "Purchasing", "subcategory": "Materials", "account_code": "5000", "offset_account_code": "2000", "payment_method": "credit_card"},
        {"keyword": "shein", "source_type": "", "status": "", "category": "Office", "subcategory": "Office Overheads", "account_code": "5060", "offset_account_code": "2000", "payment_method": "credit_card"},
        {"keyword": "noon", "source_type": "", "status": "", "category": "Office", "subcategory": "Office Overheads", "account_code": "5060", "offset_account_code": "2000", "payment_method": "credit_card"},
        {"keyword": "ikea", "source_type": "", "status": "", "category": "Office", "subcategory": "Office Overheads", "account_code": "5060", "offset_account_code": "2000", "payment_method": "credit_card"},
        {"keyword": "pan home", "source_type": "", "status": "", "category": "Office", "subcategory": "Office Overheads", "account_code": "5060", "offset_account_code": "2000", "payment_method": "credit_card"},
        {"keyword": "du", "source_type": "", "status": "", "category": "Utilities", "subcategory": "Telecom", "account_code": "5060", "offset_account_code": "2000", "payment_method": "bank"},
        {"keyword": "etisalat", "source_type": "", "status": "", "category": "Utilities", "subcategory": "Telecom", "account_code": "5060", "offset_account_code": "2000", "payment_method": "bank"},
        {"keyword": "careem", "source_type": "", "status": "", "category": "Transport", "subcategory": "Taxi", "account_code": "5040", "offset_account_code": "2000", "payment_method": "credit_card"},
        {"keyword": "uber", "source_type": "", "status": "", "category": "Transport", "subcategory": "Taxi", "account_code": "5040", "offset_account_code": "2000", "payment_method": "credit_card"},
        {"keyword": "talabat", "source_type": "", "status": "", "category": "Meals", "subcategory": "Staff Meals", "account_code": "5060", "offset_account_code": "2000", "payment_method": "credit_card"},
        {"keyword": "deliveroo", "source_type": "", "status": "", "category": "Meals", "subcategory": "Staff Meals", "account_code": "5060", "offset_account_code": "2000", "payment_method": "credit_card"},
        {"keyword": "transfer", "source_type": "sheet", "status": "not_applicable", "category": "Banking", "subcategory": "Transfer", "account_code": "", "offset_account_code": "", "payment_method": "bank"},
        {"keyword": "payment received", "source_type": "sheet", "status": "not_applicable", "category": "Collections", "subcategory": "Customer Receipt", "account_code": "1100", "offset_account_code": "1010", "payment_method": "bank"},
        {"keyword": "refund", "source_type": "sheet", "status": "not_applicable", "category": "Refund", "subcategory": "Vendor Refund", "account_code": "1010", "offset_account_code": "2000", "payment_method": "bank"},
    ]


def infer_rule_spec_from_document(document: DocumentRecord) -> Optional[Dict[str, Any]]:
    vendor = (document.canonical_company_name or document.company_name or "").strip()
    if not vendor:
        return None
    normalized_vendor = normalize_company_name(vendor)
    if len(normalized_vendor) < 4:
        return None
    source_type = (document.source_type or "").strip().lower()
    direction = journal_direction_for_document(document)
    category = (document.category or "").strip()
    subcategory = (document.subcategory or "").strip()
    account_code = (document.account_code or "").strip()
    offset_account_code = (document.offset_account_code or "").strip()
    payment_method = (document.payment_method or "").strip()

    if not category and source_type == "sheet" and direction == "credit":
        category = "Collections"
        subcategory = subcategory or "Customer Receipt"
        account_code = account_code or "1100"
        offset_account_code = offset_account_code or "1010"
        payment_method = payment_method or "bank"
    elif not category and source_type == "sheet" and direction == "debit":
        category = "Purchasing"
        subcategory = subcategory or "Bank Purchase"
        account_code = account_code or "5000"
        offset_account_code = offset_account_code or "1010"
        payment_method = payment_method or "bank"
    elif not category:
        category = "Purchasing"
        subcategory = subcategory or "Expense"
        account_code = account_code or "5000"
        offset_account_code = offset_account_code or "2000"
        payment_method = payment_method or ("credit_card" if source_type in {"pdf", "video"} else "bank")

    return {
        "keyword": vendor,
        "source_type": source_type,
        "status": "",
        "category": category,
        "subcategory": subcategory,
        "account_code": account_code,
        "offset_account_code": offset_account_code,
        "project_code": (document.project_code or "").strip(),
        "cost_code": (document.cost_code or "").strip(),
        "cost_center": (document.cost_center or "").strip(),
        "payment_method": payment_method,
        "vat_flag": bool(document.vat_flag),
        "auto_post": True,
    }


def journal_direction_for_document(document: DocumentRecord) -> str:
    direction = (document.transaction_direction or "").strip().lower()
    if direction in {"debit", "credit"}:
        return direction
    source_type = (document.source_type or "").strip().lower()
    if source_type in {"pdf", "video"}:
        return "debit"
    status = (document.match_status or "").strip().lower()
    if status == "not_applicable" and "received" in (document.raw_text or "").lower():
        return "credit"
    return "debit"


def default_offset_account_for_document(document: DocumentRecord) -> str:
    source_type = (document.source_type or "").strip().lower()
    direction = journal_direction_for_document(document)
    if document.offset_account_code:
        return document.offset_account_code
    if source_type == "sheet":
        return "1010"
    if direction == "credit":
        return "1100"
    return "2000"


def journal_draft_for_document(document: DocumentRecord, rules: Optional[List[ProjectRule]] = None) -> Optional[Dict[str, Any]]:
    amount = processor.amount_to_float(document.amount)
    if amount is None or amount <= 0:
        return None
    tag_meta = record_tag_meta(document, rules or [])
    primary_account = (tag_meta["account_code"] or "").strip()
    if not primary_account:
        return None
    offset_account = (tag_meta["offset_account_code"] or "").strip() or default_offset_account_for_document(document)
    direction = journal_direction_for_document(document)
    memo_parts = [
        document.canonical_company_name or document.company_name or "",
        document.number or "",
        document.source_file or "",
    ]
    memo = " | ".join(part for part in memo_parts if part)
    if direction == "credit":
        lines = [
            {"account_code": offset_account, "debit": f"{amount:.2f}", "credit": "", "role": "offset"},
            {"account_code": primary_account, "debit": "", "credit": f"{amount:.2f}", "role": "primary"},
        ]
    else:
        lines = [
            {"account_code": primary_account, "debit": f"{amount:.2f}", "credit": "", "role": "primary"},
            {"account_code": offset_account, "debit": "", "credit": f"{amount:.2f}", "role": "offset"},
        ]
    return {
        "document_id": document.id,
        "date": document.date or "",
        "reference": document.number or "",
        "vendor": document.canonical_company_name or document.company_name or "",
        "amount": f"{amount:.2f}",
        "source_type": document.source_type or "",
        "memo": memo,
        "status": document.review_state or document.match_status or "",
        "project_code": tag_meta["project_code"] or "",
        "cost_code": tag_meta["cost_code"] or "",
        "cost_center": tag_meta["cost_center"] or "",
        "payment_method": tag_meta["payment_method"] or "",
        "rule_keyword": tag_meta["rule_keyword"] or "",
        "auto_post": bool(tag_meta["auto_post"]),
        "lines": lines,
    }


def combined_accounting_rules(project_rules: Optional[List[Any]] = None, company_rules: Optional[List[Any]] = None) -> List[Any]:
    return list(project_rules or []) + list(company_rules or [])


def company_period_for_date(periods: List[AccountingPeriod], entry_date: str) -> Optional[AccountingPeriod]:
    value = (entry_date or "").strip()
    if not value:
        return None
    for period in periods:
        start_date = (period.start_date or "").strip()
        end_date = (period.end_date or "").strip()
        if start_date and end_date and start_date <= value <= end_date:
            return period
    return None


def annotate_draft_with_period(draft: Dict[str, Any], periods: List[AccountingPeriod]) -> Dict[str, Any]:
    period = company_period_for_date(periods, draft.get("date", ""))
    if not period:
        draft["period_name"] = ""
        draft["period_status"] = "missing"
        draft["posting_allowed"] = False
        draft["posting_reason"] = "No accounting period covers this draft date."
        return draft
    status = (period.status or "open").strip().lower()
    draft["period_name"] = period.name or ""
    draft["period_status"] = status
    draft["posting_allowed"] = status == "open"
    draft["posting_reason"] = "" if status == "open" else f'Posting blocked because period "{period.name}" is {status}.'
    return draft


def trial_balance_rows(entries: List[JournalEntry]) -> List[Dict[str, Any]]:
    buckets: Dict[str, Dict[str, float]] = {}
    for entry in entries:
        if (entry.status or "").lower() != "posted":
            continue
        for line in entry.lines:
            bucket = buckets.setdefault(line.account_code or "Unknown", {"debit": 0.0, "credit": 0.0})
            bucket["debit"] += processor.amount_to_float(line.debit) or 0.0
            bucket["credit"] += processor.amount_to_float(line.credit) or 0.0
    rows = []
    for account_code, totals in sorted(buckets.items()):
        rows.append({
            "account_code": account_code,
            "debit": round(totals["debit"], 2),
            "credit": round(totals["credit"], 2),
            "balance": round(totals["debit"] - totals["credit"], 2),
        })
    return rows


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


PROJECT_ROLE_RANK = {
    "viewer": 10,
    "reviewer": 20,
    "admin": 30,
    "owner": 40,
}


def project_access_role(session, project: Project, user: User) -> Optional[str]:
    if project.user_id == user.id:
        return "owner"
    member = (
        session.query(ProjectMember)
        .filter(ProjectMember.project_id == project.id, ProjectMember.user_id == user.id)
        .first()
    )
    if not member:
        return None
    role = (member.role or "viewer").strip().lower()
    return role if role in PROJECT_ROLE_RANK else "viewer"


def require_project_access(
    session,
    project_id: int,
    user: User,
    min_role: str = "viewer",
) -> tuple[Project, str]:
    project = session.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    access_role = project_access_role(session, project, user)
    if not access_role or PROJECT_ROLE_RANK.get(access_role, 0) < PROJECT_ROLE_RANK.get(min_role, 0):
        raise HTTPException(status_code=403, detail="Project access denied")
    return project, access_role


def require_document_access(
    session,
    document_id: int,
    user: User,
    min_role: str = "viewer",
) -> tuple[DocumentRecord, Project, str]:
    document = session.query(DocumentRecord).filter(DocumentRecord.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Stored document not found")
    project, access_role = require_project_access(session, document.project_id, user, min_role=min_role)
    return document, project, access_role


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


def project_to_payload(project: Project, access_role: str = "owner") -> Dict[str, Any]:
    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "job_code": getattr(project, "job_code", "") or "",
        "client_name": getattr(project, "client_name", "") or "",
        "site_name": getattr(project, "site_name", "") or "",
        "contract_number": getattr(project, "contract_number", "") or "",
        "budget_amount": getattr(project, "budget_amount", "") or "",
        "contract_value": getattr(project, "contract_value", "") or "",
        "variation_amount": getattr(project, "variation_amount", "") or "",
        "billed_to_date": getattr(project, "billed_to_date", "") or "",
        "certified_progress_pct": getattr(project, "certified_progress_pct", "") or "",
        "retention_percent": getattr(project, "retention_percent", "") or "",
        "advance_received": getattr(project, "advance_received", "") or "",
        "project_status": getattr(project, "project_status", "active") or "active",
        "access_role": access_role,
        "company_id": getattr(project, "company_id", None),
        "company_name": getattr(project, "company_name", "") or "",
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


def serialize_rule(rule: ProjectRule) -> Dict[str, Any]:
    return {
        "id": rule.id,
        "keyword": rule.keyword,
        "source_type": rule.source_type,
        "status": rule.status,
        "category": rule.category,
        "subcategory": rule.subcategory,
        "account_code": getattr(rule, "account_code", "") or "",
        "offset_account_code": getattr(rule, "offset_account_code", "") or "",
        "project_code": getattr(rule, "project_code", "") or "",
        "cost_code": getattr(rule, "cost_code", "") or "",
        "cost_center": getattr(rule, "cost_center", "") or "",
        "payment_method": getattr(rule, "payment_method", "") or "",
        "vat_flag": bool(getattr(rule, "vat_flag", False)),
        "auto_post": bool(getattr(rule, "auto_post", True)),
        "created_at": rule.created_at.isoformat() if rule.created_at else "",
    }


def serialize_vendor_alias(alias: VendorAlias) -> Dict[str, Any]:
    return {
        "id": alias.id,
        "normalized_key": alias.normalized_key,
        "canonical_name": alias.canonical_name,
        "created_at": alias.created_at.isoformat() if alias.created_at else "",
    }


def serialize_comment(comment: ProjectComment, username: str = "") -> Dict[str, Any]:
    return {
        "id": comment.id,
        "document_id": comment.document_id,
        "body": comment.body,
        "username": username,
        "created_at": comment.created_at.isoformat() if comment.created_at else "",
    }


def serialize_attachment(attachment: DocumentAttachment, username: str = "") -> Dict[str, Any]:
    return {
        "id": attachment.id,
        "document_id": attachment.document_id,
        "attachment_type": getattr(attachment, "attachment_type", "supporting_document") or "supporting_document",
        "label": attachment.label,
        "file_path": attachment.file_path,
        "file_name": attachment.file_name,
        "note": attachment.note,
        "username": username,
        "created_at": attachment.created_at.isoformat() if attachment.created_at else "",
    }


def serialize_saved_search(saved_search: SavedSearch) -> Dict[str, Any]:
    try:
        query = json.loads(saved_search.query_json or "{}")
    except Exception:
        query = {}
    return {
        "id": saved_search.id,
        "name": saved_search.name,
        "scope": saved_search.scope,
        "query": query,
        "created_at": saved_search.created_at.isoformat() if saved_search.created_at else "",
    }


def serialize_account(account: AccountingAccount) -> Dict[str, Any]:
    return {
        "id": account.id,
        "code": account.code,
        "name": account.name,
        "account_type": account.account_type,
        "subtype": account.subtype,
        "is_active": bool(account.is_active),
        "created_at": account.created_at.isoformat() if account.created_at else "",
    }


def serialize_period(period: AccountingPeriod) -> Dict[str, Any]:
    return {
        "id": period.id,
        "name": period.name,
        "start_date": period.start_date,
        "end_date": period.end_date,
        "status": period.status,
        "created_at": period.created_at.isoformat() if period.created_at else "",
    }


def serialize_journal_entry(entry: JournalEntry) -> Dict[str, Any]:
    return {
        "id": entry.id,
        "document_id": entry.document_id,
        "entry_date": entry.entry_date,
        "reference": entry.reference,
        "memo": entry.memo,
        "status": entry.status,
        "created_at": entry.created_at.isoformat() if entry.created_at else "",
        "lines": [
            {
                "id": line.id,
                "account_code": line.account_code,
                "debit": line.debit,
                "credit": line.credit,
                "cost_center": line.cost_center,
                "project_code": line.project_code,
            }
            for line in sorted(entry.lines, key=lambda item: item.id)
        ],
    }


def serialize_company(company: Company) -> Dict[str, Any]:
    return {
        "id": company.id,
        "name": company.name,
        "base_currency": getattr(company, "base_currency", "AED") or "AED",
        "fiscal_year_start_month": int(getattr(company, "fiscal_year_start_month", 1) or 1),
        "vat_registration_number": getattr(company, "vat_registration_number", "") or "",
        "vat_rate": getattr(company, "vat_rate", "5.00") or "5.00",
        "created_at": company.created_at.isoformat() if company.created_at else "",
    }


def serialize_accounting_rule(rule: Any, scope: str = "project") -> Dict[str, Any]:
    return {
        "id": rule.id,
        "scope": scope,
        "keyword": rule.keyword,
        "source_type": rule.source_type,
        "status": rule.status,
        "category": rule.category,
        "subcategory": rule.subcategory,
        "account_code": getattr(rule, "account_code", "") or "",
        "offset_account_code": getattr(rule, "offset_account_code", "") or "",
        "project_code": getattr(rule, "project_code", "") or "",
        "cost_code": getattr(rule, "cost_code", "") or "",
        "cost_center": getattr(rule, "cost_center", "") or "",
        "payment_method": getattr(rule, "payment_method", "") or "",
        "vat_flag": bool(getattr(rule, "vat_flag", False)),
        "auto_post": bool(getattr(rule, "auto_post", True)),
        "created_at": rule.created_at.isoformat() if getattr(rule, "created_at", None) else "",
    }


def serialize_company_party(party: CompanyParty) -> Dict[str, Any]:
    return {
        "id": party.id,
        "party_type": party.party_type,
        "name": party.name,
        "tax_registration_number": party.tax_registration_number,
        "contact_email": party.contact_email,
        "contact_phone": party.contact_phone,
        "default_account_code": party.default_account_code,
        "payment_terms_days": party.payment_terms_days,
        "created_at": party.created_at.isoformat() if party.created_at else "",
    }


def serialize_company_dimension(item: CompanyDimension) -> Dict[str, Any]:
    return {
        "id": item.id,
        "dimension_type": item.dimension_type,
        "code": item.code,
        "name": item.name,
        "is_active": bool(item.is_active),
        "created_at": item.created_at.isoformat() if item.created_at else "",
    }


def serialize_company_allocation(item: CompanyAllocation) -> Dict[str, Any]:
    return {
        "id": item.id,
        "allocation_type": item.allocation_type,
        "payment_document_id": item.payment_document_id,
        "target_document_id": item.target_document_id,
        "amount": item.amount,
        "note": item.note,
        "created_at": item.created_at.isoformat() if item.created_at else "",
    }


def serialize_company_billing_event(item: CompanyBillingEvent, project: Optional[Project] = None) -> Dict[str, Any]:
    return {
        "id": item.id,
        "project_id": item.project_id,
        "project_name": getattr(project, "name", "") if project else "",
        "project_code": getattr(project, "job_code", "") if project else "",
        "event_type": item.event_type,
        "label": item.label,
        "event_date": item.event_date,
        "amount": item.amount,
        "status": item.status,
        "note": item.note,
        "created_at": item.created_at.isoformat() if item.created_at else "",
    }


def serialize_company_purchase_order(
    item: CompanyPurchaseOrder,
    project: Optional[Project] = None,
    supplier: Optional[CompanyParty] = None,
) -> Dict[str, Any]:
    return {
        "id": item.id,
        "project_id": item.project_id,
        "project_name": getattr(project, "name", "") if project else "",
        "project_code": getattr(project, "job_code", "") if project else "",
        "supplier_party_id": item.supplier_party_id,
        "supplier_name": getattr(supplier, "name", "") if supplier else "",
        "cost_code": item.cost_code,
        "po_number": item.po_number,
        "po_date": item.po_date,
        "amount": item.amount,
        "status": item.status,
        "note": item.note,
        "created_at": item.created_at.isoformat() if item.created_at else "",
    }


def serialize_company_receipt(
    item: CompanyReceipt,
    order: Optional[CompanyPurchaseOrder] = None,
    project: Optional[Project] = None,
) -> Dict[str, Any]:
    return {
        "id": item.id,
        "purchase_order_id": item.purchase_order_id,
        "project_id": getattr(order, "project_id", 0) if order else 0,
        "project_name": getattr(project, "name", "") if project else "",
        "project_code": getattr(project, "job_code", "") if project else "",
        "po_number": getattr(order, "po_number", "") if order else "",
        "receipt_type": item.receipt_type,
        "receipt_number": item.receipt_number,
        "receipt_date": item.receipt_date,
        "amount": item.amount,
        "status": item.status,
        "note": item.note,
        "created_at": item.created_at.isoformat() if item.created_at else "",
    }


def serialize_company_procurement_review(item: CompanyProcurementReview, assigned_user: Optional[User] = None) -> Dict[str, Any]:
    return {
        "id": item.id,
        "project_id": item.project_id,
        "supplier_name": item.supplier_name,
        "match_flag": item.match_flag,
        "assigned_user_id": item.assigned_user_id,
        "assigned_username": getattr(assigned_user, "username", "") if assigned_user else "",
        "review_state": item.review_state,
        "note": item.note,
        "created_at": item.created_at.isoformat() if item.created_at else "",
        "updated_at": item.updated_at.isoformat() if item.updated_at else "",
    }


def company_ledger_rows(entries: List[JournalEntry], account_code: str) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    running_balance = 0.0
    sorted_entries = sorted(entries, key=lambda item: ((item.entry_date or ""), item.id))
    for entry in sorted_entries:
        for line in sorted(entry.lines, key=lambda item: item.id):
            if (line.account_code or "") != account_code:
                continue
            debit_value = processor.amount_to_float(line.debit) or 0.0
            credit_value = processor.amount_to_float(line.credit) or 0.0
            running_balance += debit_value - credit_value
            rows.append({
                "entry_id": entry.id,
                "document_id": entry.document_id,
                "entry_date": entry.entry_date,
                "reference": entry.reference,
                "memo": entry.memo,
                "debit": round(debit_value, 2),
                "credit": round(credit_value, 2),
                "balance": round(running_balance, 2),
                "cost_center": line.cost_center,
                "project_code": line.project_code,
                "status": entry.status,
            })
    return rows


def accounting_export_headers(preset: str) -> List[str]:
    if preset == "odoo_vendor_bills":
        return [
            "BillDate", "Reference", "Vendor", "Amount", "Currency", "Memo", "Category",
            "CostCenter", "ProjectCode", "PaymentMethod", "VatFlag", "SourceFile", "OutputFile",
        ]
    if preset == "quickbooks_expenses":
        return [
            "TxnDate", "Vendor", "RefNumber", "Amount", "Currency", "Account", "Class",
            "CustomerProject", "PaymentMethod", "Memo", "AttachmentStatus", "SourceFile",
        ]
    if preset == "sap_ap":
        return [
            "DocumentDate", "Reference", "VendorName", "Amount", "Currency", "Assignment",
            "Text", "CostCenter", "ProfitCenter", "PaymentMethod", "MatchStatus", "ReviewState", "SourceFile",
        ]
    return [
        "Project", "Date", "Kind", "DocType", "SourceFile", "Reference", "Vendor", "CanonicalVendor",
        "Amount", "Currency", "Direction", "AccountCode", "OffsetAccountCode", "Category", "Subcategory", "CostCenter", "ProjectCode",
        "PaymentMethod", "VatFlag", "MatchStatus", "ReviewState", "OutputFile",
    ]


def accounting_export_row(project: Project, document: DocumentRecord, preset: str) -> List[Any]:
    vendor = document.canonical_company_name or document.company_name
    memo = " | ".join(
        part for part in [
            document.review_note or "",
            document.match_basis or "",
        ] if part
    )
    if preset == "odoo_vendor_bills":
        return [
            document.date,
            document.number,
            vendor,
            document.amount,
            document.currency,
            memo,
            document.category,
            document.cost_center,
            document.project_code,
            document.payment_method,
            "yes" if document.vat_flag else "no",
            document.source_file,
            document.output_file,
        ]
    if preset == "quickbooks_expenses":
        account = document.category or document.doc_type or "Uncategorized Expense"
        attachment_status = "attached" if document.output_file else "missing"
        return [
            document.date,
            vendor,
            document.number,
            document.amount,
            document.currency,
            account,
            document.subcategory or document.cost_center,
            document.project_code,
            document.payment_method,
            memo or document.source_file,
            attachment_status,
            document.source_file,
        ]
    if preset == "sap_ap":
        return [
            document.date,
            document.number,
            vendor,
            document.amount,
            document.currency,
            document.project_code or document.number,
            memo or vendor,
            document.cost_center,
            document.subcategory or document.category,
            document.payment_method,
            document.match_status,
            document.review_state,
            document.source_file,
        ]
    return [
        project.project_name,
        document.date,
        document.source_type,
        document.doc_type,
        document.source_file,
        document.number,
        document.company_name,
        document.canonical_company_name,
        document.amount,
        document.currency,
        document.transaction_direction,
        document.account_code,
        document.offset_account_code,
        document.category,
        document.subcategory,
        document.cost_center,
        document.project_code,
        document.payment_method,
        "yes" if document.vat_flag else "no",
        document.match_status,
        document.review_state,
        document.output_file,
    ]


def parser_warnings_for_document(document: DocumentRecord) -> List[str]:
    warnings: List[str] = []
    if not document.date or document.date == "Unknown":
        warnings.append("date_unresolved")
    if not document.company_name or document.company_name == "Unknown":
        warnings.append("vendor_unresolved")
    if not document.amount or document.amount == "Unknown":
        warnings.append("amount_unresolved")
    if not document.number or document.number == "Unknown":
        warnings.append("reference_unresolved")
    if (document.confidence_label or "").lower() == "low":
        warnings.append("low_confidence_ocr")
    raw = (document.raw_text or "").lower()
    if document.source_type == "sheet" and (document.transaction_direction or "").strip().lower() not in {"debit", "credit"}:
        if re.search(r"\bcredit\b|\bdeposit\b|\bpayment received\b|\bdebit\b|\bpurchase\b|\bwithdrawal\b", raw):
            warnings.append("direction_inferred")
    if (document.match_status or "").strip().lower() == "missing_receipt":
        warnings.append("missing_receipt")
    return warnings


def confidence_breakdown_for_document(document: DocumentRecord) -> Dict[str, Any]:
    overall = int(document.confidence_score or 0)
    fields = {
        "date": 100 if document.date and document.date != "Unknown" else 35,
        "vendor": 100 if document.company_name and document.company_name != "Unknown" else 30,
        "amount": 100 if document.amount and document.amount != "Unknown" else 25,
        "reference": 85 if document.number and document.number != "Unknown" else 30,
        "ocr": overall,
    }
    return {
        "overall": overall,
        "label": document.confidence_label or "low",
        "fields": fields,
    }


def provenance_for_document(document: DocumentRecord) -> Dict[str, Any]:
    source_timestamp = document.source_timestamp or ""
    return {
        "source_type": document.source_type or "",
        "source_origin": document.source_origin or "",
        "source_file": document.source_file or "",
        "sheet_name": normalized_bank_name(source_timestamp) if document.source_type == "sheet" else "",
        "source_timestamp": source_timestamp,
        "processed_at": document.created_at.isoformat() if getattr(document, "created_at", None) else "",
        "review_updated_at": document.review_updated_at.isoformat() if getattr(document, "review_updated_at", None) else "",
    }


def match_factors_from_basis(basis: str) -> List[Dict[str, Any]]:
    factors: List[Dict[str, Any]] = []
    for part in re.split(r"[|;]+", basis or ""):
        cleaned = part.strip(" .")
        lowered = cleaned.lower()
        if not cleaned:
            continue
        factor: Dict[str, Any] = {"label": cleaned, "kind": "other"}
        if lowered.startswith("amount "):
            factor["kind"] = "amount"
            factor["strength"] = "strong" if "exact" in lowered else "medium" if "close" in lowered else "weak"
        elif lowered.startswith("vendor "):
            factor["kind"] = "vendor"
            score_match = re.search(r"([0-9]+(?:\.[0-9]+)?)", lowered)
            if score_match:
                score = float(score_match.group(1))
                factor["score"] = round(score, 2)
                factor["strength"] = "strong" if score >= 0.75 else "medium" if score >= 0.5 else "weak"
        elif "date" in lowered or "apart" in lowered:
            factor["kind"] = "date"
            if "same date" in lowered:
                factor["strength"] = "strong"
            elif re.search(r"\b[0-3]d apart\b", lowered):
                factor["strength"] = "medium"
            else:
                factor["strength"] = "weak"
        elif "excluded by pattern" in lowered:
            factor["kind"] = "rule"
            factor["strength"] = "strong"
        factors.append(factor)
    return factors


def explainability_for_document(document: DocumentRecord) -> Dict[str, Any]:
    status = (document.review_state or "").strip().lower()
    if not status or status == "unreviewed":
        status = (document.match_status or "").strip().lower() or "unreviewed"
    match_reasons: List[str] = []
    basis = (document.match_basis or "").strip()
    if basis:
        for part in re.split(r"[|;]+", basis):
            cleaned = part.strip(" .")
            if cleaned:
                match_reasons.append(cleaned)
    if not match_reasons and status == "missing_receipt":
        match_reasons.append("No linked supporting receipt or invoice was found.")
    if not match_reasons and status == "not_applicable":
        match_reasons.append("This record was classified as not requiring receipt support.")
    if not match_reasons and status in {"matched", "linked_to_bank"}:
        match_reasons.append("A cross-source match was found for this record.")
    return {
        "status": status,
        "match_reasons": match_reasons,
        "match_factors": match_factors_from_basis(basis),
        "review_note": (document.review_note or "").strip(),
        "parser_warnings": parser_warnings_for_document(document),
        "provenance": provenance_for_document(document),
        "confidence_breakdown": confidence_breakdown_for_document(document),
    }


def serialize_document(document: DocumentRecord) -> Dict[str, Any]:
    explainability = explainability_for_document(document)
    return {
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
        "canonical_company_name": getattr(document, "canonical_company_name", "") or "",
        "amount": document.amount,
        "currency": document.currency,
        "transaction_direction": document.transaction_direction,
        "confidence_score": document.confidence_score,
        "confidence_label": document.confidence_label,
        "match_status": document.match_status,
        "match_score": document.match_score,
        "matched_record_source_file": document.matched_record_source_file,
        "matched_record_output_file": document.matched_record_output_file,
        "matched_record_source_type": document.matched_record_source_type,
        "matched_record_source_timestamp": document.matched_record_source_timestamp,
        "matched_record_date": document.matched_record_date,
        "matched_record_number": document.matched_record_number,
        "matched_record_company_name": document.matched_record_company_name,
        "matched_record_amount": document.matched_record_amount,
        "matched_record_transaction_direction": document.matched_record_transaction_direction,
        "match_basis": document.match_basis,
        "raw_text": document.raw_text,
        "parser_warnings": explainability["parser_warnings"],
        "provenance": explainability["provenance"],
        "confidence_breakdown": explainability["confidence_breakdown"],
        "explainability": explainability,
        "review_state": getattr(document, "review_state", "unreviewed") or "unreviewed",
        "review_note": getattr(document, "review_note", "") or "",
        "review_updated_at": document.review_updated_at.isoformat() if getattr(document, "review_updated_at", None) else "",
        "assigned_user_id": getattr(document, "assigned_user_id", None),
        "category": getattr(document, "category", "") or "",
        "subcategory": getattr(document, "subcategory", "") or "",
        "account_code": getattr(document, "account_code", "") or "",
        "offset_account_code": getattr(document, "offset_account_code", "") or "",
        "cost_code": getattr(document, "cost_code", "") or "",
        "cost_center": getattr(document, "cost_center", "") or "",
        "project_code": getattr(document, "project_code", "") or "",
        "purchase_order_id": getattr(document, "purchase_order_id", None),
        "payment_method": getattr(document, "payment_method", "") or "",
        "vat_flag": bool(getattr(document, "vat_flag", False)),
    }


def serialize_project_member(member: ProjectMember, user: Optional[User]) -> Dict[str, Any]:
    return {
        "id": member.id,
        "project_id": member.project_id,
        "user_id": member.user_id,
        "username": user.username if user else "",
        "account_role": getattr(user, "role", "admin") if user else "admin",
        "project_role": member.role or "reviewer",
        "created_at": member.created_at.isoformat() if member.created_at else "",
    }


def document_query_for_project(session, project_id: int):
    return session.query(DocumentRecord).filter(DocumentRecord.project_id == project_id)


def apply_document_filters(
    query,
    *,
    search: str = "",
    source_type: str = "",
    doc_type: str = "",
    confidence_label: str = "",
    match_status: str = "",
    company: str = "",
    direction: str = "",
    bank: str = "",
    date_from: str = "",
    date_to: str = "",
    only_bank: bool = False,
):
    if only_bank:
        query = query.filter(DocumentRecord.source_type == "sheet", DocumentRecord.doc_type == "BankTransaction")
    if source_type:
        query = query.filter(DocumentRecord.source_type == source_type)
    if doc_type:
        query = query.filter(DocumentRecord.doc_type == doc_type)
    if confidence_label:
        query = query.filter(DocumentRecord.confidence_label == confidence_label)
    if match_status:
        query = query.filter(DocumentRecord.match_status == match_status)
    if company:
        company_pattern = f"%{company.strip()}%"
        query = query.filter(
            or_(
                DocumentRecord.company_name.ilike(company_pattern),
                DocumentRecord.canonical_company_name.ilike(company_pattern),
            )
        )
    if direction:
        query = query.filter(DocumentRecord.transaction_direction == direction)
    if bank:
        query = query.filter(
            or_(
                DocumentRecord.source_timestamp == bank,
                DocumentRecord.source_timestamp.like(f"{bank}:row:%"),
            )
        )
    if date_from:
        query = query.filter(DocumentRecord.date >= date_from)
    if date_to:
        query = query.filter(DocumentRecord.date <= date_to)
    if search:
        pattern = f"%{search.strip()}%"
        query = query.filter(
            or_(
                DocumentRecord.source_file.ilike(pattern),
                DocumentRecord.output_file.ilike(pattern),
                DocumentRecord.source_type.ilike(pattern),
                DocumentRecord.source_origin.ilike(pattern),
                DocumentRecord.source_timestamp.ilike(pattern),
                DocumentRecord.doc_type.ilike(pattern),
                DocumentRecord.date.ilike(pattern),
                DocumentRecord.number.ilike(pattern),
                DocumentRecord.company_name.ilike(pattern),
                DocumentRecord.canonical_company_name.ilike(pattern),
                DocumentRecord.amount.ilike(pattern),
                DocumentRecord.currency.ilike(pattern),
                DocumentRecord.match_status.ilike(pattern),
                DocumentRecord.match_basis.ilike(pattern),
                DocumentRecord.raw_text.ilike(pattern),
            )
        )
    return query


def paginate_query(query, page: int, page_size: int):
    safe_page = max(1, page)
    safe_page_size = max(1, min(page_size, 20000))
    total = query.count()
    items = (
        query
        .limit(safe_page_size)
        .offset((safe_page - 1) * safe_page_size)
        .all()
    )
    return safe_page, safe_page_size, total, items


def normalized_bank_name(source_timestamp: str) -> str:
    value = (source_timestamp or "").strip()
    if not value:
        return "Unknown"
    return value.split(":row:")[0] or "Unknown"


def normalize_company_name(value: str) -> str:
    text = (value or "").lower()
    text = re.sub(r"\b\d+\b", " ", text)
    text = re.sub(r"[_#:/\\|()[\]{}.,+\-]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def parse_iso_date(value: str) -> Optional[datetime]:
    text = (value or "").strip()
    if not text or text.lower() == "unknown":
        return None
    try:
        return datetime.strptime(text[:10], "%Y-%m-%d")
    except ValueError:
        return None


def match_company_party(name: str, parties: List[CompanyParty]) -> Optional[CompanyParty]:
    normalized = normalize_company_name(name or "")
    if not normalized:
        return None
    exact_map = {
        normalize_company_name(item.name or ""): item
        for item in parties
        if normalize_company_name(item.name or "")
    }
    if normalized in exact_map:
        return exact_map[normalized]
    for item in parties:
        party_normalized = normalize_company_name(item.name or "")
        if not party_normalized:
            continue
        if normalized in party_normalized or party_normalized in normalized:
            return item
    return None


def aging_bucket(days_overdue: int) -> str:
    if days_overdue <= 0:
        return "current"
    if days_overdue <= 30:
        return "1_30"
    if days_overdue <= 60:
        return "31_60"
    if days_overdue <= 90:
        return "61_90"
    return "over_90"


def build_company_party_aging(
    documents: List[DocumentRecord],
    parties: List[CompanyParty],
    *,
    party_type: str,
    target_allocation_totals: Optional[Dict[int, float]] = None,
) -> Dict[str, Any]:
    today = datetime.now().date()
    rows: List[Dict[str, Any]] = []
    allocation_totals = target_allocation_totals or {}
    summary = {
        "count": 0,
        "total_amount": 0.0,
        "open_amount": 0.0,
        "matched_count": 0,
        "unmatched_count": 0,
        "current": 0.0,
        "bucket_1_30": 0.0,
        "bucket_31_60": 0.0,
        "bucket_61_90": 0.0,
        "bucket_over_90": 0.0,
    }
    label = "payable" if party_type == "supplier" else "receivable"
    for document in documents:
        if (document.source_type or "").strip().lower() == "sheet":
            continue
        amount_value = processor.amount_to_float(document.amount)
        if amount_value is None or amount_value <= 0:
            continue
        party = match_company_party(document.canonical_company_name or document.company_name or "", parties)
        if party_type == "customer":
            include = bool(party)
            if not include:
                account_code = (document.account_code or "").strip()
                include = account_code.startswith("4")
        else:
            include = bool(party)
            if not include:
                account_code = (document.account_code or "").strip()
                include = account_code.startswith("5") or account_code.startswith("2")
        if not include:
            continue
        issue_date = parse_iso_date(document.date)
        terms_days = max(0, int(getattr(party, "payment_terms_days", 0) or 0))
        if issue_date:
            due_date_obj = issue_date.date().fromordinal(issue_date.date().toordinal() + terms_days)
            due_date = due_date_obj.isoformat()
            days_overdue = (today - due_date_obj).days
        else:
            due_date = ""
            days_overdue = 0
        match_status = (document.match_status or "").strip().lower()
        review_state = (document.review_state or "").strip().lower()
        allocated_amount = min(amount_value, round(allocation_totals.get(document.id, 0.0), 2))
        is_settled = match_status in {"matched", "linked_to_bank"} or review_state == "reviewed"
        outstanding_amount = 0.0 if is_settled else max(0.0, round(amount_value - allocated_amount, 2))
        bucket = aging_bucket(days_overdue)
        summary["count"] += 1
        summary["total_amount"] += amount_value
        summary["open_amount"] += outstanding_amount
        if party:
            summary["matched_count"] += 1
        else:
            summary["unmatched_count"] += 1
        if outstanding_amount > 0:
            if bucket == "current":
                summary["current"] += outstanding_amount
            elif bucket == "1_30":
                summary["bucket_1_30"] += outstanding_amount
            elif bucket == "31_60":
                summary["bucket_31_60"] += outstanding_amount
            elif bucket == "61_90":
                summary["bucket_61_90"] += outstanding_amount
            else:
                summary["bucket_over_90"] += outstanding_amount
        rows.append({
            "id": document.id,
            "document_id": document.id,
            "kind": label,
            "date": document.date or "",
            "due_date": due_date,
            "days_overdue": max(days_overdue, 0) if outstanding_amount > 0 else 0,
            "source_file": document.source_file or "",
            "output_file": document.output_file or "",
            "doc_type": document.doc_type or "",
            "company_name": document.canonical_company_name or document.company_name or "Unknown",
            "party_name": party.name if party else "",
            "party_id": party.id if party else None,
            "amount": amount_value,
            "allocated_amount": allocated_amount,
            "outstanding_amount": outstanding_amount,
            "status": "settled" if is_settled else ("open" if outstanding_amount > 0 else "closed"),
            "aging_bucket": bucket,
            "project_code": document.project_code or "",
            "purchase_order_id": getattr(document, "purchase_order_id", None),
            "cost_center": document.cost_center or "",
            "account_code": document.account_code or "",
            "default_party_account_code": getattr(party, "default_account_code", "") or "",
        })
    rows.sort(
        key=lambda item: (
            {"open": 0, "settled": 1, "closed": 2}.get(item["status"], 3),
            -(item["days_overdue"] or 0),
            -(item["outstanding_amount"] or 0.0),
            item["company_name"] or "",
        )
    )
    top_parties: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        key = row["party_name"] or row["company_name"] or "Unknown"
        bucket = top_parties.setdefault(key, {"party_name": key, "count": 0, "open_amount": 0.0, "total_amount": 0.0})
        bucket["count"] += 1
        bucket["open_amount"] += row["outstanding_amount"] or 0.0
        bucket["total_amount"] += row["amount"] or 0.0
    ranked_parties = sorted(top_parties.values(), key=lambda item: (-(item["open_amount"] or 0.0), -(item["total_amount"] or 0.0), item["party_name"]))[:8]
    return {"summary": summary, "rows": rows[:25], "all_rows": rows, "top_parties": ranked_parties}


def build_company_procurement_summary(
    projects: List[Project],
    purchase_orders: List[CompanyPurchaseOrder],
    receipts: List[CompanyReceipt],
    ap_rows: List[Dict[str, Any]],
    suppliers: List[CompanyParty],
) -> Dict[str, Any]:
    project_map = {project.id: project for project in projects}
    supplier_map = {party.id: party for party in suppliers}
    buckets: Dict[str, Dict[str, Any]] = {}

    def ensure_bucket(project_id: int, supplier_party_id: int | None) -> Dict[str, Any]:
        project = project_map.get(project_id)
        supplier = supplier_map.get(supplier_party_id) if supplier_party_id else None
        key = f"{project_id}:{supplier_party_id or 0}"
        return buckets.setdefault(key, {
            "project_id": project_id,
            "project_name": getattr(project, "name", "") or "",
            "project_code": getattr(project, "job_code", "") or "",
            "supplier_party_id": supplier_party_id,
            "supplier_name": getattr(supplier, "name", "") or "Unknown",
            "po_count": 0,
            "receipt_count": 0,
            "bill_count": 0,
            "committed_amount": 0.0,
            "received_amount": 0.0,
            "billed_amount": 0.0,
            "paid_amount": 0.0,
            "open_po_amount": 0.0,
            "not_received_amount": 0.0,
            "received_not_billed_amount": 0.0,
            "billed_not_paid_amount": 0.0,
        })

    for order in purchase_orders:
        status = (order.status or "").strip().lower()
        if status == "cancelled":
            continue
        bucket = ensure_bucket(int(order.project_id), order.supplier_party_id)
        amount_value = processor.amount_to_float(order.amount) or 0.0
        bucket["po_count"] += 1
        bucket["committed_amount"] += amount_value

    po_map = {order.id: order for order in purchase_orders}
    for receipt in receipts:
        order = po_map.get(int(receipt.purchase_order_id))
        if not order:
            continue
        status = (receipt.status or "").strip().lower()
        if status == "cancelled":
            continue
        bucket = ensure_bucket(int(order.project_id), order.supplier_party_id)
        amount_value = processor.amount_to_float(receipt.amount) or 0.0
        bucket["receipt_count"] += 1
        bucket["received_amount"] += amount_value

    project_code_to_id = {
        (getattr(project, "job_code", "") or "").strip(): int(project.id)
        for project in projects
        if (getattr(project, "job_code", "") or "").strip()
    }
    po_map = {int(order.id): order for order in purchase_orders}
    for row in ap_rows:
        linked_po = po_map.get(int(row.get("purchase_order_id") or 0)) if row.get("purchase_order_id") else None
        project_id = int(getattr(linked_po, "project_id", 0) or 0) or project_code_to_id.get((row.get("project_code") or "").strip())
        party_id = getattr(linked_po, "supplier_party_id", None) if linked_po else row.get("party_id")
        if not project_id:
            continue
        bucket = ensure_bucket(project_id, int(party_id) if party_id else None)
        bucket["bill_count"] += 1
        bucket["billed_amount"] += float(row.get("amount") or 0.0)
        bucket["paid_amount"] += float(row.get("allocated_amount") or 0.0)
        bucket["billed_not_paid_amount"] += float(row.get("outstanding_amount") or 0.0)

    rows = []
    for bucket in buckets.values():
        committed_amount = round(bucket["committed_amount"], 2)
        received_amount = round(bucket["received_amount"], 2)
        billed_amount = round(bucket["billed_amount"], 2)
        paid_amount = round(bucket["paid_amount"], 2)
        billed_not_paid_amount = round(bucket["billed_not_paid_amount"], 2)
        open_po_amount = round(max(committed_amount - billed_amount, 0.0), 2)
        not_received_amount = round(max(committed_amount - received_amount, 0.0), 2)
        received_not_billed_amount = round(max(received_amount - billed_amount, 0.0), 2)
        po_overrun_amount = round(max(billed_amount - committed_amount, 0.0), 2)
        billed_before_received_amount = round(max(billed_amount - received_amount, 0.0), 2)
        if po_overrun_amount > 0.01:
            match_flag = "po_overrun"
        elif billed_before_received_amount > 0.01:
            match_flag = "billed_before_received"
        elif billed_not_paid_amount > 0.01:
            match_flag = "billed_not_paid"
        elif received_not_billed_amount > 0.01:
            match_flag = "received_not_billed"
        elif not_received_amount > 0.01:
            match_flag = "partial_receipt"
        else:
            match_flag = "aligned"
        rows.append({
            **bucket,
            "committed_amount": committed_amount,
            "received_amount": received_amount,
            "billed_amount": billed_amount,
            "paid_amount": paid_amount,
            "open_po_amount": open_po_amount,
            "not_received_amount": not_received_amount,
            "received_not_billed_amount": received_not_billed_amount,
            "billed_not_paid_amount": billed_not_paid_amount,
            "po_overrun_amount": po_overrun_amount,
            "billed_before_received_amount": billed_before_received_amount,
            "match_flag": match_flag,
        })
    rows.sort(key=lambda item: (-(item["not_received_amount"] or 0.0), -(item["billed_not_paid_amount"] or 0.0), item["project_code"], item["supplier_name"]))
    return {
        "summary": {
            "rows": len(rows),
            "committed_amount": round(sum(item["committed_amount"] for item in rows), 2),
            "received_amount": round(sum(item["received_amount"] for item in rows), 2),
            "billed_amount": round(sum(item["billed_amount"] for item in rows), 2),
            "paid_amount": round(sum(item["paid_amount"] for item in rows), 2),
            "open_po_amount": round(sum(item["open_po_amount"] for item in rows), 2),
            "not_received_amount": round(sum(item["not_received_amount"] for item in rows), 2),
            "received_not_billed_amount": round(sum(item["received_not_billed_amount"] for item in rows), 2),
            "billed_not_paid_amount": round(sum(item["billed_not_paid_amount"] for item in rows), 2),
            "po_overrun_amount": round(sum(item["po_overrun_amount"] for item in rows), 2),
            "billed_before_received_amount": round(sum(item["billed_before_received_amount"] for item in rows), 2),
        },
        "rows": rows[:20],
        "all_rows": rows,
    }


def build_company_procurement_exceptions(
    procurement_rows: List[Dict[str, Any]],
    reviews: Optional[List[CompanyProcurementReview]] = None,
    users_by_id: Optional[Dict[int, User]] = None,
    *,
    review_state_filter: str = "",
    assigned_user_id: int | None = None,
) -> Dict[str, Any]:
    flagged = [row for row in procurement_rows if (row.get("match_flag") or "aligned") != "aligned"]
    review_lookup = {
        (
            int(item.project_id),
            (item.supplier_name or "").strip().lower(),
            (item.match_flag or "").strip().lower(),
        ): item
        for item in (reviews or [])
    }
    counts = {
        "total": len(flagged),
        "po_overrun": 0,
        "billed_before_received": 0,
        "billed_not_paid": 0,
        "received_not_billed": 0,
        "partial_receipt": 0,
        "open": 0,
        "reviewed": 0,
        "ignored": 0,
    }
    for row in flagged:
        flag = row.get("match_flag") or ""
        if flag in counts:
            counts[flag] += 1
        review = review_lookup.get((
            int(row.get("project_id") or 0),
            (row.get("supplier_name") or "").strip().lower(),
            (flag or "").strip().lower(),
        ))
        if review:
            assigned_user = (users_by_id or {}).get(int(review.assigned_user_id or 0))
            row["review"] = serialize_company_procurement_review(review, assigned_user)
        else:
            row["review"] = {
                "assigned_user_id": None,
                "assigned_username": "",
                "review_state": "open",
                "note": "",
            }
        review_state = (row["review"].get("review_state") or "open").strip().lower()
        if review_state in counts:
            counts[review_state] += 1
    filtered = []
    for row in flagged:
        review_state = (row.get("review", {}).get("review_state") or "open").strip().lower()
        if review_state_filter and review_state != review_state_filter:
            continue
        if assigned_user_id and int(row.get("review", {}).get("assigned_user_id") or 0) != int(assigned_user_id):
            continue
        filtered.append(row)
    filtered.sort(key=lambda item: (
        {"po_overrun": 0, "billed_before_received": 1, "billed_not_paid": 2, "received_not_billed": 3, "partial_receipt": 4}.get(item.get("match_flag"), 9),
        -(item.get("po_overrun_amount") or 0.0),
        -(item.get("billed_before_received_amount") or 0.0),
        -(item.get("billed_not_paid_amount") or 0.0),
        -(item.get("not_received_amount") or 0.0),
    ))
    return {"summary": counts, "rows": filtered[:20]}


def company_allocation_totals(
    allocations: List[CompanyAllocation],
    *,
    field_name: str,
) -> Dict[int, float]:
    totals: Dict[int, float] = {}
    for item in allocations:
        key = getattr(item, field_name, None)
        if not key:
            continue
        totals[int(key)] = round(totals.get(int(key), 0.0) + (processor.amount_to_float(item.amount) or 0.0), 2)
    return totals


def build_company_allocation_workspace(
    documents: List[DocumentRecord],
    parties: List[CompanyParty],
    allocations: List[CompanyAllocation],
    *,
    allocation_type: str,
) -> Dict[str, Any]:
    if allocation_type == "receivable":
        target_rows = build_company_party_aging(
            documents,
            parties,
            party_type="customer",
            target_allocation_totals=company_allocation_totals(allocations, field_name="target_document_id"),
        )["rows"]
        payment_rows = []
        allocated_payment_totals = company_allocation_totals(allocations, field_name="payment_document_id")
        for document in documents:
            if (document.source_type or "").strip().lower() != "sheet":
                continue
            if inferred_transaction_direction(document) != "credit":
                continue
            amount_value = processor.amount_to_float(document.amount) or 0.0
            if amount_value <= 0:
                continue
            allocated_amount = min(amount_value, round(allocated_payment_totals.get(document.id, 0.0), 2))
            remaining_amount = max(0.0, round(amount_value - allocated_amount, 2))
            if remaining_amount <= 0:
                continue
            payment_rows.append({
                "id": document.id,
                "date": document.date or "",
                "company_name": document.canonical_company_name or document.company_name or "Unknown",
                "amount": amount_value,
                "allocated_amount": allocated_amount,
                "remaining_amount": remaining_amount,
                "source_file": document.source_file or "",
            })
    else:
        target_rows = build_company_party_aging(
            documents,
            parties,
            party_type="supplier",
            target_allocation_totals=company_allocation_totals(allocations, field_name="target_document_id"),
        )["rows"]
        payment_rows = []
        allocated_payment_totals = company_allocation_totals(allocations, field_name="payment_document_id")
        for document in documents:
            if (document.source_type or "").strip().lower() != "sheet":
                continue
            if inferred_transaction_direction(document) != "debit":
                continue
            amount_value = processor.amount_to_float(document.amount) or 0.0
            if amount_value <= 0:
                continue
            allocated_amount = min(amount_value, round(allocated_payment_totals.get(document.id, 0.0), 2))
            remaining_amount = max(0.0, round(amount_value - allocated_amount, 2))
            if remaining_amount <= 0:
                continue
            payment_rows.append({
                "id": document.id,
                "date": document.date or "",
                "company_name": document.canonical_company_name or document.company_name or "Unknown",
                "amount": amount_value,
                "allocated_amount": allocated_amount,
                "remaining_amount": remaining_amount,
                "source_file": document.source_file or "",
            })
    open_targets = [item for item in target_rows if (item.get("outstanding_amount") or 0) > 0][:40]
    payment_rows.sort(key=lambda item: (-(item["remaining_amount"] or 0.0), item["date"] or "", item["id"]))
    target_lookup = {item["document_id"]: item for item in target_rows}
    payment_lookup = {item["id"]: item for item in payment_rows}
    serialized_allocations = []
    for item in sorted(allocations, key=lambda alloc: (alloc.created_at or datetime.min), reverse=True):
        payment = payment_lookup.get(item.payment_document_id)
        target = target_lookup.get(item.target_document_id)
        serialized = serialize_company_allocation(item)
        serialized["payment_label"] = (payment or {}).get("company_name") or ""
        serialized["target_label"] = (target or {}).get("party_name") or (target or {}).get("company_name") or ""
        serialized["payment_date"] = (payment or {}).get("date") or ""
        serialized["target_date"] = (target or {}).get("date") or ""
        serialized_allocations.append(serialized)
    return {
        "targets": open_targets,
        "payments": payment_rows[:40],
        "allocations": serialized_allocations[:40],
    }


def build_company_job_costing_summary(
    projects: List[Project],
    documents: List[DocumentRecord],
    billing_events: Optional[List[CompanyBillingEvent]] = None,
    purchase_orders: Optional[List[CompanyPurchaseOrder]] = None,
) -> Dict[str, Any]:
    buckets: Dict[str, Dict[str, Any]] = {}
    project_map = {
        (getattr(project, "job_code", "") or "").strip(): project
        for project in projects
        if (getattr(project, "job_code", "") or "").strip()
    }
    billing_events = billing_events or []
    purchase_orders = purchase_orders or []
    project_event_map: Dict[int, List[CompanyBillingEvent]] = {}
    for event in billing_events:
        project_event_map.setdefault(int(event.project_id), []).append(event)
    project_po_map: Dict[int, List[CompanyPurchaseOrder]] = {}
    for order in purchase_orders:
        project_po_map.setdefault(int(order.project_id), []).append(order)
    for document in documents:
        project_code = (getattr(document, "project_code", "") or "").strip()
        if not project_code:
            continue
        bucket = buckets.setdefault(project_code, {
            "project_code": project_code,
            "project_name": "",
            "client_name": "",
            "site_name": "",
            "contract_number": "",
            "status": "active",
            "budget_amount": 0.0,
            "contract_value": 0.0,
            "variation_amount": 0.0,
            "contract_total": 0.0,
            "billed_to_date": 0.0,
            "certified_progress_pct": 0.0,
            "retention_percent": 0.0,
            "advance_received": 0.0,
            "actual_cost": 0.0,
            "actual_revenue": 0.0,
            "cost_codes": {},
            "document_count": 0,
        })
        project = project_map.get(project_code)
        if project:
            bucket["project_name"] = project.name or bucket["project_name"]
            bucket["client_name"] = getattr(project, "client_name", "") or bucket["client_name"]
            bucket["site_name"] = getattr(project, "site_name", "") or bucket["site_name"]
            bucket["contract_number"] = getattr(project, "contract_number", "") or bucket["contract_number"]
            bucket["status"] = getattr(project, "project_status", "active") or bucket["status"]
            bucket["budget_amount"] = processor.amount_to_float(getattr(project, "budget_amount", "")) or bucket["budget_amount"]
            bucket["contract_value"] = processor.amount_to_float(getattr(project, "contract_value", "")) or bucket["contract_value"]
            bucket["variation_amount"] = processor.amount_to_float(getattr(project, "variation_amount", "")) or bucket["variation_amount"]
            bucket["billed_to_date"] = processor.amount_to_float(getattr(project, "billed_to_date", "")) or bucket["billed_to_date"]
            bucket["certified_progress_pct"] = processor.amount_to_float(getattr(project, "certified_progress_pct", "")) or bucket["certified_progress_pct"]
            bucket["retention_percent"] = processor.amount_to_float(getattr(project, "retention_percent", "")) or bucket["retention_percent"]
            bucket["advance_received"] = processor.amount_to_float(getattr(project, "advance_received", "")) or bucket["advance_received"]
        amount_value = processor.amount_to_float(document.amount) or 0.0
        if amount_value <= 0:
            continue
        account_code = (getattr(document, "account_code", "") or "").strip()
        if account_code.startswith("4"):
            bucket["actual_revenue"] += amount_value
        else:
            direction = inferred_transaction_direction(document)
            if account_code.startswith("5") or direction == "debit":
                bucket["actual_cost"] += amount_value
        cost_code = (getattr(document, "cost_code", "") or "").strip() or "Uncoded"
        code_bucket = bucket["cost_codes"].setdefault(cost_code, 0.0)
        if not account_code.startswith("4"):
            bucket["cost_codes"][cost_code] = code_bucket + amount_value
        bucket["document_count"] += 1
    rows = []
    for item in buckets.values():
        project = project_map.get(item["project_code"])
        project_events = project_event_map.get(int(getattr(project, "id", 0) or 0), []) if project else []
        project_orders = project_po_map.get(int(getattr(project, "id", 0) or 0), []) if project else []
        posted_statuses = {"certified", "billed", "collected"}
        committed_statuses = {"draft", "open", "approved", "partially_received"}
        variation_from_events = round(sum(
            processor.amount_to_float(event.amount) or 0.0
            for event in project_events
            if (event.event_type or "").strip().lower() == "variation" and (event.status or "").strip().lower() in posted_statuses
        ), 2)
        billed_from_events = round(sum(
            (processor.amount_to_float(event.amount) or 0.0) * (
                -1.0 if (event.event_type or "").strip().lower() == "credit_note" else 1.0
            )
            for event in project_events
            if (event.status or "").strip().lower() in posted_statuses
            and (event.event_type or "").strip().lower() in {"progress_claim", "milestone", "variation", "retention_invoice", "debit_note", "credit_note"}
        ), 2)
        item["variation_amount"] = variation_from_events or item["variation_amount"]
        item["billed_to_date"] = billed_from_events or item["billed_to_date"]
        committed_cost = round(sum(
            processor.amount_to_float(order.amount) or 0.0
            for order in project_orders
            if (order.status or "").strip().lower() in committed_statuses
        ), 2)
        contract_total = round((item["contract_value"] or 0.0) + (item["variation_amount"] or 0.0), 2)
        certified_progress_pct = max(0.0, min(100.0, item["certified_progress_pct"] or 0.0))
        earned_revenue = round(contract_total * (certified_progress_pct / 100.0), 2) if contract_total else round(item["actual_revenue"] or 0.0, 2)
        billed_to_date = round(item["billed_to_date"] or 0.0, 2)
        unbilled_wip = round(max(earned_revenue - billed_to_date, 0.0), 2)
        overbilled = round(max(billed_to_date - earned_revenue, 0.0), 2)
        retention_amount = round(billed_to_date * ((item["retention_percent"] or 0.0) / 100.0), 2) if billed_to_date else 0.0
        gross_margin = round((item["actual_revenue"] or 0.0) - (item["actual_cost"] or 0.0), 2)
        earned_margin = round(earned_revenue - (item["actual_cost"] or 0.0), 2)
        budget = item["budget_amount"] or 0.0
        variance = round(budget - (item["actual_cost"] or 0.0), 2) if budget else 0.0
        cost_to_complete = round(max(budget - (item["actual_cost"] or 0.0), 0.0), 2) if budget else 0.0
        committed_variance = round(committed_cost - (item["actual_cost"] or 0.0), 2)
        if unbilled_wip > 0.01:
            billing_status = "underbilled"
        elif overbilled > 0.01:
            billing_status = "overbilled"
        else:
            billing_status = "aligned"
        top_cost_codes = sorted(
            [{"cost_code": key, "amount": value} for key, value in item["cost_codes"].items()],
            key=lambda row: (-(row["amount"] or 0.0), row["cost_code"]),
        )[:5]
        rows.append({
            **item,
            "contract_total": contract_total,
            "earned_revenue": earned_revenue,
            "certified_progress_pct": round(certified_progress_pct, 2),
            "billed_to_date": billed_to_date,
            "unbilled_wip": unbilled_wip,
            "overbilled_amount": overbilled,
            "retention_amount": retention_amount,
            "earned_margin": earned_margin,
            "actual_cost": round(item["actual_cost"], 2),
            "actual_revenue": round(item["actual_revenue"], 2),
            "gross_margin": gross_margin,
            "budget_variance": variance,
            "cost_to_complete": cost_to_complete,
            "committed_cost": committed_cost,
            "committed_variance": committed_variance,
            "billing_status": billing_status,
            "billing_event_count": len(project_events),
            "purchase_order_count": len(project_orders),
            "top_cost_codes": top_cost_codes,
        })
    rows.sort(key=lambda item: (-(item["unbilled_wip"] or 0.0), -(item["actual_cost"] or 0.0), item["project_code"]))
    return {
        "rows": rows,
        "summary": {
            "projects": len(rows),
            "budget_total": round(sum(item["budget_amount"] or 0.0 for item in rows), 2),
            "contract_total": round(sum(item["contract_total"] or 0.0 for item in rows), 2),
            "actual_cost_total": round(sum(item["actual_cost"] or 0.0 for item in rows), 2),
            "committed_cost_total": round(sum(item["committed_cost"] or 0.0 for item in rows), 2),
            "actual_revenue_total": round(sum(item["actual_revenue"] or 0.0 for item in rows), 2),
            "earned_revenue_total": round(sum(item["earned_revenue"] or 0.0 for item in rows), 2),
            "billed_to_date_total": round(sum(item["billed_to_date"] or 0.0 for item in rows), 2),
            "unbilled_wip_total": round(sum(item["unbilled_wip"] or 0.0 for item in rows), 2),
            "overbilled_total": round(sum(item["overbilled_amount"] or 0.0 for item in rows), 2),
            "retention_total": round(sum(item["retention_amount"] or 0.0 for item in rows), 2),
            "gross_margin_total": round(sum(item["gross_margin"] or 0.0 for item in rows), 2),
        },
    }


def canonical_company_name(document: DocumentRecord, vendor_alias_map: Dict[str, str]) -> str:
    normalized = normalize_company_name(document.company_name or "")
    alias = vendor_alias_map.get(normalized, "")
    return alias or (document.canonical_company_name or document.company_name or "Unknown")


def matching_rule_meta(document: DocumentRecord, rules: List[ProjectRule]) -> Dict[str, str]:
    haystack = " ".join(
        [
            document.company_name or "",
            document.raw_text or "",
            document.number or "",
            document.source_file or "",
        ]
    ).lower()
    for rule in rules:
        keyword = (rule.keyword or "").strip().lower()
        if not keyword:
            continue
        if rule.source_type and rule.source_type != document.source_type:
            continue
        if keyword in haystack:
            return {
                "status": rule.status or "",
                "category": rule.category or "",
                "subcategory": rule.subcategory or "",
                "account_code": getattr(rule, "account_code", "") or "",
                "offset_account_code": getattr(rule, "offset_account_code", "") or "",
                "project_code": getattr(rule, "project_code", "") or "",
                "cost_code": getattr(rule, "cost_code", "") or "",
                "cost_center": getattr(rule, "cost_center", "") or "",
                "payment_method": getattr(rule, "payment_method", "") or "",
                "vat_flag": "1" if bool(getattr(rule, "vat_flag", False)) else "",
                "auto_post": "1" if bool(getattr(rule, "auto_post", True)) else "",
                "keyword": rule.keyword or "",
            }
    return {
        "status": "",
        "category": "",
        "subcategory": "",
        "account_code": "",
        "offset_account_code": "",
        "project_code": "",
        "cost_code": "",
        "cost_center": "",
        "payment_method": "",
        "vat_flag": "",
        "auto_post": "",
        "keyword": "",
    }


def normalized_match_status(document: DocumentRecord, rules: List[ProjectRule]) -> str:
    rule_status = matching_rule_meta(document, rules)["status"]
    if rule_status:
        return rule_status
    status = (document.match_status or "").strip().lower()
    if status == "linked_to_bank":
        return "matched"
    return status or "unreviewed"


def inferred_transaction_direction(document: DocumentRecord) -> str:
    direct = (document.transaction_direction or "").strip().lower()
    if direct in {"debit", "credit"}:
        return direct
    raw = (document.raw_text or "").lower()
    name = (document.company_name or "").lower()
    combined = f"{raw} {name}"
    if re.search(r"\bpayment received\b|\bcredit\b|\bdeposit\b|\btop up\b|\bprofit credit\b|\bfrom\b", combined) and not re.search(r"\bdebit transaction\b", combined):
        return "credit"
    if re.search(r"\bdebit\b|\bdebit transaction\b|\bpurchase\b|\btransfer\b|\bwithdrawal\b|\batm wdl\b|\bfee\b|\bcharges?\b|\bto\b", combined):
        return "debit"
    return "unknown"


def record_tag_meta(document: DocumentRecord, rules: List[ProjectRule]) -> Dict[str, str]:
    rule_meta = matching_rule_meta(document, rules)
    category = document.category or rule_meta["category"] or ""
    subcategory = document.subcategory or rule_meta["subcategory"] or ""
    return {
        "category": category,
        "subcategory": subcategory,
        "account_code": document.account_code or rule_meta["account_code"] or "",
        "offset_account_code": document.offset_account_code or rule_meta["offset_account_code"] or "",
        "project_code": document.project_code or rule_meta["project_code"] or "",
        "cost_code": document.cost_code or rule_meta["cost_code"] or "",
        "cost_center": document.cost_center or rule_meta["cost_center"] or "",
        "payment_method": document.payment_method or rule_meta["payment_method"] or "",
        "vat_flag": "1" if (document.vat_flag or rule_meta["vat_flag"]) else "",
        "rule_keyword": rule_meta["keyword"] or "",
        "auto_post": rule_meta["auto_post"] or "",
    }


def bank_dashboard_record(document: DocumentRecord, rules: List[ProjectRule], vendor_alias_map: Dict[str, str]) -> Dict[str, Any]:
    payload = serialize_document(document)
    payload["bank_name"] = normalized_bank_name(document.source_timestamp or "")
    payload["dashboard_match_status"] = normalized_match_status(document, rules)
    payload["resolved_direction"] = inferred_transaction_direction(document)
    payload["canonical_vendor_name"] = canonical_company_name(document, vendor_alias_map)
    tags = record_tag_meta(document, rules)
    payload["resolved_category"] = tags["category"]
    payload["resolved_subcategory"] = tags["subcategory"]
    return payload


def dashboard_category_key(item: Dict[str, Any]) -> str:
    category = item.get("resolved_category") or "Uncategorized"
    subcategory = item.get("resolved_subcategory") or ""
    return f"{category} / {subcategory}" if subcategory else category


def effective_reconciliation_status(document: DocumentRecord, rules: List[ProjectRule]) -> str:
    review_state = (getattr(document, "review_state", "") or "").strip().lower()
    if review_state and review_state != "unreviewed":
        return review_state
    return normalized_match_status(document, rules)


def reconciliation_priority(status: str) -> int:
    if status == "missing_receipt":
        return 0
    if status == "matched":
        return 1
    if status == "not_applicable":
        return 2
    if status == "reviewed":
        return 3
    return 4


def build_review_issues(
    documents: List[DocumentRecord],
    rules: List[ProjectRule],
    vendor_alias_map: Dict[str, str],
) -> List[Dict[str, Any]]:
    issues: List[Dict[str, Any]] = []
    seen: Dict[str, List[DocumentRecord]] = {}
    repeated: Dict[str, List[DocumentRecord]] = {}
    split_candidates: Dict[str, List[DocumentRecord]] = {}

    def issue_payload(document: DocumentRecord, *, key: str, issue_type: str, label: str, reason: str) -> Dict[str, Any]:
        return {
            "key": key,
            "type": issue_type,
            "label": label,
            "reason": reason,
            "source_type": document.source_type or "-",
            "source_file": document.source_file or "-",
            "company_name": canonical_company_name(document, vendor_alias_map) or "-",
            "amount": document.amount or "-",
            "record_id": document.id,
        }

    for document in documents:
        status = normalized_match_status(document, rules)
        direction = inferred_transaction_direction(document)
        normalized_vendor = normalize_company_name(document.company_name or "")
        if document.confidence_label == "low":
            issues.append(issue_payload(
                document,
                key=f"low-{document.id}",
                issue_type="low_confidence",
                label="Low Confidence",
                reason=f"Confidence score {document.confidence_score or 0} on {document.doc_type or 'Unknown'}.",
            ))
        if not document.date or document.date == "Unknown" or not document.amount or document.amount == "Unknown" or not document.company_name or document.company_name == "Unknown":
            issues.append(issue_payload(
                document,
                key=f"parse-{document.id}",
                issue_type="parsing_issue",
                label="Parsing Issue",
                reason="One or more key extracted fields are missing or unresolved.",
            ))
        if document.source_type == "sheet" and document.doc_type == "BankTransaction" and status == "missing_receipt":
            issues.append(issue_payload(
                document,
                key=f"missing-{document.id}",
                issue_type="missing_receipt",
                label="Missing Receipt",
                reason="Debit bank transaction still has no linked supporting receipt or invoice.",
            ))
        dup_key = "||".join([document.source_type or "", normalized_vendor, document.date or "", str(document.amount or "")])
        repeated_key = "||".join([normalized_vendor, str(document.amount or "")])
        split_key = "||".join([normalized_vendor, document.date or ""])
        if normalized_vendor and document.date and document.amount:
            seen.setdefault(dup_key, []).append(document)
        if normalized_vendor and document.amount:
            repeated.setdefault(repeated_key, []).append(document)
        if document.source_type == "sheet" and document.doc_type == "BankTransaction" and normalized_vendor and document.date:
            split_candidates.setdefault(split_key, []).append(document)
        raw = f"{document.company_name or ''} {document.raw_text or ''} {document.number or ''}".lower()
        if re.search(r"\brefund\b|\breversal\b|\breversed\b|\bchargeback\b", raw):
            issues.append(issue_payload(
                document,
                key=f"refund-{document.id}",
                issue_type="refund_or_reversal",
                label="Refund / Reversal",
                reason="Record text suggests a refund, reversal, or chargeback that should be reviewed against original spending.",
            ))
        if document.source_type == "sheet" and document.doc_type == "BankTransaction" and direction == "credit" and status == "missing_receipt":
            issues.append(issue_payload(
                document,
                key=f"credit-misclassified-{document.id}",
                issue_type="credit_needs_review",
                label="Credit Needs Review",
                reason="Credit transaction is still marked unresolved and may be misclassified or need special handling.",
            ))
        matched_amount = processor.amount_to_float(document.matched_record_amount) or 0.0
        current_amount = processor.amount_to_float(document.amount) or 0.0
        if status == "matched" and document.matched_record_amount and abs(current_amount - matched_amount) > 0.01:
            issues.append(issue_payload(
                document,
                key=f"mismatch-{document.id}",
                issue_type="amount_mismatch",
                label="Amount Mismatch",
                reason=f"Matched record amount {document.matched_record_amount} differs from row amount {document.amount}.",
            ))

    for key, items in seen.items():
        if len(items) > 1:
            for document in items:
                issues.append(issue_payload(
                    document,
                    key=f"dup-{key}-{document.id}",
                    issue_type="duplicate_suspect",
                    label="Duplicate Suspect",
                    reason=f"{len(items)} records share the same normalized vendor, date, and amount.",
                ))

    for key, items in repeated.items():
        dated = [item for item in items if item.date and item.date != "Unknown"]
        if len(dated) < 2:
            continue
        sorted_items = sorted(dated, key=lambda item: str(item.date or ""))
        for index in range(1, len(sorted_items)):
            previous = sorted_items[index - 1]
            current = sorted_items[index]
            if previous.date == current.date:
                continue
            issues.append(issue_payload(
                current,
                key=f"repeat-{key}-{current.id}",
                issue_type="repeated_charge",
                label="Repeated Charge",
                reason=f"Same normalized vendor and amount appeared again on {current.date}; check for subscription, installment, or duplicate charge.",
            ))

    for items in split_candidates.values():
        debit_items = [item for item in items if inferred_transaction_direction(item) == "debit"]
        if len(debit_items) < 2:
            continue
        total = sum(processor.amount_to_float(item.amount) or 0.0 for item in debit_items)
        for document in debit_items:
            issues.append(issue_payload(
                document,
                key=f"split-{document.id}",
                issue_type="split_payment_candidate",
                label="Split Payment Candidate",
                reason=f"{len(debit_items)} debit rows for the same vendor/date sum to {total:.2f} AED.",
            ))
    return issues


def build_project_resources(documents: List[DocumentRecord]) -> List[Dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = {}
    for document in documents:
        key = build_resource_key(document)
        bucket = grouped.setdefault(
            key,
            {
                "key": key,
                "source_type": document.source_type or "",
                "source_path": document.source_path or "",
                "source_file": document.source_file or "",
                "source_origin": document.source_origin or "",
                "record_count": 0,
                "output_count": 0,
                "debit_total": 0.0,
                "credit_total": 0.0,
                "date_from": "",
                "date_to": "",
                "last_processed_at": "",
                "low_confidence_count": 0,
                "missing_receipt_count": 0,
                "parsing_warnings": 0,
                "matched_count": 0,
                "records": [],
            },
        )
        bucket["record_count"] += 1
        created_at = document.created_at.isoformat() if document.created_at else ""
        if created_at and (not bucket["last_processed_at"] or created_at > bucket["last_processed_at"]):
            bucket["last_processed_at"] = created_at
        if document.output_path:
            bucket["output_count"] += 1
        amount_value = processor.amount_to_float(document.amount)
        if amount_value is not None:
            if document.transaction_direction == "credit":
                bucket["credit_total"] += amount_value
            else:
                bucket["debit_total"] += amount_value
        if document.confidence_label == "low":
            bucket["low_confidence_count"] += 1
        if (document.match_status or "").strip().lower() == "missing_receipt":
            bucket["missing_receipt_count"] += 1
        if not document.date or document.date == "Unknown" or not document.company_name or document.company_name == "Unknown" or not document.amount or document.amount == "Unknown":
            bucket["parsing_warnings"] += 1
        if (document.match_status or "").strip().lower() in {"matched", "linked_to_bank"}:
            bucket["matched_count"] += 1
        if document.date and document.date != "Unknown":
            if not bucket["date_from"] or document.date < bucket["date_from"]:
                bucket["date_from"] = document.date
            if not bucket["date_to"] or document.date > bucket["date_to"]:
                bucket["date_to"] = document.date
        bucket["records"].append(serialize_document(document))
    resource_items = list(grouped.values())
    for item in resource_items:
        record_count = max(1, int(item["record_count"]))
        penalty = (
            (int(item["low_confidence_count"]) * 20)
            + (int(item["missing_receipt_count"]) * 8)
            + (int(item["parsing_warnings"]) * 10)
        ) / record_count
        quality_score = max(0, round(100 - penalty))
        if quality_score >= 85 and int(item["parsing_warnings"]) == 0 and int(item["low_confidence_count"]) == 0:
            status = "healthy"
        elif quality_score >= 60:
            status = "warning"
        else:
            status = "attention"
        item["quality_score"] = quality_score
        item["status"] = status
    return resource_items


def build_exception_cases(
    documents: List[DocumentRecord],
    rules: List[ProjectRule],
    vendor_alias_map: Dict[str, str],
) -> List[Dict[str, Any]]:
    amount_clusters: Dict[str, List[DocumentRecord]] = {}
    date_clusters: Dict[str, List[DocumentRecord]] = {}
    refund_clusters: Dict[str, List[DocumentRecord]] = {}
    duplicate_clusters: Dict[str, List[DocumentRecord]] = {}
    mismatch_rows: List[DocumentRecord] = []

    for document in documents:
        vendor = normalize_company_name(document.company_name or "")
        if not vendor:
            continue
        amount_value = processor.amount_to_float(document.amount) or 0.0
        amount_key = f"{vendor}||{amount_value:.2f}"
        date_key = f"{vendor}||{document.date or ''}"
        dup_key = f"{document.source_type or ''}||{vendor}||{document.date or ''}||{amount_value:.2f}"
        amount_clusters.setdefault(amount_key, []).append(document)
        if document.date and document.date != "Unknown":
            date_clusters.setdefault(date_key, []).append(document)
        duplicate_clusters.setdefault(dup_key, []).append(document)
        raw = f"{document.company_name or ''} {document.raw_text or ''} {document.number or ''}".lower()
        if re.search(r"\brefund\b|\breversal\b|\breversed\b|\bchargeback\b", raw):
            refund_clusters.setdefault(vendor, []).append(document)
        status = normalized_match_status(document, rules)
        matched_amount = processor.amount_to_float(document.matched_record_amount) or 0.0
        if status == "matched" and document.matched_record_amount and abs(amount_value - matched_amount) > 0.01:
            mismatch_rows.append(document)

    cases: List[Dict[str, Any]] = []

    def record_case_rows(rows: List[DocumentRecord]) -> List[Dict[str, Any]]:
        ordered = sorted(rows, key=lambda item: (item.date or "", -(processor.amount_to_float(item.amount) or 0.0), item.id))
        return [
            {
                "id": item.id,
                "date": item.date or "",
                "number": item.number or "",
                "company_name": canonical_company_name(item, vendor_alias_map),
                "amount": processor.amount_to_float(item.amount) or 0.0,
                "source_type": item.source_type or "",
                "source_file": item.source_file or "",
                "match_status": normalized_match_status(item, rules),
                "review_state": item.review_state or "",
            }
            for item in ordered
        ]

    for key, rows in amount_clusters.items():
        dated = [row for row in rows if row.date and row.date != "Unknown"]
        if len(dated) >= 3:
            vendor_name = canonical_company_name(dated[0], vendor_alias_map)
            amount_value = processor.amount_to_float(dated[0].amount) or 0.0
            dates = sorted({row.date for row in dated})
            if len(dates) >= 3:
                cases.append({
                    "key": f"installment:{key}",
                    "type": "installment_chain",
                    "label": "Installment Chain",
                    "company_name": vendor_name,
                    "amount": sum(processor.amount_to_float(row.amount) or 0.0 for row in dated),
                    "reason": f"{len(dated)} charges of {amount_value:.2f} AED across {len(dates)} dates suggest installment behavior.",
                    "rows": record_case_rows(dated),
                })

    for vendor, rows in refund_clusters.items():
        vendor_name = canonical_company_name(rows[0], vendor_alias_map)
        related = [row for row in documents if normalize_company_name(row.company_name or "") == vendor]
        credits = [row for row in related if inferred_transaction_direction(row) == "credit" or re.search(r"\brefund\b|\breversal\b|\breversed\b|\bchargeback\b", f"{row.company_name or ''} {row.raw_text or ''}".lower())]
        debits = [row for row in related if inferred_transaction_direction(row) == "debit"]
        if credits and debits:
            case_rows = credits[:3] + debits[:3]
            cases.append({
                "key": f"refund:{vendor}",
                "type": "refund_pair",
                "label": "Refund / Reversal Pair",
                "company_name": vendor_name,
                "amount": sum(processor.amount_to_float(row.amount) or 0.0 for row in credits),
                "reason": f"{len(credits)} refund-like rows and {len(debits)} debit rows were found for the same vendor.",
                "rows": record_case_rows(case_rows),
            })

    for key, rows in date_clusters.items():
        debit_rows = [row for row in rows if inferred_transaction_direction(row) == "debit"]
        if len(debit_rows) >= 2:
            vendor_name = canonical_company_name(debit_rows[0], vendor_alias_map)
            total = sum(processor.amount_to_float(row.amount) or 0.0 for row in debit_rows)
            cases.append({
                "key": f"split:{key}",
                "type": "split_payment_group",
                "label": "Split Payment Group",
                "company_name": vendor_name,
                "amount": total,
                "reason": f"{len(debit_rows)} debit rows on the same date suggest a split payment.",
                "rows": record_case_rows(debit_rows),
            })

    for key, rows in duplicate_clusters.items():
        if len(rows) >= 2:
            vendor_name = canonical_company_name(rows[0], vendor_alias_map)
            amount_total = sum(processor.amount_to_float(row.amount) or 0.0 for row in rows)
            cases.append({
                "key": f"duplicate:{key}",
                "type": "duplicate_cluster",
                "label": "Duplicate Cluster",
                "company_name": vendor_name,
                "amount": amount_total,
                "reason": f"{len(rows)} rows share vendor, date, amount, and source type.",
                "rows": record_case_rows(rows),
            })

    for row in mismatch_rows:
        vendor_name = canonical_company_name(row, vendor_alias_map)
        current_amount = processor.amount_to_float(row.amount) or 0.0
        matched_amount = processor.amount_to_float(row.matched_record_amount) or 0.0
        cases.append({
            "key": f"mismatch:{row.id}",
            "type": "amount_mismatch_case",
            "label": "Amount Mismatch",
            "company_name": vendor_name,
            "amount": abs(current_amount - matched_amount),
            "reason": f"Matched document amount {matched_amount:.2f} AED differs from row amount {current_amount:.2f} AED.",
            "rows": record_case_rows([row]),
        })

    cases.sort(key=lambda item: (item["type"], -(item["amount"] or 0.0), item["company_name"] or ""))
    return cases


def build_feedback_suggestions(
    documents: List[DocumentRecord],
    existing_aliases: Dict[str, str],
    existing_rule_keywords: set[str],
) -> Dict[str, List[Dict[str, Any]]]:
    alias_groups: Dict[str, Dict[str, Any]] = {}
    rule_groups: Dict[str, Dict[str, Any]] = {}

    for document in documents:
        normalized = normalize_company_name(document.company_name or "")
        canonical = (document.canonical_company_name or "").strip()
        if normalized and canonical and canonical.lower() != (document.company_name or "").strip().lower():
            bucket = alias_groups.setdefault(normalized, {
                "normalized_key": normalized,
                "canonical_name": canonical,
                "count": 0,
                "examples": set(),
            })
            bucket["count"] += 1
            bucket["examples"].add(document.company_name or "")

        if document.source_type == "sheet" and document.doc_type == "BankTransaction":
            review_state = (document.review_state or "").strip().lower()
            if review_state in {"missing_receipt", "not_applicable", "reviewed"} and normalized:
                keyword = (document.company_name or "").strip()
                rule_key = f"{normalized}||{review_state}"
                bucket = rule_groups.setdefault(rule_key, {
                    "keyword": keyword,
                    "source_type": "sheet",
                    "status": review_state,
                    "category": document.category or "",
                    "subcategory": document.subcategory or "",
                    "count": 0,
                    "examples": set(),
                })
                bucket["count"] += 1
                bucket["examples"].add(document.company_name or "")

    alias_suggestions = [
        {
            "type": "vendor_alias",
            "normalized_key": key,
            "canonical_name": value["canonical_name"],
            "count": value["count"],
            "examples": sorted(example for example in value["examples"] if example)[:5],
        }
        for key, value in alias_groups.items()
        if value["count"] >= 2 and existing_aliases.get(key, "") != value["canonical_name"]
    ]
    alias_suggestions.sort(key=lambda item: (-item["count"], item["canonical_name"]))

    rule_suggestions = [
        {
            "type": "project_rule",
            "keyword": value["keyword"],
            "source_type": value["source_type"],
            "status": value["status"],
            "category": value["category"],
            "subcategory": value["subcategory"],
            "count": value["count"],
            "examples": sorted(example for example in value["examples"] if example)[:5],
        }
        for value in rule_groups.values()
        if value["count"] >= 2 and (value["keyword"] or "").strip().lower() not in existing_rule_keywords
    ]
    rule_suggestions.sort(key=lambda item: (-item["count"], item["status"], item["keyword"]))
    return {"alias_suggestions": alias_suggestions, "rule_suggestions": rule_suggestions}


def build_resource_key(document: DocumentRecord) -> str:
    raw = "|".join(
        [
            document.source_type or "",
            document.source_origin or "",
            document.source_path or "",
            document.source_file or "",
        ]
    )
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]


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
                if record.source_path
            }
        )
        cancelled = job_should_cancel(job)

        processor.reconcile_bank_transactions(records)
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
                    db_record.transaction_direction = record.transaction_direction
                    db_record.confidence_score = record.confidence_score
                    db_record.confidence_label = record.confidence_label
                    db_record.raw_text = record.raw_text
                    db_record.match_status = record.match_status
                    db_record.match_score = record.match_score
                    db_record.matched_record_source_file = record.matched_record_source_file
                    db_record.matched_record_output_file = record.matched_record_output_file
                    db_record.matched_record_source_type = record.matched_record_source_type
                    db_record.matched_record_source_timestamp = record.matched_record_source_timestamp
                    db_record.matched_record_date = record.matched_record_date
                    db_record.matched_record_number = record.matched_record_number
                    db_record.matched_record_company_name = record.matched_record_company_name
                    db_record.matched_record_amount = record.matched_record_amount
                    db_record.matched_record_transaction_direction = record.matched_record_transaction_direction
                    db_record.match_basis = record.match_basis
                    if not getattr(db_record, "canonical_company_name", ""):
                        db_record.canonical_company_name = record.company_name
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
            job.status = "cancelled" if cancelled else "completed"
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


@app.get("/api/accounting-export-options")
def accounting_export_options(x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    require_user(x_auth_token)
    return {
        "default_preset": "ultra_force",
        "presets": accounting_export_metadata(),
    }


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
        company = Company(user_id=user.id, name=f"{user.username} Company")
        session.add(company)
        session.flush()
        user.company_id = company.id
        token = create_session_token()
        session.add(AuthSession(token=token, user_id=user.id))
        return {"token": token, "user": {"id": user.id, "username": user.username, "company_id": company.id, "company_name": company.name}}


@app.post("/api/auth/login")
def login(payload: AuthRequest) -> Dict[str, Any]:
    with db_session() as session:
        user = session.query(User).filter(User.username == payload.username.strip()).first()
        if not user or not verify_password(payload.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid username or password")
        company = ensure_user_company(session, user)
        token = create_session_token()
        session.add(AuthSession(token=token, user_id=user.id))
        return {"token": token, "user": {"id": user.id, "username": user.username, "company_id": company.id, "company_name": company.name}}


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
    with db_session() as session:
        db_user = session.query(User).filter(User.id == user.id).first()
        company = ensure_user_company(session, db_user)
        return {
            "id": db_user.id,
            "username": db_user.username,
            "role": getattr(db_user, "role", "admin"),
            "company_id": company.id,
            "company_name": company.name,
        }


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
        db_user = session.query(User).filter(User.id == user.id).first()
        company = ensure_user_company(session, db_user)
        owned_projects = session.query(Project).filter(Project.user_id == user.id).all()
        membership_rows = session.query(ProjectMember).filter(ProjectMember.user_id == user.id).all()
        member_project_ids = [item.project_id for item in membership_rows]
        shared_projects = session.query(Project).filter(Project.id.in_(member_project_ids)).all() if member_project_ids else []
        role_map = {item.project_id: (item.role or "viewer").strip().lower() for item in membership_rows}
        combined: Dict[int, tuple[Project, str]] = {}
        for project in owned_projects:
            project.company_name = company.name if getattr(project, "company_id", None) == company.id else ""
            combined[project.id] = (project, "owner")
        for project in shared_projects:
            if getattr(project, "company_id", None) == company.id:
                project.company_name = company.name
            combined.setdefault(project.id, (project, role_map.get(project.id, "viewer")))
        ordered = sorted(combined.values(), key=lambda item: item[0].updated_at or datetime.min, reverse=True)
        return {"projects": [project_to_payload(project, access_role=access_role) for project, access_role in ordered]}


@app.post("/api/projects")
def create_project(project_request: ProjectRequest, x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        db_user = session.query(User).filter(User.id == user.id).first()
        company = ensure_user_company(session, db_user)
        project = Project(
            user_id=user.id,
            company_id=company.id,
            name=project_request.name.strip(),
            description=project_request.description.strip(),
            job_code=project_request.job_code.strip(),
            client_name=project_request.client_name.strip(),
            site_name=project_request.site_name.strip(),
            contract_number=project_request.contract_number.strip(),
            budget_amount=project_request.budget_amount.strip(),
            contract_value=project_request.contract_value.strip(),
            variation_amount=project_request.variation_amount.strip(),
            billed_to_date=project_request.billed_to_date.strip(),
            certified_progress_pct=project_request.certified_progress_pct.strip(),
            retention_percent=project_request.retention_percent.strip(),
            advance_received=project_request.advance_received.strip(),
            project_status=(project_request.project_status or "active").strip(),
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
        session.add(ProjectMember(project_id=project.id, user_id=user.id, role="owner"))
        session.refresh(project)
        project.company_name = company.name
        return {"project": project_to_payload(project, access_role="owner")}


@app.put("/api/projects/{project_id}")
def update_project(
    project_id: int,
    project_request: ProjectRequest,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        project, access_role = require_project_access(session, project_id, user, min_role="admin")
        company = ensure_project_company(session, project, user)
        project.name = project_request.name.strip()
        project.description = project_request.description.strip()
        project.job_code = project_request.job_code.strip()
        project.client_name = project_request.client_name.strip()
        project.site_name = project_request.site_name.strip()
        project.contract_number = project_request.contract_number.strip()
        project.budget_amount = project_request.budget_amount.strip()
        project.contract_value = project_request.contract_value.strip()
        project.variation_amount = project_request.variation_amount.strip()
        project.billed_to_date = project_request.billed_to_date.strip()
        project.certified_progress_pct = project_request.certified_progress_pct.strip()
        project.retention_percent = project_request.retention_percent.strip()
        project.advance_received = project_request.advance_received.strip()
        project.project_status = (project_request.project_status or "active").strip()
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
        project.company_name = company.name
        return {"project": project_to_payload(project, access_role=access_role)}


@app.delete("/api/projects/{project_id}")
def delete_project(project_id: int, x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="owner")
        session.delete(project)
        return {"deleted": True, "project_id": project_id}


@app.get("/api/projects/{project_id}/members")
def list_project_members(project_id: int, x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="viewer")
        members = (
            session.query(ProjectMember)
            .filter(ProjectMember.project_id == project.id)
            .order_by(ProjectMember.created_at.asc(), ProjectMember.id.asc())
            .all()
        )
        if not any(item.user_id == project.user_id for item in members):
            owner_member = ProjectMember(project_id=project.id, user_id=project.user_id, role="owner")
            session.add(owner_member)
            session.flush()
            members.append(owner_member)
        user_ids = [item.user_id for item in members]
        user_map = {
            item.id: item
            for item in session.query(User).filter(User.id.in_(user_ids)).all()
        } if user_ids else {}
        return {"members": [serialize_project_member(item, user_map.get(item.user_id)) for item in members]}


@app.get("/api/projects/{project_id}/accounts")
def list_project_accounts(project_id: int, x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="viewer")
        company = ensure_project_company(session, project, user)
        accounts = (
            session.query(AccountingAccount)
            .filter(AccountingAccount.company_id == company.id)
            .order_by(AccountingAccount.code.asc(), AccountingAccount.id.asc())
            .all()
        )
        return {"accounts": [serialize_account(item) for item in accounts]}


@app.get("/api/companies/current/accounts")
def list_current_company_accounts(x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        accounts = (
            session.query(AccountingAccount)
            .filter(AccountingAccount.company_id == company.id)
            .order_by(AccountingAccount.code.asc(), AccountingAccount.id.asc())
            .all()
        )
        return {"accounts": [serialize_account(item) for item in accounts]}


@app.post("/api/projects/{project_id}/accounts")
def create_project_account(
    project_id: int,
    payload: AccountingAccountRequest,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="admin")
        company = ensure_project_company(session, project, user)
        code = (payload.code or "").strip()
        name = (payload.name or "").strip()
        account_type = (payload.account_type or "").strip().lower()
        if not code or not name or account_type not in {"asset", "liability", "equity", "revenue", "expense"}:
            raise HTTPException(status_code=400, detail="Invalid account payload")
        existing = (
            session.query(AccountingAccount)
            .filter(AccountingAccount.company_id == company.id, AccountingAccount.code == code)
            .first()
        )
        if existing:
            raise HTTPException(status_code=400, detail="Account code already exists")
        account = AccountingAccount(
            user_id=user.id,
            company_id=company.id,
            project_id=project.id,
            code=code,
            name=name,
            account_type=account_type,
            subtype=(payload.subtype or "").strip(),
            is_active=bool(payload.is_active),
        )
        session.add(account)
        session.flush()
        return {"account": serialize_account(account)}


@app.post("/api/companies/current/accounts")
def create_current_company_account(
    payload: AccountingAccountRequest,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        anchor_project = require_company_anchor_project(session, company, user)
        code = (payload.code or "").strip()
        name = (payload.name or "").strip()
        account_type = (payload.account_type or "").strip().lower()
        if not code or not name or account_type not in {"asset", "liability", "equity", "revenue", "expense"}:
            raise HTTPException(status_code=400, detail="Invalid account payload")
        existing = (
            session.query(AccountingAccount)
            .filter(AccountingAccount.company_id == company.id, AccountingAccount.code == code)
            .first()
        )
        if existing:
            raise HTTPException(status_code=400, detail="Account code already exists")
        account = AccountingAccount(
            user_id=user.id,
            company_id=company.id,
            project_id=anchor_project.id,
            code=code,
            name=name,
            account_type=account_type,
            subtype=(payload.subtype or "").strip(),
            is_active=bool(payload.is_active),
        )
        session.add(account)
        session.flush()
        return {"account": serialize_account(account)}


@app.post("/api/projects/{project_id}/accounts/seed-construction")
def seed_project_accounts(project_id: int, x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="admin")
        company = ensure_project_company(session, project, user)
        existing_codes = {
            item.code
            for item in session.query(AccountingAccount.code).filter(AccountingAccount.company_id == company.id).all()
        }
        created: List[AccountingAccount] = []
        for item in default_construction_accounts():
            if item["code"] in existing_codes:
                continue
            account = AccountingAccount(
                user_id=user.id,
                company_id=company.id,
                project_id=project.id,
                code=item["code"],
                name=item["name"],
                account_type=item["account_type"],
                subtype=item["subtype"],
                is_active=True,
            )
            session.add(account)
            created.append(account)
        session.flush()
        return {
            "created_count": len(created),
            "accounts": [serialize_account(item) for item in created],
        }


@app.post("/api/companies/current/accounts/seed-construction")
def seed_current_company_accounts(x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        anchor_project = require_company_anchor_project(session, company, user)
        existing_codes = {
            item.code
            for item in session.query(AccountingAccount.code).filter(AccountingAccount.company_id == company.id).all()
        }
        created: List[AccountingAccount] = []
        for item in default_construction_accounts():
            if item["code"] in existing_codes:
                continue
            account = AccountingAccount(
                user_id=user.id,
                company_id=company.id,
                project_id=anchor_project.id,
                code=item["code"],
                name=item["name"],
                account_type=item["account_type"],
                subtype=item["subtype"],
                is_active=True,
            )
            session.add(account)
            created.append(account)
        session.flush()
        return {
            "created_count": len(created),
            "accounts": [serialize_account(item) for item in created],
        }


@app.delete("/api/projects/{project_id}/accounts/{account_id}")
def delete_project_account(
    project_id: int,
    account_id: int,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="admin")
        company = ensure_project_company(session, project, user)
        account = (
            session.query(AccountingAccount)
            .filter(AccountingAccount.company_id == company.id, AccountingAccount.id == account_id)
            .first()
        )
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        session.delete(account)
        return {"deleted": True, "account_id": account_id}


@app.delete("/api/companies/current/accounts/{account_id}")
def delete_current_company_account(account_id: int, x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        account = (
            session.query(AccountingAccount)
            .filter(AccountingAccount.company_id == company.id, AccountingAccount.id == account_id)
            .first()
        )
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        session.delete(account)
        return {"deleted": True, "account_id": account_id}


@app.get("/api/projects/{project_id}/periods")
def list_project_periods(project_id: int, x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="viewer")
        company = ensure_project_company(session, project, user)
        periods = (
            session.query(AccountingPeriod)
            .filter(AccountingPeriod.company_id == company.id)
            .order_by(AccountingPeriod.start_date.asc(), AccountingPeriod.id.asc())
            .all()
        )
        return {"periods": [serialize_period(item) for item in periods]}


@app.get("/api/companies/current/periods")
def list_current_company_periods(x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        periods = (
            session.query(AccountingPeriod)
            .filter(AccountingPeriod.company_id == company.id)
            .order_by(AccountingPeriod.start_date.asc(), AccountingPeriod.id.asc())
            .all()
        )
        return {"periods": [serialize_period(item) for item in periods]}


@app.get("/api/projects/{project_id}/journal-drafts")
def list_project_journal_drafts(project_id: int, x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="viewer")
        company = ensure_project_company(session, project, user)
        company_rules = (
            session.query(CompanyAccountingRule)
            .filter(CompanyAccountingRule.company_id == company.id)
            .order_by(CompanyAccountingRule.created_at.asc(), CompanyAccountingRule.id.asc())
            .all()
        )
        rules = (
            session.query(ProjectRule)
            .filter(ProjectRule.project_id == project.id)
            .order_by(ProjectRule.created_at.asc(), ProjectRule.id.asc())
            .all()
        )
        documents = (
            session.query(DocumentRecord)
            .filter(DocumentRecord.project_id == project.id)
            .order_by(DocumentRecord.date.asc(), DocumentRecord.created_at.asc(), DocumentRecord.id.asc())
            .all()
        )
        effective_rules = combined_accounting_rules(rules, company_rules)
        drafts = [item for item in (journal_draft_for_document(document, effective_rules) for document in documents) if item]
        posted_document_ids = {
            item.document_id
            for item in session.query(JournalEntry.document_id)
            .filter(JournalEntry.company_id == company.id, JournalEntry.status == "posted")
            .all()
            if item.document_id
        }
        drafts = [item for item in drafts if item["document_id"] not in posted_document_ids]
        return {
            "summary": {
                "draft_count": len(drafts),
                "posted_amount": round(sum(float(item["amount"]) for item in drafts), 2),
            },
            "drafts": drafts,
        }


@app.get("/api/companies/current/journal-drafts")
def list_current_company_journal_drafts(x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        project_ids = [item.id for item in session.query(Project.id).filter(Project.company_id == company.id).all()]
        company_rules = (
            session.query(CompanyAccountingRule)
            .filter(CompanyAccountingRule.company_id == company.id)
            .order_by(CompanyAccountingRule.created_at.asc(), CompanyAccountingRule.id.asc())
            .all()
        )
        periods = (
            session.query(AccountingPeriod)
            .filter(AccountingPeriod.company_id == company.id)
            .order_by(AccountingPeriod.start_date.asc(), AccountingPeriod.id.asc())
            .all()
        )
        project_rules_map: Dict[int, List[ProjectRule]] = {}
        if project_ids:
            for rule in (
                session.query(ProjectRule)
                .filter(ProjectRule.project_id.in_(project_ids))
                .order_by(ProjectRule.project_id.asc(), ProjectRule.created_at.asc(), ProjectRule.id.asc())
                .all()
            ):
                project_rules_map.setdefault(int(rule.project_id), []).append(rule)
        documents = (
            session.query(DocumentRecord)
            .filter(DocumentRecord.project_id.in_(project_ids if project_ids else [-1]))
            .order_by(DocumentRecord.date.asc(), DocumentRecord.created_at.asc(), DocumentRecord.id.asc())
            .all()
        )
        drafts = [
            item
            for item in (
                journal_draft_for_document(
                    document,
                    combined_accounting_rules(project_rules_map.get(int(document.project_id), []), company_rules),
                )
                for document in documents
            )
            if item
        ]
        posted_document_ids = {
            item.document_id
            for item in session.query(JournalEntry.document_id)
            .filter(JournalEntry.company_id == company.id, JournalEntry.status == "posted")
            .all()
            if item.document_id
        }
        drafts = [item for item in drafts if item["document_id"] not in posted_document_ids]
        drafts = [annotate_draft_with_period(item, periods) for item in drafts]
        return {
            "summary": {
                "draft_count": len(drafts),
                "posted_amount": round(sum(float(item["amount"]) for item in drafts), 2),
            },
            "drafts": drafts,
        }


@app.post("/api/projects/{project_id}/journal-post")
def post_project_journals(
    project_id: int,
    payload: JournalPostRequest,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="admin")
        company = ensure_project_company(session, project, user)
        company_rules = (
            session.query(CompanyAccountingRule)
            .filter(CompanyAccountingRule.company_id == company.id)
            .order_by(CompanyAccountingRule.created_at.asc(), CompanyAccountingRule.id.asc())
            .all()
        )
        rules = (
            session.query(ProjectRule)
            .filter(ProjectRule.project_id == project.id)
            .order_by(ProjectRule.created_at.asc(), ProjectRule.id.asc())
            .all()
        )
        query = session.query(DocumentRecord).filter(DocumentRecord.project_id == project.id)
        if payload.document_ids:
            query = query.filter(DocumentRecord.id.in_(payload.document_ids))
        documents = query.order_by(DocumentRecord.date.asc(), DocumentRecord.created_at.asc(), DocumentRecord.id.asc()).all()
        posted_existing = {
            item.document_id
            for item in session.query(JournalEntry.document_id)
            .filter(JournalEntry.company_id == company.id, JournalEntry.status == "posted")
            .all()
            if item.document_id
        }
        created_entries: List[JournalEntry] = []
        skipped_undated: List[Dict[str, Any]] = []
        for document in documents:
            if document.id in posted_existing:
                continue
            draft = journal_draft_for_document(document, combined_accounting_rules(rules, company_rules))
            if not draft:
                continue
            draft_date = (draft.get("date") or "").strip()
            if not draft_date or draft_date == "Unknown":
                skipped_undated.append({
                    "document_id": document.id,
                    "source_file": document.source_file or "",
                    "vendor": document.canonical_company_name or document.company_name or "",
                })
                continue
            entry = JournalEntry(
                user_id=user.id,
                company_id=company.id,
                project_id=project.id,
                document_id=document.id,
                entry_date=draft["date"],
                reference=draft["reference"],
                memo=draft["memo"],
                status="posted",
            )
            session.add(entry)
            session.flush()
            for line in draft["lines"]:
                session.add(JournalEntryLine(
                    entry_id=entry.id,
                    account_code=line["account_code"],
                    debit=line["debit"],
                    credit=line["credit"],
                    cost_center=document.cost_center or "",
                    project_code=document.project_code or "",
                ))
            created_entries.append(entry)
        session.flush()
        return {
            "created_count": len(created_entries),
            "skipped_undated_count": len(skipped_undated),
            "skipped_undated": skipped_undated[:10],
            "entries": [serialize_journal_entry(item) for item in created_entries],
        }


@app.post("/api/companies/current/journal-post")
def post_current_company_journals(
    payload: JournalPostRequest,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        project_ids = [item.id for item in session.query(Project.id).filter(Project.company_id == company.id).all()]
        company_rules = (
            session.query(CompanyAccountingRule)
            .filter(CompanyAccountingRule.company_id == company.id)
            .order_by(CompanyAccountingRule.created_at.asc(), CompanyAccountingRule.id.asc())
            .all()
        )
        project_rules_map: Dict[int, List[ProjectRule]] = {}
        if project_ids:
            project_rules = (
                session.query(ProjectRule)
                .filter(ProjectRule.project_id.in_(project_ids))
                .order_by(ProjectRule.project_id.asc(), ProjectRule.created_at.asc(), ProjectRule.id.asc())
                .all()
            )
            for rule in project_rules:
                project_rules_map.setdefault(int(rule.project_id), []).append(rule)
        periods = (
            session.query(AccountingPeriod)
            .filter(AccountingPeriod.company_id == company.id)
            .order_by(AccountingPeriod.start_date.asc(), AccountingPeriod.id.asc())
            .all()
        )
        query = session.query(DocumentRecord).filter(DocumentRecord.project_id.in_(project_ids if project_ids else [-1]))
        if payload.document_ids:
            query = query.filter(DocumentRecord.id.in_(payload.document_ids))
        documents = query.order_by(DocumentRecord.date.asc(), DocumentRecord.created_at.asc(), DocumentRecord.id.asc()).all()
        posted_existing = {
            item.document_id
            for item in session.query(JournalEntry.document_id)
            .filter(JournalEntry.company_id == company.id, JournalEntry.status == "posted")
            .all()
            if item.document_id
        }
        created_entries: List[JournalEntry] = []
        skipped_undated: List[Dict[str, Any]] = []
        for document in documents:
            if document.id in posted_existing:
                continue
            draft = journal_draft_for_document(
                document,
                combined_accounting_rules(project_rules_map.get(int(document.project_id), []), company_rules),
            )
            if not draft:
                continue
            draft_date = (draft.get("date") or "").strip()
            if not draft_date or draft_date == "Unknown":
                skipped_undated.append({
                    "document_id": document.id,
                    "source_file": document.source_file or "",
                    "vendor": document.canonical_company_name or document.company_name or "",
                })
                continue
            draft = annotate_draft_with_period(draft, periods)
            if not draft.get("posting_allowed"):
                raise HTTPException(
                    status_code=400,
                    detail=draft.get("posting_reason") or "Posting blocked by accounting period status",
                )
            entry = JournalEntry(
                user_id=user.id,
                company_id=company.id,
                project_id=document.project_id,
                document_id=document.id,
                entry_date=draft["date"],
                reference=draft["reference"],
                memo=draft["memo"],
                status="posted",
            )
            session.add(entry)
            session.flush()
            for line in draft["lines"]:
                session.add(JournalEntryLine(
                    entry_id=entry.id,
                    account_code=line["account_code"],
                    debit=line["debit"],
                    credit=line["credit"],
                    cost_center=document.cost_center or "",
                    project_code=document.project_code or "",
                ))
            created_entries.append(entry)
        session.flush()
        return {
            "created_count": len(created_entries),
            "skipped_undated_count": len(skipped_undated),
            "skipped_undated": skipped_undated[:10],
            "entries": [serialize_journal_entry(item) for item in created_entries],
        }


@app.get("/api/projects/{project_id}/journal-entries")
def list_project_journal_entries(project_id: int, x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="viewer")
        company = ensure_project_company(session, project, user)
        entries = (
            session.query(JournalEntry)
            .filter(JournalEntry.company_id == company.id)
            .order_by(JournalEntry.entry_date.asc(), JournalEntry.id.asc())
            .all()
        )
        for entry in entries:
            _ = entry.lines
        return {
            "entries": [serialize_journal_entry(item) for item in entries],
            "trial_balance": trial_balance_rows(entries),
        }


@app.get("/api/companies/current/journal-entries")
def list_current_company_journal_entries(x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        entries = (
            session.query(JournalEntry)
            .filter(JournalEntry.company_id == company.id)
            .order_by(JournalEntry.entry_date.asc(), JournalEntry.id.asc())
            .all()
        )
        for entry in entries:
            _ = entry.lines
        return {
            "entries": [serialize_journal_entry(item) for item in entries],
            "trial_balance": trial_balance_rows(entries),
        }


@app.get("/api/companies/current/ledger")
def list_current_company_ledger(
    account_code: str,
    project_code: str = "",
    cost_center: str = "",
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        entries = (
            session.query(JournalEntry)
            .filter(JournalEntry.company_id == company.id, JournalEntry.status == "posted")
            .order_by(JournalEntry.entry_date.asc(), JournalEntry.id.asc())
            .all()
        )
        for entry in entries:
            _ = entry.lines
        rows = company_ledger_rows(entries, (account_code or "").strip())
        project_filter = (project_code or "").strip().lower()
        cost_filter = (cost_center or "").strip().lower()
        if project_filter:
            rows = [row for row in rows if project_filter in (row.get("project_code", "") or "").lower()]
        if cost_filter:
            rows = [row for row in rows if cost_filter in (row.get("cost_center", "") or "").lower()]
        return {
            "account_code": (account_code or "").strip(),
            "rows": rows,
            "summary": {
                "count": len(rows),
                "ending_balance": rows[-1]["balance"] if rows else 0,
            },
            "filters": {
                "project_code": project_code,
                "cost_center": cost_center,
            },
        }


@app.post("/api/projects/{project_id}/journal-entries/{entry_id}/unpost")
def unpost_project_journal_entry(project_id: int, entry_id: int, x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="admin")
        company = ensure_project_company(session, project, user)
        entry = (
            session.query(JournalEntry)
            .filter(JournalEntry.company_id == company.id, JournalEntry.id == entry_id)
            .first()
        )
        if not entry:
            raise HTTPException(status_code=404, detail="Journal entry not found")
        entry.status = "unposted"
        session.flush()
        _ = entry.lines
        return {"entry": serialize_journal_entry(entry)}


@app.post("/api/companies/current/journal-entries/{entry_id}/unpost")
def unpost_current_company_journal_entry(entry_id: int, x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        entry = (
            session.query(JournalEntry)
            .filter(JournalEntry.company_id == company.id, JournalEntry.id == entry_id)
            .first()
        )
        if not entry:
            raise HTTPException(status_code=404, detail="Journal entry not found")
        entry.status = "unposted"
        session.flush()
        _ = entry.lines
        return {"entry": serialize_journal_entry(entry)}


@app.get("/api/companies/current")
def get_current_company(x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        return {"company": serialize_company(company)}


@app.get("/api/companies")
def list_companies(x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        db_user = session.query(User).filter(User.id == user.id).first()
        current = require_current_company(session, db_user)
        companies = (
            session.query(Company)
            .filter(Company.user_id == db_user.id)
            .order_by(Company.name.asc(), Company.id.asc())
            .all()
        )
        return {
            "companies": [
                {**serialize_company(item), "is_active": item.id == current.id}
                for item in companies
            ],
            "current_company_id": current.id,
        }


@app.post("/api/companies")
def create_company(payload: CompanyCreateRequest, x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        db_user = session.query(User).filter(User.id == user.id).first()
        name = (payload.name or "").strip()
        if not name:
            raise HTTPException(status_code=400, detail="Company name is required")
        company = Company(user_id=db_user.id, name=name)
        session.add(company)
        session.flush()
        db_user.company_id = company.id
        session.flush()
        return {"company": {**serialize_company(company), "is_active": True}}


@app.post("/api/companies/{company_id}/activate")
def activate_company(company_id: int, x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        db_user = session.query(User).filter(User.id == user.id).first()
        company = session.query(Company).filter(Company.id == company_id, Company.user_id == db_user.id).first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        db_user.company_id = company.id
        session.flush()
        return {"company": {**serialize_company(company), "is_active": True}}


@app.put("/api/companies/current")
def update_current_company(
    payload: CompanyUpdateRequest,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        company.name = (payload.name or "").strip() or company.name or "My Company"
        company.base_currency = (payload.base_currency or "AED").strip().upper() or "AED"
        month = int(payload.fiscal_year_start_month or 1)
        if month < 1 or month > 12:
            raise HTTPException(status_code=400, detail="Fiscal year start month must be between 1 and 12")
        company.fiscal_year_start_month = month
        company.vat_registration_number = (payload.vat_registration_number or "").strip()
        company.vat_rate = (payload.vat_rate or "5.00").strip() or "5.00"
        session.flush()
        return {"company": serialize_company(company)}


@app.get("/api/companies/current/accounting-rules")
def list_current_company_accounting_rules(x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        rules = (
            session.query(CompanyAccountingRule)
            .filter(CompanyAccountingRule.company_id == company.id)
            .order_by(CompanyAccountingRule.created_at.asc(), CompanyAccountingRule.id.asc())
            .all()
        )
        return {"rules": [serialize_accounting_rule(rule, "company") for rule in rules]}


@app.post("/api/companies/current/accounting-rules")
def create_current_company_accounting_rule(
    payload: CompanyAccountingRuleRequest,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        keyword = (payload.keyword or "").strip()
        if not keyword:
            raise HTTPException(status_code=400, detail="Keyword is required")
        rule = CompanyAccountingRule(
            user_id=user.id,
            company_id=company.id,
            keyword=keyword,
            source_type=(payload.source_type or "").strip(),
            status=(payload.status or "").strip(),
            category=(payload.category or "").strip(),
            subcategory=(payload.subcategory or "").strip(),
            account_code=(payload.account_code or "").strip(),
            offset_account_code=(payload.offset_account_code or "").strip(),
            project_code=(payload.project_code or "").strip(),
            cost_code=(payload.cost_code or "").strip(),
            cost_center=(payload.cost_center or "").strip(),
            payment_method=(payload.payment_method or "").strip(),
            vat_flag=payload.vat_flag,
            auto_post=payload.auto_post,
        )
        session.add(rule)
        session.flush()
        return {"rule": serialize_accounting_rule(rule, "company")}


@app.post("/api/companies/current/accounting-rules/seed")
def seed_current_company_accounting_rules(x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        existing_rules = (
            session.query(CompanyAccountingRule)
            .filter(CompanyAccountingRule.company_id == company.id)
            .order_by(CompanyAccountingRule.created_at.asc(), CompanyAccountingRule.id.asc())
            .all()
        )
        existing_keys = {
            ((item.keyword or "").strip().lower(), (item.source_type or "").strip().lower())
            for item in existing_rules
        }
        created: List[CompanyAccountingRule] = []
        for spec in seeded_accounting_rule_specs():
            key = ((spec.get("keyword") or "").strip().lower(), (spec.get("source_type") or "").strip().lower())
            if not key[0] or key in existing_keys:
                continue
            rule = CompanyAccountingRule(
                user_id=user.id,
                company_id=company.id,
                keyword=spec.get("keyword", "").strip(),
                source_type=spec.get("source_type", "").strip(),
                status=spec.get("status", "").strip(),
                category=spec.get("category", "").strip(),
                subcategory=spec.get("subcategory", "").strip(),
                account_code=spec.get("account_code", "").strip(),
                offset_account_code=spec.get("offset_account_code", "").strip(),
                project_code=spec.get("project_code", "").strip(),
                cost_code=spec.get("cost_code", "").strip(),
                cost_center=spec.get("cost_center", "").strip(),
                payment_method=spec.get("payment_method", "").strip(),
                vat_flag=bool(spec.get("vat_flag", False)),
                auto_post=bool(spec.get("auto_post", True)),
            )
            session.add(rule)
            created.append(rule)
            existing_keys.add(key)
        project_ids = [item.id for item in session.query(Project.id).filter(Project.company_id == company.id).all()]
        documents = (
            session.query(DocumentRecord)
            .filter(DocumentRecord.project_id.in_(project_ids if project_ids else [-1]))
            .order_by(DocumentRecord.created_at.desc(), DocumentRecord.id.desc())
            .all()
        )
        inferred_candidates: Dict[Tuple[str, str], Dict[str, Any]] = {}
        for document in documents:
            spec = infer_rule_spec_from_document(document)
            if not spec:
                continue
            key = ((spec.get("keyword") or "").strip().lower(), (spec.get("source_type") or "").strip().lower())
            if not key[0] or key in existing_keys:
                continue
            if key not in inferred_candidates:
                inferred_candidates[key] = spec
            if len(inferred_candidates) >= 40:
                break
        for spec in inferred_candidates.values():
            rule = CompanyAccountingRule(
                user_id=user.id,
                company_id=company.id,
                keyword=spec.get("keyword", "").strip(),
                source_type=spec.get("source_type", "").strip(),
                status=spec.get("status", "").strip(),
                category=spec.get("category", "").strip(),
                subcategory=spec.get("subcategory", "").strip(),
                account_code=spec.get("account_code", "").strip(),
                offset_account_code=spec.get("offset_account_code", "").strip(),
                project_code=spec.get("project_code", "").strip(),
                cost_code=spec.get("cost_code", "").strip(),
                cost_center=spec.get("cost_center", "").strip(),
                payment_method=spec.get("payment_method", "").strip(),
                vat_flag=bool(spec.get("vat_flag", False)),
                auto_post=bool(spec.get("auto_post", True)),
            )
            session.add(rule)
            created.append(rule)
            existing_keys.add(((spec.get("keyword") or "").strip().lower(), (spec.get("source_type") or "").strip().lower()))
        session.flush()
        return {"created_count": len(created), "rules": [serialize_accounting_rule(rule, "company") for rule in created]}


@app.delete("/api/companies/current/accounting-rules/{rule_id}")
def delete_current_company_accounting_rule(rule_id: int, x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        rule = (
            session.query(CompanyAccountingRule)
            .filter(CompanyAccountingRule.id == rule_id, CompanyAccountingRule.company_id == company.id)
            .first()
        )
        if not rule:
            raise HTTPException(status_code=404, detail="Rule not found")
        session.delete(rule)
        return {"deleted": True, "rule_id": rule_id}


@app.get("/api/companies/current/parties")
def list_current_company_parties(
    party_type: str = "",
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        query = session.query(CompanyParty).filter(CompanyParty.company_id == company.id)
        normalized_type = (party_type or "").strip().lower()
        if normalized_type in {"supplier", "customer"}:
            query = query.filter(CompanyParty.party_type == normalized_type)
        parties = query.order_by(CompanyParty.party_type.asc(), CompanyParty.name.asc(), CompanyParty.id.asc()).all()
        return {"parties": [serialize_company_party(item) for item in parties]}


@app.post("/api/companies/current/parties")
def create_current_company_party(
    payload: CompanyPartyRequest,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        party_type = (payload.party_type or "supplier").strip().lower()
        if party_type not in {"supplier", "customer"}:
            raise HTTPException(status_code=400, detail="Party type must be supplier or customer")
        name = (payload.name or "").strip()
        if not name:
            raise HTTPException(status_code=400, detail="Party name is required")
        party = CompanyParty(
            user_id=user.id,
            company_id=company.id,
            party_type=party_type,
            name=name,
            tax_registration_number=(payload.tax_registration_number or "").strip(),
            contact_email=(payload.contact_email or "").strip(),
            contact_phone=(payload.contact_phone or "").strip(),
            default_account_code=(payload.default_account_code or "").strip(),
            payment_terms_days=max(0, int(payload.payment_terms_days or 0)),
        )
        session.add(party)
        session.flush()
        return {"party": serialize_company_party(party)}


@app.delete("/api/companies/current/parties/{party_id}")
def delete_current_company_party(party_id: int, x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        party = session.query(CompanyParty).filter(CompanyParty.company_id == company.id, CompanyParty.id == party_id).first()
        if not party:
            raise HTTPException(status_code=404, detail="Party not found")
        session.delete(party)
        return {"deleted": True, "party_id": party_id}


@app.get("/api/companies/current/dimensions")
def list_current_company_dimensions(
    dimension_type: str = "",
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        query = session.query(CompanyDimension).filter(CompanyDimension.company_id == company.id)
        normalized_type = (dimension_type or "").strip().lower()
        if normalized_type in {"project_code", "cost_center", "cost_code"}:
            query = query.filter(CompanyDimension.dimension_type == normalized_type)
        items = query.order_by(CompanyDimension.dimension_type.asc(), CompanyDimension.code.asc(), CompanyDimension.id.asc()).all()
        return {"dimensions": [serialize_company_dimension(item) for item in items]}


@app.get("/api/companies/current/ap-summary")
def get_current_company_ap_summary(x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        suppliers = (
            session.query(CompanyParty)
            .filter(CompanyParty.company_id == company.id, CompanyParty.party_type == "supplier")
            .order_by(CompanyParty.name.asc(), CompanyParty.id.asc())
            .all()
        )
        documents = (
            session.query(DocumentRecord)
            .join(Project, Project.id == DocumentRecord.project_id)
            .filter(Project.company_id == company.id)
            .order_by(DocumentRecord.date.desc(), DocumentRecord.created_at.desc(), DocumentRecord.id.desc())
            .all()
        )
        allocations = (
            session.query(CompanyAllocation)
            .filter(CompanyAllocation.company_id == company.id, CompanyAllocation.allocation_type == "payable")
            .order_by(CompanyAllocation.created_at.desc(), CompanyAllocation.id.desc())
            .all()
        )
        return build_company_party_aging(
            documents,
            suppliers,
            party_type="supplier",
            target_allocation_totals=company_allocation_totals(allocations, field_name="target_document_id"),
        )


@app.get("/api/companies/current/ar-summary")
def get_current_company_ar_summary(x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        customers = (
            session.query(CompanyParty)
            .filter(CompanyParty.company_id == company.id, CompanyParty.party_type == "customer")
            .order_by(CompanyParty.name.asc(), CompanyParty.id.asc())
            .all()
        )
        documents = (
            session.query(DocumentRecord)
            .join(Project, Project.id == DocumentRecord.project_id)
            .filter(Project.company_id == company.id)
            .order_by(DocumentRecord.date.desc(), DocumentRecord.created_at.desc(), DocumentRecord.id.desc())
            .all()
        )
        allocations = (
            session.query(CompanyAllocation)
            .filter(CompanyAllocation.company_id == company.id, CompanyAllocation.allocation_type == "receivable")
            .order_by(CompanyAllocation.created_at.desc(), CompanyAllocation.id.desc())
            .all()
        )
        return build_company_party_aging(
            documents,
            customers,
            party_type="customer",
            target_allocation_totals=company_allocation_totals(allocations, field_name="target_document_id"),
        )


@app.get("/api/companies/current/procurement-summary")
def get_current_company_procurement_summary(x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        projects = (
            session.query(Project)
            .filter(Project.company_id == company.id)
            .order_by(Project.name.asc(), Project.id.asc())
            .all()
        )
        suppliers = (
            session.query(CompanyParty)
            .filter(CompanyParty.company_id == company.id, CompanyParty.party_type == "supplier")
            .order_by(CompanyParty.name.asc(), CompanyParty.id.asc())
            .all()
        )
        documents = (
            session.query(DocumentRecord)
            .join(Project, Project.id == DocumentRecord.project_id)
            .filter(Project.company_id == company.id)
            .order_by(DocumentRecord.date.desc(), DocumentRecord.created_at.desc(), DocumentRecord.id.desc())
            .all()
        )
        allocations = (
            session.query(CompanyAllocation)
            .filter(CompanyAllocation.company_id == company.id, CompanyAllocation.allocation_type == "payable")
            .order_by(CompanyAllocation.created_at.desc(), CompanyAllocation.id.desc())
            .all()
        )
        purchase_orders = (
            session.query(CompanyPurchaseOrder)
            .filter(CompanyPurchaseOrder.company_id == company.id)
            .order_by(CompanyPurchaseOrder.po_date.desc(), CompanyPurchaseOrder.id.desc())
            .all()
        )
        receipts = (
            session.query(CompanyReceipt)
            .join(CompanyPurchaseOrder, CompanyPurchaseOrder.id == CompanyReceipt.purchase_order_id)
            .filter(CompanyReceipt.company_id == company.id, CompanyPurchaseOrder.company_id == company.id)
            .order_by(CompanyReceipt.receipt_date.desc(), CompanyReceipt.id.desc())
            .all()
        )
        ap_result = build_company_party_aging(
            documents,
            suppliers,
            party_type="supplier",
            target_allocation_totals=company_allocation_totals(allocations, field_name="target_document_id"),
        )
        return build_company_procurement_summary(projects, purchase_orders, receipts, ap_result["all_rows"], suppliers)


@app.get("/api/companies/current/procurement-exceptions")
def get_current_company_procurement_exceptions(
    review_state: str = "",
    mine_only: bool = False,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        projects = (
            session.query(Project)
            .filter(Project.company_id == company.id)
            .order_by(Project.name.asc(), Project.id.asc())
            .all()
        )
        suppliers = (
            session.query(CompanyParty)
            .filter(CompanyParty.company_id == company.id, CompanyParty.party_type == "supplier")
            .order_by(CompanyParty.name.asc(), CompanyParty.id.asc())
            .all()
        )
        documents = (
            session.query(DocumentRecord)
            .join(Project, Project.id == DocumentRecord.project_id)
            .filter(Project.company_id == company.id)
            .order_by(DocumentRecord.date.desc(), DocumentRecord.created_at.desc(), DocumentRecord.id.desc())
            .all()
        )
        allocations = (
            session.query(CompanyAllocation)
            .filter(CompanyAllocation.company_id == company.id, CompanyAllocation.allocation_type == "payable")
            .order_by(CompanyAllocation.created_at.desc(), CompanyAllocation.id.desc())
            .all()
        )
        purchase_orders = (
            session.query(CompanyPurchaseOrder)
            .filter(CompanyPurchaseOrder.company_id == company.id)
            .order_by(CompanyPurchaseOrder.po_date.desc(), CompanyPurchaseOrder.id.desc())
            .all()
        )
        receipts = (
            session.query(CompanyReceipt)
            .join(CompanyPurchaseOrder, CompanyPurchaseOrder.id == CompanyReceipt.purchase_order_id)
            .filter(CompanyReceipt.company_id == company.id, CompanyPurchaseOrder.company_id == company.id)
            .order_by(CompanyReceipt.receipt_date.desc(), CompanyReceipt.id.desc())
            .all()
        )
        ap_result = build_company_party_aging(
            documents,
            suppliers,
            party_type="supplier",
            target_allocation_totals=company_allocation_totals(allocations, field_name="target_document_id"),
        )
        procurement = build_company_procurement_summary(projects, purchase_orders, receipts, ap_result["all_rows"], suppliers)
        reviews = (
            session.query(CompanyProcurementReview)
            .filter(CompanyProcurementReview.company_id == company.id)
            .order_by(CompanyProcurementReview.updated_at.desc(), CompanyProcurementReview.id.desc())
            .all()
        )
        assigned_user_ids = {int(item.assigned_user_id) for item in reviews if item.assigned_user_id}
        users_by_id = {}
        if assigned_user_ids:
            users_by_id = {
                item.id: item
                for item in session.query(User).filter(User.id.in_(assigned_user_ids)).all()
            }
        return build_company_procurement_exceptions(
            procurement["all_rows"],
            reviews,
            users_by_id,
            review_state_filter=(review_state or "").strip().lower(),
            assigned_user_id=user.id if mine_only else None,
        )


@app.put("/api/companies/current/procurement-exceptions/review")
def update_current_company_procurement_exception_review(
    payload: CompanyProcurementReviewRequest,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        project = session.query(Project).filter(Project.company_id == company.id, Project.id == payload.project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found for current company")
        supplier_name = (payload.supplier_name or "").strip()
        match_flag = (payload.match_flag or "").strip().lower()
        if not supplier_name or not match_flag:
            raise HTTPException(status_code=400, detail="Supplier and match flag are required")
        review_state = (payload.review_state or "open").strip().lower()
        if review_state not in {"open", "reviewed", "ignored"}:
            raise HTTPException(status_code=400, detail="Unsupported review state")
        review = (
            session.query(CompanyProcurementReview)
            .filter(
                CompanyProcurementReview.company_id == company.id,
                CompanyProcurementReview.project_id == project.id,
                CompanyProcurementReview.supplier_name == supplier_name,
                CompanyProcurementReview.match_flag == match_flag,
            )
            .first()
        )
        if not review:
            review = CompanyProcurementReview(
                user_id=user.id,
                company_id=company.id,
                project_id=project.id,
                supplier_name=supplier_name,
                match_flag=match_flag,
            )
            session.add(review)
        review.user_id = user.id
        review.assigned_user_id = payload.assigned_user_id
        review.review_state = review_state
        review.note = (payload.note or "").strip()
        session.flush()
        assigned_user = session.query(User).filter(User.id == review.assigned_user_id).first() if review.assigned_user_id else None
        return {"review": serialize_company_procurement_review(review, assigned_user)}


@app.get("/api/companies/current/activity")
def get_current_company_activity(limit: int = 100, x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    safe_limit = max(1, min(limit, 300))
    with db_session() as session:
        company = require_current_company(session, user)
        users = session.query(User).all()
        user_map = {item.id: item.username for item in users}
        projects = session.query(Project).filter(Project.company_id == company.id).all()
        project_map = {item.id: item for item in projects}
        documents = (
            session.query(DocumentRecord)
            .join(Project, Project.id == DocumentRecord.project_id)
            .filter(Project.company_id == company.id)
            .all()
        )
        document_map = {item.id: item for item in documents}

        events: List[Dict[str, Any]] = []

        allocations = (
            session.query(CompanyAllocation)
            .filter(CompanyAllocation.company_id == company.id)
            .order_by(CompanyAllocation.created_at.desc(), CompanyAllocation.id.desc())
            .limit(safe_limit)
            .all()
        )
        for item in allocations:
            target = document_map.get(item.target_document_id)
            project = project_map.get(target.project_id) if target and target.project_id else None
            events.append({
                "kind": "allocation",
                "at": item.created_at.isoformat() if item.created_at else "",
                "username": user_map.get(item.user_id, ""),
                "project_name": project.name if project else "",
                "summary": f'{item.allocation_type} allocation {item.amount or "0"} to {target.company_name or target.source_file if target else "document"}',
            })

        billing_events = (
            session.query(CompanyBillingEvent)
            .filter(CompanyBillingEvent.company_id == company.id)
            .order_by(CompanyBillingEvent.created_at.desc(), CompanyBillingEvent.id.desc())
            .limit(safe_limit)
            .all()
        )
        for item in billing_events:
            project = project_map.get(item.project_id)
            events.append({
                "kind": "billing_event",
                "at": item.created_at.isoformat() if item.created_at else "",
                "username": user_map.get(item.user_id, ""),
                "project_name": project.name if project else "",
                "label": item.label or item.event_type,
                "summary": f'{item.event_type} {item.label or ""} {item.amount or "0"} {item.status}'.strip(),
            })

        purchase_orders = (
            session.query(CompanyPurchaseOrder)
            .filter(CompanyPurchaseOrder.company_id == company.id)
            .order_by(CompanyPurchaseOrder.created_at.desc(), CompanyPurchaseOrder.id.desc())
            .limit(safe_limit)
            .all()
        )
        for item in purchase_orders:
            project = project_map.get(item.project_id)
            events.append({
                "kind": "purchase_order",
                "at": item.created_at.isoformat() if item.created_at else "",
                "username": user_map.get(item.user_id, ""),
                "project_name": project.name if project else "",
                "reference": item.po_number,
                "summary": f'PO {item.po_number or item.id} {item.amount or "0"} {item.status} | {item.note or item.cost_code or ""}'.strip(" |"),
            })

        receipts = (
            session.query(CompanyReceipt)
            .join(CompanyPurchaseOrder, CompanyPurchaseOrder.id == CompanyReceipt.purchase_order_id)
            .filter(CompanyReceipt.company_id == company.id, CompanyPurchaseOrder.company_id == company.id)
            .order_by(CompanyReceipt.created_at.desc(), CompanyReceipt.id.desc())
            .limit(safe_limit)
            .all()
        )
        po_map = {item.id: item for item in purchase_orders}
        if len(po_map) < len(receipts):
            extra_po_ids = {item.purchase_order_id for item in receipts if item.purchase_order_id not in po_map}
            if extra_po_ids:
                for po in session.query(CompanyPurchaseOrder).filter(CompanyPurchaseOrder.id.in_(extra_po_ids)).all():
                    po_map[po.id] = po
        for item in receipts:
            po = po_map.get(item.purchase_order_id)
            project = project_map.get(po.project_id) if po else None
            events.append({
                "kind": "receipt",
                "at": item.created_at.isoformat() if item.created_at else "",
                "username": user_map.get(item.user_id, ""),
                "project_name": project.name if project else "",
                "reference": item.receipt_number,
                "summary": f'{item.receipt_type} {item.receipt_number or item.id} {item.amount or "0"} {item.status}',
            })

        procurement_reviews = (
            session.query(CompanyProcurementReview)
            .filter(CompanyProcurementReview.company_id == company.id)
            .order_by(CompanyProcurementReview.updated_at.desc(), CompanyProcurementReview.id.desc())
            .limit(safe_limit)
            .all()
        )
        for item in procurement_reviews:
            project = project_map.get(item.project_id)
            assigned_username = user_map.get(item.assigned_user_id, "") if item.assigned_user_id else ""
            assignment_suffix = f" -> {assigned_username}" if assigned_username else ""
            note_suffix = f" | {item.note}" if (item.note or "").strip() else ""
            events.append({
                "kind": "procurement_review",
                "at": item.updated_at.isoformat() if item.updated_at else "",
                "username": user_map.get(item.user_id, ""),
                "project_name": project.name if project else "",
                "counterparty": item.supplier_name,
                "summary": f'{item.match_flag}: {item.review_state}{assignment_suffix} | {item.supplier_name}{note_suffix}',
            })

        dimensions = (
            session.query(CompanyDimension)
            .filter(CompanyDimension.company_id == company.id)
            .order_by(CompanyDimension.created_at.desc(), CompanyDimension.id.desc())
            .limit(max(1, safe_limit // 3))
            .all()
        )
        for item in dimensions:
            events.append({
                "kind": "dimension",
                "at": item.created_at.isoformat() if item.created_at else "",
                "username": user_map.get(item.user_id, ""),
                "summary": f'{item.dimension_type}: {item.code or item.name}',
            })

        parties = (
            session.query(CompanyParty)
            .filter(CompanyParty.company_id == company.id)
            .order_by(CompanyParty.created_at.desc(), CompanyParty.id.desc())
            .limit(max(1, safe_limit // 3))
            .all()
        )
        for item in parties:
            events.append({
                "kind": "party",
                "at": item.created_at.isoformat() if item.created_at else "",
                "username": user_map.get(item.user_id, ""),
                "counterparty": item.name,
                "summary": f'{item.party_type}: {item.name}',
            })

        events.sort(key=lambda item: item.get("at", ""), reverse=True)
        return {"events": events[:safe_limit]}


@app.get("/api/companies/current/ap-documents")
def get_current_company_ap_documents(
    page: int = 1,
    page_size: int = 15,
    query: str = "",
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        suppliers = (
            session.query(CompanyParty)
            .filter(CompanyParty.company_id == company.id, CompanyParty.party_type == "supplier")
            .order_by(CompanyParty.name.asc(), CompanyParty.id.asc())
            .all()
        )
        documents = (
            session.query(DocumentRecord)
            .join(Project, Project.id == DocumentRecord.project_id)
            .filter(Project.company_id == company.id)
            .order_by(DocumentRecord.date.desc(), DocumentRecord.created_at.desc(), DocumentRecord.id.desc())
            .all()
        )
        allocations = (
            session.query(CompanyAllocation)
            .filter(CompanyAllocation.company_id == company.id, CompanyAllocation.allocation_type == "payable")
            .order_by(CompanyAllocation.created_at.desc(), CompanyAllocation.id.desc())
            .all()
        )
        result = build_company_party_aging(
            documents,
            suppliers,
            party_type="supplier",
            target_allocation_totals=company_allocation_totals(allocations, field_name="target_document_id"),
        )
        rows = result["all_rows"]
        q = (query or "").strip().lower()
        if q:
            rows = [
                item for item in rows
                if q in " ".join([
                    item.get("party_name", ""),
                    item.get("company_name", ""),
                    item.get("source_file", ""),
                    item.get("doc_type", ""),
                    item.get("date", ""),
                    item.get("due_date", ""),
                    item.get("project_code", ""),
                    item.get("cost_center", ""),
                    item.get("account_code", ""),
                    item.get("status", ""),
                ]).lower()
            ]
        safe_page = max(1, page)
        safe_page_size = max(1, min(page_size, 100))
        total = len(rows)
        start = (safe_page - 1) * safe_page_size
        paged_rows = rows[start:start + safe_page_size]
        return {
            "rows": paged_rows,
            "pagination": {
                "page": safe_page,
                "page_size": safe_page_size,
                "total": total,
                "total_pages": max(1, (total + safe_page_size - 1) // safe_page_size),
            },
        }


@app.get("/api/companies/current/ar-documents")
def get_current_company_ar_documents(
    page: int = 1,
    page_size: int = 15,
    query: str = "",
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        customers = (
            session.query(CompanyParty)
            .filter(CompanyParty.company_id == company.id, CompanyParty.party_type == "customer")
            .order_by(CompanyParty.name.asc(), CompanyParty.id.asc())
            .all()
        )
        documents = (
            session.query(DocumentRecord)
            .join(Project, Project.id == DocumentRecord.project_id)
            .filter(Project.company_id == company.id)
            .order_by(DocumentRecord.date.desc(), DocumentRecord.created_at.desc(), DocumentRecord.id.desc())
            .all()
        )
        allocations = (
            session.query(CompanyAllocation)
            .filter(CompanyAllocation.company_id == company.id, CompanyAllocation.allocation_type == "receivable")
            .order_by(CompanyAllocation.created_at.desc(), CompanyAllocation.id.desc())
            .all()
        )
        result = build_company_party_aging(
            documents,
            customers,
            party_type="customer",
            target_allocation_totals=company_allocation_totals(allocations, field_name="target_document_id"),
        )
        rows = result["all_rows"]
        q = (query or "").strip().lower()
        if q:
            rows = [
                item for item in rows
                if q in " ".join([
                    item.get("party_name", ""),
                    item.get("company_name", ""),
                    item.get("source_file", ""),
                    item.get("doc_type", ""),
                    item.get("date", ""),
                    item.get("due_date", ""),
                    item.get("project_code", ""),
                    item.get("cost_center", ""),
                    item.get("account_code", ""),
                    item.get("status", ""),
                ]).lower()
            ]
        safe_page = max(1, page)
        safe_page_size = max(1, min(page_size, 100))
        total = len(rows)
        start = (safe_page - 1) * safe_page_size
        paged_rows = rows[start:start + safe_page_size]
        return {
            "rows": paged_rows,
            "pagination": {
                "page": safe_page,
                "page_size": safe_page_size,
                "total": total,
                "total_pages": max(1, (total + safe_page_size - 1) // safe_page_size),
            },
        }


@app.get("/api/companies/current/allocation-workspace")
def get_current_company_allocation_workspace(
    allocation_type: str = "payable",
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    normalized_type = (allocation_type or "payable").strip().lower()
    if normalized_type not in {"payable", "receivable"}:
        raise HTTPException(status_code=400, detail="Allocation type must be payable or receivable")
    with db_session() as session:
        company = require_current_company(session, user)
        parties = (
            session.query(CompanyParty)
            .filter(
                CompanyParty.company_id == company.id,
                CompanyParty.party_type == ("supplier" if normalized_type == "payable" else "customer"),
            )
            .order_by(CompanyParty.name.asc(), CompanyParty.id.asc())
            .all()
        )
        documents = (
            session.query(DocumentRecord)
            .join(Project, Project.id == DocumentRecord.project_id)
            .filter(Project.company_id == company.id)
            .order_by(DocumentRecord.date.desc(), DocumentRecord.created_at.desc(), DocumentRecord.id.desc())
            .all()
        )
        allocations = (
            session.query(CompanyAllocation)
            .filter(CompanyAllocation.company_id == company.id, CompanyAllocation.allocation_type == normalized_type)
            .order_by(CompanyAllocation.created_at.desc(), CompanyAllocation.id.desc())
            .all()
        )
        return build_company_allocation_workspace(documents, parties, allocations, allocation_type=normalized_type)


@app.post("/api/companies/current/allocations")
def create_current_company_allocation(
    payload: CompanyAllocationRequest,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    allocation_type = (payload.allocation_type or "payable").strip().lower()
    if allocation_type not in {"payable", "receivable"}:
        raise HTTPException(status_code=400, detail="Allocation type must be payable or receivable")
    with db_session() as session:
        company = require_current_company(session, user)
        payment_document, payment_project, _ = require_document_access(session, payload.payment_document_id, user, min_role="reviewer")
        target_document, target_project, _ = require_document_access(session, payload.target_document_id, user, min_role="reviewer")
        if getattr(payment_project, "company_id", None) != company.id or getattr(target_project, "company_id", None) != company.id:
            raise HTTPException(status_code=400, detail="Allocation documents must belong to the current company")
        amount_value = processor.amount_to_float(payload.amount) or 0.0
        if amount_value <= 0:
            raise HTTPException(status_code=400, detail="Allocation amount must be greater than zero")
        existing = (
            session.query(CompanyAllocation)
            .filter(CompanyAllocation.company_id == company.id, CompanyAllocation.allocation_type == allocation_type)
            .all()
        )
        payment_totals = company_allocation_totals(existing, field_name="payment_document_id")
        target_totals = company_allocation_totals(existing, field_name="target_document_id")
        payment_total = processor.amount_to_float(payment_document.amount) or 0.0
        target_total = processor.amount_to_float(target_document.amount) or 0.0
        payment_remaining = max(0.0, round(payment_total - payment_totals.get(payment_document.id, 0.0), 2))
        target_remaining = max(0.0, round(target_total - target_totals.get(target_document.id, 0.0), 2))
        if amount_value > payment_remaining + 0.0001:
            raise HTTPException(status_code=400, detail="Allocation exceeds remaining payment amount")
        if amount_value > target_remaining + 0.0001:
            raise HTTPException(status_code=400, detail="Allocation exceeds target outstanding amount")
        item = CompanyAllocation(
            user_id=user.id,
            company_id=company.id,
            allocation_type=allocation_type,
            payment_document_id=payment_document.id,
            target_document_id=target_document.id,
            amount=f"{amount_value:.2f}",
            note=(payload.note or "").strip(),
        )
        session.add(item)
        session.flush()
        return {"allocation": serialize_company_allocation(item)}


@app.delete("/api/companies/current/allocations/{allocation_id}")
def delete_current_company_allocation(allocation_id: int, x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        item = (
            session.query(CompanyAllocation)
            .filter(CompanyAllocation.company_id == company.id, CompanyAllocation.id == allocation_id)
            .first()
        )
        if not item:
            raise HTTPException(status_code=404, detail="Allocation not found")
        session.delete(item)
        return {"deleted": True, "allocation_id": allocation_id}


@app.get("/api/companies/current/job-costing-summary")
def get_current_company_job_costing_summary(x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        projects = (
            session.query(Project)
            .filter(Project.company_id == company.id)
            .order_by(Project.name.asc(), Project.id.asc())
            .all()
        )
        documents = (
            session.query(DocumentRecord)
            .join(Project, Project.id == DocumentRecord.project_id)
            .filter(Project.company_id == company.id)
            .order_by(DocumentRecord.date.desc(), DocumentRecord.created_at.desc(), DocumentRecord.id.desc())
            .all()
        )
        billing_events = (
            session.query(CompanyBillingEvent)
            .filter(CompanyBillingEvent.company_id == company.id)
            .order_by(CompanyBillingEvent.event_date.desc(), CompanyBillingEvent.id.desc())
            .all()
        )
        purchase_orders = (
            session.query(CompanyPurchaseOrder)
            .filter(CompanyPurchaseOrder.company_id == company.id)
            .order_by(CompanyPurchaseOrder.po_date.desc(), CompanyPurchaseOrder.id.desc())
            .all()
        )
        return build_company_job_costing_summary(projects, documents, billing_events, purchase_orders)


@app.get("/api/companies/current/billing-events")
def list_current_company_billing_events(x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        projects = (
            session.query(Project)
            .filter(Project.company_id == company.id)
            .order_by(Project.name.asc(), Project.id.asc())
            .all()
        )
        project_map = {project.id: project for project in projects}
        events = (
            session.query(CompanyBillingEvent)
            .filter(CompanyBillingEvent.company_id == company.id)
            .order_by(CompanyBillingEvent.event_date.desc(), CompanyBillingEvent.id.desc())
            .all()
        )
        return {"events": [serialize_company_billing_event(item, project_map.get(item.project_id)) for item in events]}


@app.post("/api/companies/current/billing-events")
def create_current_company_billing_event(
    payload: CompanyBillingEventRequest,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        project = session.query(Project).filter(Project.company_id == company.id, Project.id == payload.project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found for current company")
        event_type = (payload.event_type or "progress_claim").strip().lower()
        if event_type not in {"progress_claim", "milestone", "variation", "retention_invoice", "debit_note", "credit_note"}:
            raise HTTPException(status_code=400, detail="Unsupported billing event type")
        status = (payload.status or "draft").strip().lower()
        if status not in {"draft", "certified", "billed", "collected", "cancelled"}:
            raise HTTPException(status_code=400, detail="Unsupported billing event status")
        amount_value = processor.amount_to_float(payload.amount)
        if amount_value is None or amount_value <= 0:
            raise HTTPException(status_code=400, detail="Billing event amount must be greater than zero")
        event_date = (payload.event_date or "").strip()
        if not event_date:
            raise HTTPException(status_code=400, detail="Billing event date is required")
        item = CompanyBillingEvent(
            user_id=user.id,
            company_id=company.id,
            project_id=project.id,
            event_type=event_type,
            label=(payload.label or "").strip(),
            event_date=event_date,
            amount=f"{amount_value:.2f}",
            status=status,
            note=(payload.note or "").strip(),
        )
        session.add(item)
        session.flush()
        return {"event": serialize_company_billing_event(item, project)}


@app.delete("/api/companies/current/billing-events/{event_id}")
def delete_current_company_billing_event(event_id: int, x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        item = (
            session.query(CompanyBillingEvent)
            .filter(CompanyBillingEvent.company_id == company.id, CompanyBillingEvent.id == event_id)
            .first()
        )
        if not item:
            raise HTTPException(status_code=404, detail="Billing event not found")
        session.delete(item)
        return {"deleted": True, "event_id": event_id}


@app.get("/api/companies/current/purchase-orders")
def list_current_company_purchase_orders(x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        projects = (
            session.query(Project)
            .filter(Project.company_id == company.id)
            .order_by(Project.name.asc(), Project.id.asc())
            .all()
        )
        suppliers = (
            session.query(CompanyParty)
            .filter(CompanyParty.company_id == company.id, CompanyParty.party_type == "supplier")
            .order_by(CompanyParty.name.asc(), CompanyParty.id.asc())
            .all()
        )
        project_map = {project.id: project for project in projects}
        supplier_map = {party.id: party for party in suppliers}
        orders = (
            session.query(CompanyPurchaseOrder)
            .filter(CompanyPurchaseOrder.company_id == company.id)
            .order_by(CompanyPurchaseOrder.po_date.desc(), CompanyPurchaseOrder.id.desc())
            .all()
        )
        return {"orders": [serialize_company_purchase_order(item, project_map.get(item.project_id), supplier_map.get(item.supplier_party_id)) for item in orders]}


@app.post("/api/companies/current/purchase-orders")
def create_current_company_purchase_order(
    payload: CompanyPurchaseOrderRequest,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        project = session.query(Project).filter(Project.company_id == company.id, Project.id == payload.project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found for current company")
        supplier = None
        if payload.supplier_party_id:
            supplier = session.query(CompanyParty).filter(
                CompanyParty.company_id == company.id,
                CompanyParty.party_type == "supplier",
                CompanyParty.id == payload.supplier_party_id,
            ).first()
            if not supplier:
                raise HTTPException(status_code=404, detail="Supplier not found for current company")
        amount_value = processor.amount_to_float(payload.amount)
        if amount_value is None or amount_value <= 0:
            raise HTTPException(status_code=400, detail="Purchase order amount must be greater than zero")
        status = (payload.status or "open").strip().lower()
        if status not in {"draft", "open", "approved", "partially_received", "closed", "cancelled"}:
            raise HTTPException(status_code=400, detail="Unsupported purchase order status")
        po_date = (payload.po_date or "").strip()
        if not po_date:
            raise HTTPException(status_code=400, detail="Purchase order date is required")
        item = CompanyPurchaseOrder(
            user_id=user.id,
            company_id=company.id,
            project_id=project.id,
            supplier_party_id=payload.supplier_party_id,
            cost_code=(payload.cost_code or "").strip(),
            po_number=(payload.po_number or "").strip(),
            po_date=po_date,
            amount=f"{amount_value:.2f}",
            status=status,
            note=(payload.note or "").strip(),
        )
        session.add(item)
        session.flush()
        return {"order": serialize_company_purchase_order(item, project, supplier)}


@app.delete("/api/companies/current/purchase-orders/{order_id}")
def delete_current_company_purchase_order(order_id: int, x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        item = (
            session.query(CompanyPurchaseOrder)
            .filter(CompanyPurchaseOrder.company_id == company.id, CompanyPurchaseOrder.id == order_id)
            .first()
        )
        if not item:
            raise HTTPException(status_code=404, detail="Purchase order not found")
        session.delete(item)
        return {"deleted": True, "order_id": order_id}


@app.get("/api/companies/current/receipts")
def list_current_company_receipts(x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        orders = (
            session.query(CompanyPurchaseOrder)
            .filter(CompanyPurchaseOrder.company_id == company.id)
            .order_by(CompanyPurchaseOrder.po_date.desc(), CompanyPurchaseOrder.id.desc())
            .all()
        )
        order_map = {item.id: item for item in orders}
        projects = (
            session.query(Project)
            .filter(Project.company_id == company.id)
            .order_by(Project.name.asc(), Project.id.asc())
            .all()
        )
        project_map = {item.id: item for item in projects}
        receipts = (
            session.query(CompanyReceipt)
            .filter(CompanyReceipt.company_id == company.id)
            .order_by(CompanyReceipt.receipt_date.desc(), CompanyReceipt.id.desc())
            .all()
        )
        return {"receipts": [serialize_company_receipt(item, order_map.get(item.purchase_order_id), project_map.get(getattr(order_map.get(item.purchase_order_id), "project_id", 0))) for item in receipts]}


@app.post("/api/companies/current/receipts")
def create_current_company_receipt(
    payload: CompanyReceiptRequest,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        order = (
            session.query(CompanyPurchaseOrder)
            .filter(CompanyPurchaseOrder.company_id == company.id, CompanyPurchaseOrder.id == payload.purchase_order_id)
            .first()
        )
        if not order:
            raise HTTPException(status_code=404, detail="Purchase order not found")
        amount_value = processor.amount_to_float(payload.amount)
        if amount_value is None or amount_value <= 0:
            raise HTTPException(status_code=400, detail="Receipt amount must be greater than zero")
        receipt_type = (payload.receipt_type or "goods_receipt").strip().lower()
        if receipt_type not in {"goods_receipt", "service_receipt"}:
            raise HTTPException(status_code=400, detail="Unsupported receipt type")
        status = (payload.status or "received").strip().lower()
        if status not in {"received", "partial", "cancelled"}:
            raise HTTPException(status_code=400, detail="Unsupported receipt status")
        receipt_date = (payload.receipt_date or "").strip()
        if not receipt_date:
            raise HTTPException(status_code=400, detail="Receipt date is required")
        item = CompanyReceipt(
            user_id=user.id,
            company_id=company.id,
            purchase_order_id=order.id,
            receipt_type=receipt_type,
            receipt_number=(payload.receipt_number or "").strip(),
            receipt_date=receipt_date,
            amount=f"{amount_value:.2f}",
            status=status,
            note=(payload.note or "").strip(),
        )
        session.add(item)
        session.flush()
        project = session.query(Project).filter(Project.id == order.project_id).first()
        return {"receipt": serialize_company_receipt(item, order, project)}


@app.delete("/api/companies/current/receipts/{receipt_id}")
def delete_current_company_receipt(receipt_id: int, x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        item = (
            session.query(CompanyReceipt)
            .filter(CompanyReceipt.company_id == company.id, CompanyReceipt.id == receipt_id)
            .first()
        )
        if not item:
            raise HTTPException(status_code=404, detail="Receipt not found")
        session.delete(item)
        return {"deleted": True, "receipt_id": receipt_id}


@app.post("/api/companies/current/dimensions")
def create_current_company_dimension(
    payload: CompanyDimensionRequest,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        dimension_type = (payload.dimension_type or "project_code").strip().lower()
        if dimension_type not in {"project_code", "cost_center", "cost_code"}:
            raise HTTPException(status_code=400, detail="Dimension type must be project_code, cost_center, or cost_code")
        code = (payload.code or "").strip()
        if not code:
            raise HTTPException(status_code=400, detail="Dimension code is required")
        existing = (
            session.query(CompanyDimension)
            .filter(
                CompanyDimension.company_id == company.id,
                CompanyDimension.dimension_type == dimension_type,
                CompanyDimension.code == code,
            )
            .first()
        )
        if existing:
            raise HTTPException(status_code=400, detail="Dimension code already exists")
        item = CompanyDimension(
            user_id=user.id,
            company_id=company.id,
            dimension_type=dimension_type,
            code=code,
            name=(payload.name or "").strip(),
            is_active=bool(payload.is_active),
        )
        session.add(item)
        session.flush()
        return {"dimension": serialize_company_dimension(item)}


@app.delete("/api/companies/current/dimensions/{dimension_id}")
def delete_current_company_dimension(dimension_id: int, x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        item = session.query(CompanyDimension).filter(CompanyDimension.company_id == company.id, CompanyDimension.id == dimension_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Dimension not found")
        session.delete(item)
        return {"deleted": True, "dimension_id": dimension_id}


@app.post("/api/companies/current/manual-journal")
def create_current_company_manual_journal(
    payload: ManualJournalRequest,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        anchor_project = require_company_anchor_project(session, company, user)
        periods = (
            session.query(AccountingPeriod)
            .filter(AccountingPeriod.company_id == company.id)
            .order_by(AccountingPeriod.start_date.asc(), AccountingPeriod.id.asc())
            .all()
        )
        period = company_period_for_date(periods, payload.entry_date)
        if not period:
            raise HTTPException(status_code=400, detail="No accounting period covers this entry date")
        if (period.status or "").strip().lower() != "open":
            raise HTTPException(status_code=400, detail=f'Posting blocked because period "{period.name}" is {(period.status or "").strip().lower()}.')

        account_codes = {
            item.code
            for item in session.query(AccountingAccount.code).filter(AccountingAccount.company_id == company.id).all()
        }
        cleaned_lines: List[Dict[str, Any]] = []
        total_debit = 0.0
        total_credit = 0.0
        for line in payload.lines:
            account_code = (line.account_code or "").strip()
            if not account_code:
                continue
            if account_code not in account_codes:
                raise HTTPException(status_code=400, detail=f"Unknown account code: {account_code}")
            debit_value = processor.amount_to_float(line.debit) or 0.0
            credit_value = processor.amount_to_float(line.credit) or 0.0
            if debit_value <= 0 and credit_value <= 0:
                continue
            if debit_value > 0 and credit_value > 0:
                raise HTTPException(status_code=400, detail=f"Line for account {account_code} cannot have both debit and credit")
            total_debit += debit_value
            total_credit += credit_value
            cleaned_lines.append({
                "account_code": account_code,
                "debit": f"{debit_value:.2f}" if debit_value > 0 else "",
                "credit": f"{credit_value:.2f}" if credit_value > 0 else "",
                "project_code": (line.project_code or "").strip(),
                "cost_center": (line.cost_center or "").strip(),
            })
        if len(cleaned_lines) < 2:
            raise HTTPException(status_code=400, detail="Manual journal requires at least two non-empty lines")
        if round(total_debit, 2) != round(total_credit, 2):
            raise HTTPException(status_code=400, detail="Manual journal is not balanced")

        entry = JournalEntry(
            user_id=user.id,
            company_id=company.id,
            project_id=anchor_project.id,
            document_id=None,
            entry_date=(payload.entry_date or "").strip(),
            reference=(payload.reference or "").strip(),
            memo=(payload.memo or "").strip(),
            status="posted",
        )
        session.add(entry)
        session.flush()
        for line in cleaned_lines:
            session.add(JournalEntryLine(
                entry_id=entry.id,
                account_code=line["account_code"],
                debit=line["debit"],
                credit=line["credit"],
                cost_center=line["cost_center"],
                project_code=line["project_code"],
            ))
        session.flush()
        _ = entry.lines
        return {"entry": serialize_journal_entry(entry)}


@app.post("/api/projects/{project_id}/periods")
def create_project_period(
    project_id: int,
    payload: AccountingPeriodRequest,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="admin")
        company = ensure_project_company(session, project, user)
        status = (payload.status or "open").strip().lower()
        if status not in {"open", "closed", "locked"}:
            raise HTTPException(status_code=400, detail="Invalid period status")
        period = AccountingPeriod(
            user_id=user.id,
            company_id=company.id,
            project_id=project.id,
            name=(payload.name or "").strip(),
            start_date=(payload.start_date or "").strip(),
            end_date=(payload.end_date or "").strip(),
            status=status,
        )
        session.add(period)
        session.flush()
        return {"period": serialize_period(period)}


@app.post("/api/companies/current/periods")
def create_current_company_period(
    payload: AccountingPeriodRequest,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        anchor_project = require_company_anchor_project(session, company, user)
        status = (payload.status or "open").strip().lower()
        if status not in {"open", "closed", "locked"}:
            raise HTTPException(status_code=400, detail="Invalid period status")
        period = AccountingPeriod(
            user_id=user.id,
            company_id=company.id,
            project_id=anchor_project.id,
            name=(payload.name or "").strip(),
            start_date=(payload.start_date or "").strip(),
            end_date=(payload.end_date or "").strip(),
            status=status,
        )
        session.add(period)
        session.flush()
        return {"period": serialize_period(period)}


@app.post("/api/companies/current/periods/seed-quarters")
def seed_current_company_quarter_periods(
    payload: QuarterSeedRequest,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        anchor_project = require_company_anchor_project(session, company, user)
        year = int(payload.year)
        status = (payload.status or "open").strip().lower()
        if year < 2000 or year > 2100:
            raise HTTPException(status_code=400, detail="Invalid year")
        if status not in {"open", "closed", "locked"}:
            raise HTTPException(status_code=400, detail="Invalid period status")
        quarter_specs = [
            (f"Q1 {year}", f"{year}-01-01", f"{year}-03-31"),
            (f"Q2 {year}", f"{year}-04-01", f"{year}-06-30"),
            (f"Q3 {year}", f"{year}-07-01", f"{year}-09-30"),
            (f"Q4 {year}", f"{year}-10-01", f"{year}-12-31"),
        ]
        existing_names = {
            item.name
            for item in session.query(AccountingPeriod.name).filter(AccountingPeriod.company_id == company.id).all()
        }
        created: List[AccountingPeriod] = []
        for name, start_date, end_date in quarter_specs:
            if name in existing_names:
                continue
            period = AccountingPeriod(
                user_id=user.id,
                company_id=company.id,
                project_id=anchor_project.id,
                name=name,
                start_date=start_date,
                end_date=end_date,
                status=status,
            )
            session.add(period)
            created.append(period)
        session.flush()
        return {
            "created_count": len(created),
            "periods": [serialize_period(item) for item in created],
        }


@app.post("/api/companies/current/periods/seed-missing-drafts")
def seed_current_company_missing_draft_periods(
    payload: MissingPeriodSeedRequest,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        anchor_project = require_company_anchor_project(session, company, user)
        status = (payload.status or "open").strip().lower()
        if status not in {"open", "closed", "locked"}:
            raise HTTPException(status_code=400, detail="Invalid period status")
        project_ids = [item.id for item in session.query(Project.id).filter(Project.company_id == company.id).all()]
        periods = (
            session.query(AccountingPeriod)
            .filter(AccountingPeriod.company_id == company.id)
            .order_by(AccountingPeriod.start_date.asc(), AccountingPeriod.id.asc())
            .all()
        )
        company_rules = (
            session.query(CompanyAccountingRule)
            .filter(CompanyAccountingRule.company_id == company.id)
            .order_by(CompanyAccountingRule.created_at.asc(), CompanyAccountingRule.id.asc())
            .all()
        )
        project_rules_map: Dict[int, List[ProjectRule]] = {}
        if project_ids:
            for rule in (
                session.query(ProjectRule)
                .filter(ProjectRule.project_id.in_(project_ids))
                .order_by(ProjectRule.project_id.asc(), ProjectRule.created_at.asc(), ProjectRule.id.asc())
                .all()
            ):
                project_rules_map.setdefault(int(rule.project_id), []).append(rule)
        posted_document_ids = {
            item.document_id
            for item in session.query(JournalEntry.document_id)
            .filter(JournalEntry.company_id == company.id, JournalEntry.status == "posted")
            .all()
            if item.document_id
        }
        documents = (
            session.query(DocumentRecord)
            .filter(DocumentRecord.project_id.in_(project_ids if project_ids else [-1]))
            .order_by(DocumentRecord.date.asc(), DocumentRecord.created_at.asc(), DocumentRecord.id.asc())
            .all()
        )
        missing_quarters: Dict[str, Tuple[str, str, str]] = {}
        undated_count = 0
        undated_samples: List[str] = []
        for document in documents:
            if document.id in posted_document_ids:
                continue
            draft = journal_draft_for_document(
                document,
                combined_accounting_rules(project_rules_map.get(int(document.project_id), []), company_rules),
            )
            if not draft:
                continue
            annotated = annotate_draft_with_period(draft, periods)
            if annotated.get("posting_allowed") or annotated.get("period_status") != "missing":
                continue
            draft_date = (annotated.get("date") or "").strip()
            if not draft_date or draft_date == "Unknown":
                undated_count += 1
                if len(undated_samples) < 5:
                    undated_samples.append(document.canonical_company_name or document.company_name or document.source_file or f"Document {document.id}")
                continue
            try:
                date_obj = datetime.strptime(draft_date, "%Y-%m-%d")
            except ValueError:
                undated_count += 1
                if len(undated_samples) < 5:
                    undated_samples.append(document.canonical_company_name or document.company_name or document.source_file or f"Document {document.id}")
                continue
            quarter_index = ((date_obj.month - 1) // 3) + 1
            start_month = ((quarter_index - 1) * 3) + 1
            end_month = start_month + 2
            end_day = calendar.monthrange(date_obj.year, end_month)[1]
            quarter_key = f"{date_obj.year:04d}-Q{quarter_index}"
            missing_quarters[quarter_key] = (
                f"Q{quarter_index} {date_obj.year}",
                f"{date_obj.year:04d}-{start_month:02d}-01",
                f"{date_obj.year:04d}-{end_month:02d}-{end_day:02d}",
            )
        created: List[AccountingPeriod] = []
        existing_names = {
            item.name
            for item in session.query(AccountingPeriod.name).filter(AccountingPeriod.company_id == company.id).all()
        }
        for _, (name, start_date, end_date) in sorted(missing_quarters.items()):
            if name in existing_names:
                continue
            period = AccountingPeriod(
                user_id=user.id,
                company_id=company.id,
                project_id=anchor_project.id,
                name=name,
                start_date=start_date,
                end_date=end_date,
                status=status,
            )
            session.add(period)
            created.append(period)
        session.flush()
        return {
            "created_count": len(created),
            "periods": [serialize_period(item) for item in created],
            "undated_count": undated_count,
            "undated_samples": undated_samples,
        }


@app.put("/api/projects/{project_id}/periods/{period_id}")
def update_project_period(
    project_id: int,
    period_id: int,
    payload: AccountingPeriodRequest,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="admin")
        company = ensure_project_company(session, project, user)
        period = (
            session.query(AccountingPeriod)
            .filter(AccountingPeriod.company_id == company.id, AccountingPeriod.id == period_id)
            .first()
        )
        if not period:
            raise HTTPException(status_code=404, detail="Period not found")
        status = (payload.status or "open").strip().lower()
        if status not in {"open", "closed", "locked"}:
            raise HTTPException(status_code=400, detail="Invalid period status")
        period.name = (payload.name or "").strip()
        period.start_date = (payload.start_date or "").strip()
        period.end_date = (payload.end_date or "").strip()
        period.status = status
        session.flush()
        return {"period": serialize_period(period)}


@app.put("/api/companies/current/periods/{period_id}")
def update_current_company_period(
    period_id: int,
    payload: AccountingPeriodRequest,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        company = require_current_company(session, user)
        period = (
            session.query(AccountingPeriod)
            .filter(AccountingPeriod.company_id == company.id, AccountingPeriod.id == period_id)
            .first()
        )
        if not period:
            raise HTTPException(status_code=404, detail="Period not found")
        status = (payload.status or "open").strip().lower()
        if status not in {"open", "closed", "locked"}:
            raise HTTPException(status_code=400, detail="Invalid period status")
        period.name = (payload.name or "").strip()
        period.start_date = (payload.start_date or "").strip()
        period.end_date = (payload.end_date or "").strip()
        period.status = status
        session.flush()
        return {"period": serialize_period(period)}


@app.post("/api/projects/{project_id}/members")
def add_project_member(
    project_id: int,
    payload: ProjectMemberRequest,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    allowed_roles = {"owner", "admin", "reviewer", "viewer"}
    role = (payload.role or "reviewer").strip().lower()
    if role not in allowed_roles:
        raise HTTPException(status_code=400, detail="Unsupported project role")
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="admin")
        target_user = (
            session.query(User)
            .filter(func.lower(User.username) == payload.username.strip().lower())
            .first()
        )
        if not target_user:
            raise HTTPException(status_code=404, detail="User not found")
        existing = (
            session.query(ProjectMember)
            .filter(ProjectMember.project_id == project.id, ProjectMember.user_id == target_user.id)
            .first()
        )
        if existing:
            existing.role = role
            session.flush()
            return {"member": serialize_project_member(existing, target_user)}
        member = ProjectMember(project_id=project.id, user_id=target_user.id, role=role)
        session.add(member)
        session.flush()
        return {"member": serialize_project_member(member, target_user)}


@app.delete("/api/projects/{project_id}/members/{member_id}")
def remove_project_member(
    project_id: int,
    member_id: int,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="viewer")
        member = (
            session.query(ProjectMember)
            .filter(ProjectMember.id == member_id, ProjectMember.project_id == project.id)
            .first()
        )
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
        if member.user_id == user.id:
            raise HTTPException(status_code=400, detail="Owner membership cannot be removed here")
        session.delete(member)
        return {"deleted": True, "member_id": member_id}


@app.post("/api/projects/{project_id}/rebuild-reconciliation")
def rebuild_project_reconciliation(project_id: int, x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="reviewer")

        documents = (
            session.query(DocumentRecord)
            .filter(DocumentRecord.project_id == project.id)
            .order_by(DocumentRecord.created_at.asc(), DocumentRecord.id.asc())
            .all()
        )
        if not documents:
            return {"ok": True, "updated": 0}

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
                transaction_direction=document.transaction_direction,
                project_name=project.project_name,
                confidence_score=document.confidence_score,
                confidence_label=document.confidence_label,
                raw_text=document.raw_text,
                match_status=document.match_status,
                match_score=document.match_score,
                matched_record_source_file=document.matched_record_source_file,
                matched_record_output_file=document.matched_record_output_file,
                matched_record_source_type=document.matched_record_source_type,
                matched_record_source_timestamp=document.matched_record_source_timestamp,
                matched_record_date=document.matched_record_date,
                matched_record_number=document.matched_record_number,
                matched_record_company_name=document.matched_record_company_name,
                matched_record_amount=document.matched_record_amount,
                matched_record_transaction_direction=document.matched_record_transaction_direction,
                match_basis=document.match_basis,
            )
            for document in documents
        ]

        processor.reconcile_bank_transactions(records)

        for document, record in zip(documents, records):
            document.match_status = record.match_status
            document.match_score = record.match_score
            document.matched_record_source_file = record.matched_record_source_file
            document.matched_record_output_file = record.matched_record_output_file
            document.matched_record_source_type = record.matched_record_source_type
            document.matched_record_source_timestamp = record.matched_record_source_timestamp
            document.matched_record_date = record.matched_record_date
            document.matched_record_number = record.matched_record_number
            document.matched_record_company_name = record.matched_record_company_name
            document.matched_record_amount = record.matched_record_amount
            document.matched_record_transaction_direction = record.matched_record_transaction_direction
            document.match_basis = record.match_basis

        return {"ok": True, "updated": len(documents)}


@app.put("/api/documents/{document_id}")
def update_document(
    document_id: int,
    request: DocumentUpdateRequest,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        document, project, _ = require_document_access(session, document_id, user, min_role="reviewer")

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

        return {"document": serialize_document(document)}


@app.get("/api/projects/{project_id}/documents")
def project_documents(
    project_id: int,
    page: int = 1,
    page_size: int = 2500,
    search: str = "",
    source_type: str = "",
    doc_type: str = "",
    confidence_label: str = "",
    match_status: str = "",
    company: str = "",
    direction: str = "",
    bank: str = "",
    date_from: str = "",
    date_to: str = "",
    only_bank: bool = False,
    mode: str = "all",
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="viewer")
        query = document_query_for_project(session, project.id)
        query = apply_document_filters(
            query,
            search=search,
            source_type=source_type,
            doc_type=doc_type,
            confidence_label=confidence_label,
            match_status=match_status,
            company=company,
            direction=direction,
            bank=bank,
            date_from=date_from,
            date_to=date_to,
            only_bank=only_bank,
        )
        order_query = query.order_by(DocumentRecord.created_at.desc(), DocumentRecord.id.desc())
        safe_page, safe_page_size, total, documents = paginate_query(order_query, page, page_size)
        payload = {
            "documents": [serialize_document(document) for document in documents],
            "pagination": {
                "page": safe_page,
                "page_size": safe_page_size,
                "total": total,
                "total_pages": max(1, (total + safe_page_size - 1) // safe_page_size),
            },
        }
        if mode == "filters":
            base_documents = document_query_for_project(session, project.id).all()
            payload["filters"] = {
                "doc_types": sorted({item.doc_type for item in base_documents if item.doc_type}),
                "source_types": sorted({item.source_type for item in base_documents if item.source_type}),
                "banks": sorted({normalized_bank_name(item.source_timestamp) for item in base_documents if item.source_timestamp}),
                "companies": sorted(
                    {
                        item.canonical_company_name or item.company_name
                        for item in base_documents
                        if item.company_name or item.canonical_company_name
                    }
                ),
            }
        return payload


@app.get("/api/projects/{project_id}/dashboard/bank")
def project_bank_dashboard(
    project_id: int,
    search: str = "",
    direction: str = "",
    match_status: str = "",
    bank: str = "",
    date_from: str = "",
    date_to: str = "",
    drilldown_mode: str = "all",
    drilldown_value: str = "",
    drilldown_search: str = "",
    drilldown_direction: str = "",
    drilldown_match: str = "",
    page: int = 1,
    page_size: int = 25,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="viewer")

        rules = (
            session.query(ProjectRule)
            .filter(ProjectRule.project_id == project.id)
            .order_by(ProjectRule.created_at.asc(), ProjectRule.id.asc())
            .all()
        )
        vendor_alias_map = {
            item.normalized_key: item.canonical_name
            for item in session.query(VendorAlias)
            .filter(VendorAlias.project_id == project.id)
            .all()
        }
        documents = (
            document_query_for_project(session, project.id)
            .filter(DocumentRecord.source_type == "sheet", DocumentRecord.doc_type == "BankTransaction")
            .order_by(DocumentRecord.date.desc(), DocumentRecord.id.desc())
            .all()
        )
        records = [bank_dashboard_record(document, rules, vendor_alias_map) for document in documents]

        search_value = search.strip().lower()

        def matches_top_filters(item: Dict[str, Any]) -> bool:
            date_value = item["date"] if re.match(r"^\d{4}-\d{2}-\d{2}$", item.get("date", "")) else ""
            if search_value:
                haystack = " ".join(
                    [
                        item.get("bank_name", ""),
                        item.get("date", ""),
                        item.get("number", ""),
                        item.get("company_name", ""),
                        item.get("canonical_vendor_name", ""),
                        item.get("amount", ""),
                        item.get("dashboard_match_status", ""),
                        item.get("match_basis", ""),
                        item.get("raw_text", ""),
                    ]
                ).lower()
                if search_value not in haystack:
                    return False
            if date_from and (not date_value or date_value < date_from):
                return False
            if date_to and (not date_value or date_value > date_to):
                return False
            if direction and item.get("resolved_direction") != direction:
                return False
            if match_status and item.get("dashboard_match_status") != match_status:
                return False
            if bank and item.get("bank_name") != bank:
                return False
            return True

        filtered = [item for item in records if matches_top_filters(item)]

        debit_records = [item for item in filtered if item.get("resolved_direction") == "debit"]
        credit_records = [item for item in filtered if item.get("resolved_direction") == "credit"]
        unknown_direction_records = [item for item in filtered if item.get("resolved_direction") == "unknown"]
        matched_debit_records = [item for item in debit_records if item.get("dashboard_match_status") == "matched"]
        missing_debit_records = [item for item in debit_records if item.get("dashboard_match_status") == "missing_receipt"]
        receipt_relevant_debit_records = [item for item in debit_records if item.get("dashboard_match_status") != "not_applicable"]

        def amount_value(item: Dict[str, Any]) -> float:
            return processor.amount_to_float(item.get("amount")) or 0.0

        total_debit = sum(amount_value(item) for item in debit_records)
        total_credit = sum(amount_value(item) for item in credit_records)
        unmatched_debit_amount = sum(amount_value(item) for item in missing_debit_records)
        matched_debit_amount = sum(amount_value(item) for item in matched_debit_records)
        coverage = (
            (len(matched_debit_records) / len(receipt_relevant_debit_records)) * 100
            if receipt_relevant_debit_records else 0.0
        )

        monthly_map: Dict[str, Dict[str, float]] = {}
        for item in filtered:
            month = item["date"][:7] if re.match(r"^\d{4}-\d{2}-\d{2}$", item.get("date", "")) else "Unknown"
            bucket = monthly_map.setdefault(month, {"debit": 0.0, "credit": 0.0, "missing": 0.0, "matched": 0.0})
            amount = amount_value(item)
            if item.get("resolved_direction") == "debit":
                bucket["debit"] += amount
                if item.get("dashboard_match_status") == "missing_receipt":
                    bucket["missing"] += amount
                if item.get("dashboard_match_status") == "matched":
                    bucket["matched"] += amount
            elif item.get("resolved_direction") == "credit":
                bucket["credit"] += amount

        bank_map: Dict[str, Dict[str, float]] = {}
        for item in filtered:
            bank_name = item.get("bank_name") or "Unknown"
            bucket = bank_map.setdefault(bank_name, {"count": 0, "debit": 0.0, "credit": 0.0, "relevant_debit": 0, "matched_debit": 0})
            bucket["count"] += 1
            amount = amount_value(item)
            if item.get("resolved_direction") == "debit":
                bucket["debit"] += amount
                if item.get("dashboard_match_status") != "not_applicable":
                    bucket["relevant_debit"] += 1
                if item.get("dashboard_match_status") == "matched":
                    bucket["matched_debit"] += 1
            elif item.get("resolved_direction") == "credit":
                bucket["credit"] += amount

        vendor_map: Dict[str, Dict[str, float]] = {}
        for item in missing_debit_records:
            vendor_name = item.get("canonical_vendor_name") or "Unknown"
            bucket = vendor_map.setdefault(vendor_name, {"count": 0, "amount": 0.0})
            bucket["count"] += 1
            bucket["amount"] += amount_value(item)

        category_map: Dict[str, Dict[str, float]] = {}
        for item in debit_records:
            key = item.get("resolved_category") or "Uncategorized"
            if item.get("resolved_subcategory"):
                key = f"{key} / {item['resolved_subcategory']}"
            bucket = category_map.setdefault(key, {"count": 0, "amount": 0.0})
            bucket["count"] += 1
            bucket["amount"] += amount_value(item)

        anomaly_rows = [
            item for item in filtered
            if item.get("confidence_label") == "low"
            or item.get("dashboard_match_status") == "missing_receipt"
            or item.get("review_state") == "missing_receipt"
        ]
        anomaly_rows.sort(key=amount_value, reverse=True)
        attention_rows = sorted(missing_debit_records, key=amount_value, reverse=True)[:10]
        exception_cases: List[Dict[str, Any]] = []
        if drilldown_mode == "exception":
            exception_cases = build_exception_cases(documents, rules, vendor_alias_map)

        def unresolved_aging_bucket(item: Dict[str, Any]) -> str:
            date_value = item.get("date") or ""
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_value):
                return "Unknown date"
            try:
                age_days = (date.today() - datetime.strptime(date_value, "%Y-%m-%d").date()).days
            except ValueError:
                return "Unknown date"
            if age_days <= 7:
                return "0-7 days"
            if age_days <= 30:
                return "8-30 days"
            if age_days <= 60:
                return "31-60 days"
            if age_days <= 90:
                return "61-90 days"
            return "91+ days"

        def apply_drilldown_scope(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
            if drilldown_mode in {"", "all"}:
                scoped = rows
            elif drilldown_mode == "debit":
                scoped = [item for item in rows if item.get("resolved_direction") == "debit"]
            elif drilldown_mode == "credit":
                scoped = [item for item in rows if item.get("resolved_direction") == "credit"]
            elif drilldown_mode == "unknown":
                scoped = [item for item in rows if item.get("resolved_direction") == "unknown"]
            elif drilldown_mode == "receipt_relevant_debit":
                scoped = [item for item in rows if item.get("resolved_direction") == "debit" and item.get("dashboard_match_status") != "not_applicable"]
            elif drilldown_mode == "matched_debit":
                scoped = [item for item in rows if item.get("resolved_direction") == "debit" and item.get("dashboard_match_status") == "matched"]
            elif drilldown_mode == "credits_na":
                scoped = [item for item in rows if item.get("resolved_direction") == "credit" and item.get("dashboard_match_status") == "not_applicable"]
            elif drilldown_mode == "match":
                scoped = [item for item in rows if item.get("dashboard_match_status") == drilldown_value]
            elif drilldown_mode == "month":
                scoped = [item for item in rows if (item.get("date") or "").startswith(drilldown_value)]
            elif drilldown_mode == "bank":
                scoped = [item for item in rows if item.get("bank_name") == drilldown_value]
            elif drilldown_mode == "vendor_missing":
                scoped = [item for item in rows if item.get("dashboard_match_status") == "missing_receipt" and item.get("canonical_vendor_name") == drilldown_value]
            elif drilldown_mode == "category":
                scoped = [
                    item for item in rows
                    if dashboard_category_key(item) == drilldown_value
                ]
            elif drilldown_mode == "aging":
                unresolved_candidates = [
                    item for item in rows
                    if item.get("dashboard_match_status") == "missing_receipt"
                    or item.get("review_state") == "missing_receipt"
                    or item.get("confidence_label") == "low"
                ]
                scoped = [item for item in unresolved_candidates if unresolved_aging_bucket(item) == drilldown_value]
            elif drilldown_mode == "exception":
                related_ids: set[int] = set()
                for case in exception_cases:
                    case_type = case.get("type") or ""
                    if (
                        (drilldown_value == "installment" and case_type == "installment_chain")
                        or (drilldown_value == "refund" and case_type == "refund_pair")
                        or (drilldown_value == "split" and case_type == "split_payment_group")
                        or (drilldown_value == "duplicate" and case_type == "duplicate_cluster")
                        or (drilldown_value == "mismatch" and case_type == "amount_mismatch_case")
                    ):
                        for row in case.get("rows", []):
                            row_id = row.get("id")
                            if row_id is not None:
                                related_ids.add(int(row_id))
                scoped = [item for item in rows if int(item.get("id") or 0) in related_ids]
            elif drilldown_mode == "focus":
                scoped = [item for item in rows if str(item.get("id")) == drilldown_value]
            else:
                scoped = rows

            drilldown_search_value = drilldown_search.strip().lower()
            if drilldown_search_value:
                scoped = [
                    item for item in scoped
                    if drilldown_search_value in " ".join(
                        [
                            item.get("bank_name", ""),
                            item.get("date", ""),
                            item.get("number", ""),
                            item.get("company_name", ""),
                            item.get("canonical_vendor_name", ""),
                            item.get("amount", ""),
                            item.get("dashboard_match_status", ""),
                            item.get("match_basis", ""),
                            item.get("raw_text", ""),
                        ]
                    ).lower()
                ]
            if drilldown_direction:
                scoped = [item for item in scoped if item.get("resolved_direction") == drilldown_direction]
            if drilldown_match:
                scoped = [item for item in scoped if item.get("dashboard_match_status") == drilldown_match]
            return scoped

        drilldown_rows = apply_drilldown_scope(filtered)
        safe_page = max(1, page)
        safe_page_size = max(1, min(page_size, 100))
        total = len(drilldown_rows)
        start = (safe_page - 1) * safe_page_size
        paged_rows = drilldown_rows[start:start + safe_page_size]

        return {
            "analytics": {
                "totals": {
                    "bank_transactions": len(filtered),
                    "total_debit": total_debit,
                    "total_credit": total_credit,
                    "coverage_pct": coverage,
                    "missing_receipt_debit": unmatched_debit_amount,
                    "matched_debit_amount": matched_debit_amount,
                    "banks_count": len(bank_map),
                    "credits_not_applicable": len([item for item in credit_records if item.get("dashboard_match_status") == "not_applicable"]),
                },
                "counts": {
                    "debit": len(debit_records),
                    "credit": len(credit_records),
                    "unknown": len(unknown_direction_records),
                    "matched": len([item for item in filtered if item.get("dashboard_match_status") == "matched"]),
                    "missing_receipt": len([item for item in filtered if item.get("dashboard_match_status") == "missing_receipt"]),
                    "not_applicable": len([item for item in filtered if item.get("dashboard_match_status") == "not_applicable"]),
                    "receipt_relevant_debit": len(receipt_relevant_debit_records),
                    "matched_debit": len(matched_debit_records),
                    "missing_debit": len(missing_debit_records),
                },
                "monthly": [
                    {"month": key, **values}
                    for key, values in sorted(monthly_map.items(), key=lambda item: str(item[0]))[-12:]
                ],
                "banks": [
                    {
                        "bank": key,
                        **values,
                        "match_rate": ((values["matched_debit"] / values["relevant_debit"]) * 100) if values["relevant_debit"] else 0.0,
                    }
                    for key, values in sorted(bank_map.items(), key=lambda item: (item[1]["debit"] + item[1]["credit"]), reverse=True)
                ],
                "vendors": [
                    {"vendor": key, **values}
                    for key, values in sorted(vendor_map.items(), key=lambda item: item[1]["amount"], reverse=True)[:8]
                ],
                "categories": [
                    {"category": key, **values}
                    for key, values in sorted(category_map.items(), key=lambda item: item[1]["amount"], reverse=True)[:8]
                ],
                "attention": attention_rows,
                "anomalies": anomaly_rows[:8],
            },
            "filters": {
                "banks": sorted({item.get("bank_name") or "Unknown" for item in records}),
            },
            "drilldown": {
                "rows": paged_rows,
                "pagination": {
                    "page": safe_page,
                    "page_size": safe_page_size,
                    "total": total,
                    "total_pages": max(1, (total + safe_page_size - 1) // safe_page_size),
                },
            },
        }


@app.get("/api/projects/{project_id}/reconciliation")
def project_reconciliation_queue(
    project_id: int,
    search: str = "",
    status: str = "attention",
    bank: str = "",
    sort: str = "priority",
    page: int = 1,
    page_size: int = 12,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="reviewer")
        rules = (
            session.query(ProjectRule)
            .filter(ProjectRule.project_id == project.id)
            .order_by(ProjectRule.created_at.asc(), ProjectRule.id.asc())
            .all()
        )
        vendor_alias_map = {
            item.normalized_key: item.canonical_name
            for item in session.query(VendorAlias)
            .filter(VendorAlias.project_id == project.id)
            .all()
        }
        documents = (
            document_query_for_project(session, project.id)
            .filter(DocumentRecord.source_type == "sheet", DocumentRecord.doc_type == "BankTransaction")
            .order_by(DocumentRecord.date.desc(), DocumentRecord.id.desc())
            .all()
        )
        records = [bank_dashboard_record(document, rules, vendor_alias_map) for document in documents]
        reviewed_count = sum(1 for document in documents if (document.review_state or "") not in {"", "unreviewed"})
        needs_review_records = [
            item for item, document in zip(records, documents)
            if item.get("resolved_direction") == "debit"
            and effective_reconciliation_status(document, rules) not in {"matched", "not_applicable", "reviewed"}
        ]
        missing_amount = sum(processor.amount_to_float(item.get("amount")) or 0.0 for item in needs_review_records)
        query = search.strip().lower()
        filtered: List[Dict[str, Any]] = []
        for item in records:
            item_status = item.get("review_state") if item.get("review_state") and item.get("review_state") != "unreviewed" else item.get("dashboard_match_status")
            item_status = item_status or "unreviewed"
            matches_query = (
                not query
                or query in " ".join([
                    item.get("bank_name", ""),
                    item.get("date", ""),
                    item.get("number", ""),
                    item.get("company_name", ""),
                    item.get("amount", ""),
                    item.get("match_basis", ""),
                    item.get("raw_text", ""),
                ]).lower()
            )
            matches_status = (
                item.get("resolved_direction") == "debit" and item_status not in {"matched", "not_applicable", "reviewed"}
                if status == "attention"
                else not status or item_status == status
            )
            matches_bank = not bank or item.get("bank_name") == bank
            if matches_query and matches_status and matches_bank:
                filtered.append({**item, "effective_status": item_status})

        def sort_key(item: Dict[str, Any]):
            if sort == "amount_desc":
                return (-(processor.amount_to_float(item.get("amount")) or 0.0),)
            if sort == "date_asc":
                return (str(item.get("date") or ""),)
            if sort == "date_desc":
                return (str(item.get("date") or ""),)
            return (
                reconciliation_priority(item.get("effective_status") or ""),
                -(processor.amount_to_float(item.get("amount")) or 0.0),
                str(item.get("date") or ""),
            )

        reverse = sort == "date_desc"
        filtered = sorted(filtered, key=sort_key, reverse=reverse)
        safe_page = max(1, page)
        safe_page_size = max(1, min(page_size, 100))
        total = len(filtered)
        start = (safe_page - 1) * safe_page_size
        rows = filtered[start:start + safe_page_size]
        return {
            "summary": {
                "needs_review_count": len(needs_review_records),
                "missing_amount": missing_amount,
                "reviewed_count": reviewed_count,
            },
            "filters": {
                "banks": sorted({item.get("bank_name") or "Unknown" for item in records}),
            },
            "rows": rows,
            "pagination": {
                "page": safe_page,
                "page_size": safe_page_size,
                "total": total,
                "total_pages": max(1, (total + safe_page_size - 1) // safe_page_size),
            },
        }


@app.get("/api/projects/{project_id}/review-queue")
def project_review_queue(
    project_id: int,
    search: str = "",
    issue_type: str = "",
    source_type: str = "",
    page: int = 1,
    page_size: int = 12,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="reviewer")
        rules = (
            session.query(ProjectRule)
            .filter(ProjectRule.project_id == project.id)
            .order_by(ProjectRule.created_at.asc(), ProjectRule.id.asc())
            .all()
        )
        vendor_alias_map = {
            item.normalized_key: item.canonical_name
            for item in session.query(VendorAlias)
            .filter(VendorAlias.project_id == project.id)
            .all()
        }
        documents = document_query_for_project(session, project.id).order_by(DocumentRecord.created_at.desc(), DocumentRecord.id.desc()).all()
        issues = build_review_issues(documents, rules, vendor_alias_map)
        query = search.strip().lower()
        filtered = [
            item for item in issues
            if (
                (not query or query in " ".join([item["label"], item["reason"], item["source_file"], item["company_name"], item["amount"], item["source_type"]]).lower())
                and (not issue_type or item["type"] == issue_type)
                and (not source_type or item["source_type"] == source_type)
            )
        ]
        safe_page = max(1, page)
        safe_page_size = max(1, min(page_size, 100))
        total = len(filtered)
        start = (safe_page - 1) * safe_page_size
        rows = filtered[start:start + safe_page_size]
        return {
            "summary": {
                "total": len(issues),
                "low_confidence": sum(1 for item in issues if item["type"] == "low_confidence"),
                "duplicates": sum(1 for item in issues if item["type"] in {"duplicate_suspect", "repeated_charge"}),
                "parsing": sum(1 for item in issues if item["type"] in {"parsing_issue", "refund_or_reversal", "credit_needs_review"}),
            },
            "filters": {
                "source_types": sorted({item["source_type"] for item in issues if item["source_type"]}),
            },
            "rows": rows,
            "pagination": {
                "page": safe_page,
                "page_size": safe_page_size,
                "total": total,
                "total_pages": max(1, (total + safe_page_size - 1) // safe_page_size),
            },
        }


@app.get("/api/projects/{project_id}/resources")
def project_resources(
    project_id: int,
    page: int = 1,
    page_size: int = 12,
    search: str = "",
    source_type: str = "",
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="viewer")
        documents = (
            document_query_for_project(session, project.id)
            .order_by(DocumentRecord.created_at.desc(), DocumentRecord.id.desc())
            .all()
        )
        resource_items = build_project_resources(documents)
        if search:
            search_lower = search.strip().lower()
            resource_items = [
                item for item in resource_items
                if search_lower in " ".join(
                    [
                        item["source_type"],
                        item["source_path"],
                        item["source_file"],
                        item["source_origin"],
                        item["date_from"],
                        item["date_to"],
                    ]
                ).lower()
            ]
        if source_type:
            resource_items = [item for item in resource_items if item["source_type"] == source_type]
        for item in resource_items:
            item.pop("records", None)
        resource_items.sort(key=lambda item: (item["source_type"], item["source_file"]))
        safe_page = max(1, page)
        # Some project analytics views need a larger server response than the paged
        # operational tables. Keep pagination, but allow a higher ceiling here.
        safe_page_size = max(1, min(page_size, 10000))
        total = len(resource_items)
        start = (safe_page - 1) * safe_page_size
        items = resource_items[start:start + safe_page_size]
        return {
            "resources": items,
            "pagination": {
                "page": safe_page,
                "page_size": safe_page_size,
                "total": total,
                "total_pages": max(1, (total + safe_page_size - 1) // safe_page_size),
            },
            "filters": {
                "source_types": sorted({item["source_type"] for item in resource_items if item["source_type"]}),
            },
        }


@app.get("/api/projects/{project_id}/resource-detail")
def project_resource_detail(
    project_id: int,
    key: str,
    page: int = 1,
    page_size: int = 12,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="viewer")
        documents = (
            document_query_for_project(session, project.id)
            .order_by(DocumentRecord.created_at.desc(), DocumentRecord.id.desc())
            .all()
        )
        resource_documents = [document for document in documents if build_resource_key(document) == key]
        resources = build_project_resources(documents)
        resource = next((item for item in resources if item["key"] == key), None)
        if not resource:
            raise HTTPException(status_code=404, detail="Resource not found")
        records = resource.get("records", [])
        document_ids = [document.id for document in resource_documents]
        low_confidence_count = sum(1 for item in records if item.get("confidence_label") == "low")
        missing_receipt_count = sum(1 for item in records if item.get("match_status") == "missing_receipt")
        parsing_warnings = sum(
            1 for item in records
            if not item.get("date") or item.get("date") == "Unknown"
            or not item.get("company_name") or item.get("company_name") == "Unknown"
            or not item.get("amount") or item.get("amount") == "Unknown"
        )
        matched_count = sum(1 for item in records if item.get("match_status") in {"matched", "linked_to_bank"})
        direction_profiles = len({
            (item.get("transaction_direction") or "unknown").lower()
            if (item.get("transaction_direction") or "").lower() in {"debit", "credit"}
            else "unknown"
            for item in records
        })
        warning_items: List[str] = []
        if low_confidence_count:
            warning_items.append(f"{low_confidence_count} low confidence record{'s' if low_confidence_count != 1 else ''}")
        if missing_receipt_count:
            warning_items.append(f"{missing_receipt_count} record{'s' if missing_receipt_count != 1 else ''} still missing receipt support")
        if parsing_warnings:
            warning_items.append(f"{parsing_warnings} parsing warning{'s' if parsing_warnings != 1 else ''}")
        if matched_count == 0 and resource.get("record_count", 0):
            warning_items.append("No linked matches found for this source yet")
        if direction_profiles <= 1 and resource.get("source_type") == "sheet":
            warning_items.append("Only one transaction direction detected in this sheet")

        activity: List[Dict[str, Any]] = []
        if resource_documents:
            earliest = min((document.created_at for document in resource_documents if document.created_at), default=None)
            if earliest:
                activity.append({
                    "kind": "ingested",
                    "at": earliest.isoformat(),
                    "summary": f"Imported {len(resource_documents)} record{'s' if len(resource_documents) != 1 else ''} from this source",
                })
        if document_ids:
            user_map = {
                item.id: item.username
                for item in session.query(User).all()
            }
            comments = (
                session.query(ProjectComment)
                .filter(ProjectComment.project_id == project.id, ProjectComment.document_id.in_(document_ids))
                .order_by(ProjectComment.created_at.desc())
                .limit(20)
                .all()
            )
            for item in comments:
                activity.append({
                    "kind": "comment",
                    "at": item.created_at.isoformat() if item.created_at else "",
                    "summary": item.body,
                    "username": user_map.get(item.user_id, ""),
                })
            attachments = (
                session.query(DocumentAttachment)
                .filter(DocumentAttachment.project_id == project.id, DocumentAttachment.document_id.in_(document_ids))
                .order_by(DocumentAttachment.created_at.desc())
                .limit(20)
                .all()
            )
            for item in attachments:
                activity.append({
                    "kind": "attachment",
                    "at": item.created_at.isoformat() if item.created_at else "",
                    "summary": f"{item.label or item.file_name} attached",
                    "username": user_map.get(item.user_id, ""),
                })
        for document in resource_documents:
            if document.review_updated_at and document.review_state and document.review_state != "unreviewed":
                activity.append({
                    "kind": "review",
                    "at": document.review_updated_at.isoformat(),
                    "summary": f"{document.review_state}: {document.company_name or document.source_file}",
                    "username": user_map.get(document.user_id, "") if 'user_map' in locals() else "",
                })
        activity.sort(key=lambda item: item.get("at", ""), reverse=True)
        safe_page = max(1, page)
        safe_page_size = max(1, min(page_size, 100))
        total = len(records)
        start = (safe_page - 1) * safe_page_size
        paged_records = records[start:start + safe_page_size]
        resource_summary = {k: v for k, v in resource.items() if k != "records"}
        return {
            "resource": resource_summary,
            "diagnostics": {
                "low_confidence_count": low_confidence_count,
                "missing_receipt_count": missing_receipt_count,
                "parsing_warnings": parsing_warnings,
                "matched_count": matched_count,
                "direction_profiles": direction_profiles,
                "warnings": warning_items,
            },
            "activity": activity[:20],
            "records": paged_records,
            "pagination": {
                "page": safe_page,
                "page_size": safe_page_size,
                "total": total,
                "total_pages": max(1, (total + safe_page_size - 1) // safe_page_size),
            },
        }


@app.put("/api/documents/{document_id}/review")
def update_document_review(
    document_id: int,
    request: ReviewUpdateRequest,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        document, _, _ = require_document_access(session, document_id, user, min_role="reviewer")
        document.review_state = request.review_state.strip() or "unreviewed"
        document.review_note = request.review_note.strip()
        document.review_updated_at = datetime.now()
        return {"document": serialize_document(document)}


@app.put("/api/documents/{document_id}/tags")
def update_document_tags(
    document_id: int,
    request: DocumentTagsUpdateRequest,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        document, _, _ = require_document_access(session, document_id, user, min_role="reviewer")
        document.canonical_company_name = request.canonical_company_name.strip()
        document.category = request.category.strip()
        document.subcategory = request.subcategory.strip()
        document.account_code = request.account_code.strip()
        document.offset_account_code = request.offset_account_code.strip()
        document.cost_code = request.cost_code.strip()
        document.cost_center = request.cost_center.strip()
        document.project_code = request.project_code.strip()
        document.purchase_order_id = int(request.purchase_order_id) if request.purchase_order_id else None
        document.payment_method = request.payment_method.strip()
        document.vat_flag = request.vat_flag
        return {"document": serialize_document(document)}


@app.put("/api/documents/{document_id}/assignment")
def update_document_assignment(
    document_id: int,
    request: DocumentAssignmentRequest,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        document, _, _ = require_document_access(session, document_id, user, min_role="reviewer")
        if request.assigned_user_id:
            member = (
                session.query(ProjectMember)
                .filter(
                    ProjectMember.project_id == document.project_id,
                    ProjectMember.user_id == request.assigned_user_id,
                )
                .first()
            )
            if not member:
                raise HTTPException(status_code=400, detail="Assigned user is not a member of this project")
            document.assigned_user_id = request.assigned_user_id
        else:
            document.assigned_user_id = None
        assigned_user = session.query(User).filter(User.id == document.assigned_user_id).first() if document.assigned_user_id else None
        payload = serialize_document(document)
        payload["assigned_username"] = assigned_user.username if assigned_user else ""
        return {"document": payload}


@app.get("/api/projects/{project_id}/rules")
def list_project_rules(project_id: int, x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="viewer")
        rules = (
            session.query(ProjectRule)
            .filter(ProjectRule.project_id == project.id)
            .order_by(ProjectRule.created_at.asc(), ProjectRule.id.asc())
            .all()
        )
        return {"rules": [serialize_accounting_rule(rule, "project") for rule in rules]}


@app.post("/api/projects/{project_id}/rules")
def create_project_rule(
    project_id: int,
    payload: ProjectRuleRequest,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="admin")
        rule = ProjectRule(
            user_id=user.id,
            project_id=project.id,
            keyword=payload.keyword.strip(),
            source_type=payload.source_type.strip(),
            status=payload.status.strip(),
            category=payload.category.strip(),
            subcategory=payload.subcategory.strip(),
            account_code=payload.account_code.strip(),
            offset_account_code=payload.offset_account_code.strip(),
            project_code=payload.project_code.strip(),
            cost_code=payload.cost_code.strip(),
            cost_center=payload.cost_center.strip(),
            payment_method=payload.payment_method.strip(),
            vat_flag=payload.vat_flag,
            auto_post=payload.auto_post,
        )
        session.add(rule)
        session.flush()
        return {"rule": serialize_accounting_rule(rule, "project")}


@app.post("/api/projects/{project_id}/rules/seed-accounting")
def seed_project_accounting_rules(project_id: int, x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="reviewer")
        existing_rules = (
            session.query(ProjectRule)
            .filter(ProjectRule.project_id == project.id)
            .order_by(ProjectRule.created_at.asc(), ProjectRule.id.asc())
            .all()
        )
        existing_keys = {
            ((item.keyword or "").strip().lower(), (item.source_type or "").strip().lower())
            for item in existing_rules
        }
        created: List[ProjectRule] = []

        for spec in seeded_accounting_rule_specs():
            key = ((spec.get("keyword") or "").strip().lower(), (spec.get("source_type") or "").strip().lower())
            if not key[0] or key in existing_keys:
                continue
            rule = ProjectRule(
                user_id=user.id,
                project_id=project.id,
                keyword=spec.get("keyword", "").strip(),
                source_type=spec.get("source_type", "").strip(),
                status=spec.get("status", "").strip(),
                category=spec.get("category", "").strip(),
                subcategory=spec.get("subcategory", "").strip(),
                account_code=spec.get("account_code", "").strip(),
                offset_account_code=spec.get("offset_account_code", "").strip(),
                project_code=spec.get("project_code", "").strip(),
                cost_code=spec.get("cost_code", "").strip(),
                cost_center=spec.get("cost_center", "").strip(),
                payment_method=spec.get("payment_method", "").strip(),
                vat_flag=bool(spec.get("vat_flag", False)),
                auto_post=bool(spec.get("auto_post", True)),
            )
            session.add(rule)
            created.append(rule)
            existing_keys.add(key)

        documents = (
            session.query(DocumentRecord)
            .filter(DocumentRecord.project_id == project.id)
            .order_by(DocumentRecord.created_at.desc(), DocumentRecord.id.desc())
            .all()
        )
        inferred_candidates: Dict[Tuple[str, str], Dict[str, Any]] = {}
        for document in documents:
            spec = infer_rule_spec_from_document(document)
            if not spec:
                continue
            key = ((spec.get("keyword") or "").strip().lower(), (spec.get("source_type") or "").strip().lower())
            if not key[0] or key in existing_keys:
                continue
            if key not in inferred_candidates:
                inferred_candidates[key] = spec
            if len(inferred_candidates) >= 25:
                break

        for spec in inferred_candidates.values():
            rule = ProjectRule(
                user_id=user.id,
                project_id=project.id,
                keyword=spec.get("keyword", "").strip(),
                source_type=spec.get("source_type", "").strip(),
                status=spec.get("status", "").strip(),
                category=spec.get("category", "").strip(),
                subcategory=spec.get("subcategory", "").strip(),
                account_code=spec.get("account_code", "").strip(),
                offset_account_code=spec.get("offset_account_code", "").strip(),
                project_code=spec.get("project_code", "").strip(),
                cost_code=spec.get("cost_code", "").strip(),
                cost_center=spec.get("cost_center", "").strip(),
                payment_method=spec.get("payment_method", "").strip(),
                vat_flag=bool(spec.get("vat_flag", False)),
                auto_post=bool(spec.get("auto_post", True)),
            )
            session.add(rule)
            created.append(rule)
            existing_keys.add(((spec.get("keyword") or "").strip().lower(), (spec.get("source_type") or "").strip().lower()))

        session.flush()
        return {"created_count": len(created), "rules": [serialize_accounting_rule(rule, "project") for rule in created]}


@app.delete("/api/projects/{project_id}/rules/{rule_id}")
def delete_project_rule(project_id: int, rule_id: int, x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="admin")
        rule = (
            session.query(ProjectRule)
            .filter(ProjectRule.id == rule_id, ProjectRule.project_id == project.id)
            .first()
        )
        if not rule:
            raise HTTPException(status_code=404, detail="Rule not found")
        session.delete(rule)
        return {"deleted": True, "rule_id": rule_id}


@app.get("/api/projects/{project_id}/vendor-aliases")
def list_vendor_aliases(project_id: int, x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="viewer")
        aliases = (
            session.query(VendorAlias)
            .filter(VendorAlias.project_id == project.id)
            .order_by(VendorAlias.created_at.asc(), VendorAlias.id.asc())
            .all()
        )
        return {"aliases": [serialize_vendor_alias(alias) for alias in aliases]}


@app.post("/api/projects/{project_id}/vendor-aliases")
def upsert_vendor_alias(
    project_id: int,
    payload: VendorAliasRequest,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="admin")
        normalized_key = payload.normalized_key.strip()
        if not normalized_key:
            raise HTTPException(status_code=400, detail="normalized_key is required")
        alias = (
            session.query(VendorAlias)
            .filter(VendorAlias.project_id == project.id, VendorAlias.normalized_key == normalized_key)
            .first()
        )
        if not alias:
            alias = VendorAlias(
                user_id=user.id,
                project_id=project.id,
                normalized_key=normalized_key,
            )
            session.add(alias)
        alias.canonical_name = payload.canonical_name.strip()
        session.flush()
        return {"alias": serialize_vendor_alias(alias)}


@app.delete("/api/projects/{project_id}/vendor-aliases/{alias_id}")
def delete_vendor_alias(project_id: int, alias_id: int, x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="admin")
        alias = (
            session.query(VendorAlias)
            .filter(VendorAlias.id == alias_id, VendorAlias.project_id == project.id)
            .first()
        )
        if not alias:
            raise HTTPException(status_code=404, detail="Vendor alias not found")
        session.delete(alias)
        return {"deleted": True, "alias_id": alias_id}


@app.get("/api/projects/{project_id}/comments")
def list_project_comments(
    project_id: int,
    document_id: Optional[int] = None,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="reviewer")
        query = session.query(ProjectComment).filter(ProjectComment.project_id == project.id)
        if document_id:
            query = query.filter(ProjectComment.document_id == document_id)
        comments = query.order_by(ProjectComment.created_at.desc(), ProjectComment.id.desc()).all()
        user_map = {
            item.id: item.username
            for item in session.query(User).filter(User.id.in_([comment.user_id for comment in comments])).all()
        } if comments else {}
        return {"comments": [serialize_comment(comment, user_map.get(comment.user_id, "")) for comment in comments]}


@app.post("/api/projects/{project_id}/comments")
def create_project_comment(
    project_id: int,
    payload: ProjectCommentRequest,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="viewer")
        comment = ProjectComment(
            user_id=user.id,
            project_id=project.id,
            document_id=payload.document_id,
            body=payload.body.strip(),
        )
        session.add(comment)
        session.flush()
        return {"comment": serialize_comment(comment, user.username)}


@app.get("/api/documents/{document_id}/attachments")
def list_document_attachments(document_id: int, x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        document, _, _ = require_document_access(session, document_id, user, min_role="viewer")
        attachments = (
            session.query(DocumentAttachment)
            .filter(DocumentAttachment.document_id == document.id)
            .order_by(DocumentAttachment.created_at.desc(), DocumentAttachment.id.desc())
            .all()
        )
        user_map = {
            item.id: item.username
            for item in session.query(User).filter(User.id.in_([attachment.user_id for attachment in attachments])).all()
        } if attachments else {}
        return {"attachments": [serialize_attachment(item, user_map.get(item.user_id, "")) for item in attachments]}


@app.get("/api/projects/{project_id}/attachment-counts")
def project_attachment_counts(project_id: int, x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="viewer")
        rows = (
            session.query(DocumentAttachment.document_id, func.count(DocumentAttachment.id))
            .filter(DocumentAttachment.project_id == project.id)
            .group_by(DocumentAttachment.document_id)
            .all()
        )
        return {"counts": {str(document_id): count for document_id, count in rows}}


@app.post("/api/documents/{document_id}/attachments")
def create_document_attachment(
    document_id: int,
    payload: AttachmentRequest,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    attachment_type = (payload.attachment_type or "").strip().lower() or "supporting_document"
    allowed_types = {
        "receipt",
        "invoice",
        "screenshot",
        "bank_statement",
        "delivery_note",
        "contract",
        "supporting_document",
        "other",
    }
    if attachment_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid attachment type")
    with db_session() as session:
        document, _, _ = require_document_access(session, document_id, user, min_role="reviewer")
        target = Path(payload.file_path).expanduser().resolve()
        if not target.exists() or not target.is_file():
            raise HTTPException(status_code=404, detail="Attachment file not found")
        attachment = DocumentAttachment(
            user_id=user.id,
            project_id=document.project_id,
            document_id=document.id,
            attachment_type=attachment_type,
            label=payload.label.strip() or target.name,
            file_path=str(target),
            file_name=target.name,
            note=payload.note.strip(),
        )
        session.add(attachment)
        session.flush()
        return {"attachment": serialize_attachment(attachment, user.username)}


@app.delete("/api/documents/{document_id}/attachments/{attachment_id}")
def delete_document_attachment(
    document_id: int,
    attachment_id: int,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        _, project, _ = require_document_access(session, document_id, user, min_role="reviewer")
        attachment = (
            session.query(DocumentAttachment)
            .filter(
                DocumentAttachment.id == attachment_id,
                DocumentAttachment.document_id == document_id,
                DocumentAttachment.project_id == project.id,
            )
            .first()
        )
        if not attachment:
            raise HTTPException(status_code=404, detail="Attachment not found")
        session.delete(attachment)
        return {"deleted": True, "attachment_id": attachment_id}


@app.get("/api/projects/{project_id}/saved-searches")
def list_saved_searches(project_id: int, x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="viewer")
        searches = (
            session.query(SavedSearch)
            .filter(SavedSearch.project_id == project.id)
            .order_by(SavedSearch.created_at.desc(), SavedSearch.id.desc())
            .all()
        )
        return {"saved_searches": [serialize_saved_search(item) for item in searches]}


@app.post("/api/projects/{project_id}/saved-searches")
def create_saved_search(
    project_id: int,
    payload: SavedSearchRequest,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="viewer")
        saved_search = SavedSearch(
            user_id=user.id,
            project_id=project.id,
            name=payload.name.strip(),
            scope=payload.scope.strip() or "global_search",
            query_json=json.dumps(payload.query or {}),
        )
        session.add(saved_search)
        session.flush()
        return {"saved_search": serialize_saved_search(saved_search)}


@app.delete("/api/projects/{project_id}/saved-searches/{saved_search_id}")
def delete_saved_search(project_id: int, saved_search_id: int, x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="viewer")
        saved_search = (
            session.query(SavedSearch)
            .filter(SavedSearch.id == saved_search_id, SavedSearch.project_id == project.id)
            .first()
        )
        if not saved_search:
            raise HTTPException(status_code=404, detail="Saved search not found")
        session.delete(saved_search)
        return {"deleted": True, "saved_search_id": saved_search_id}


@app.post("/api/projects/{project_id}/rerun-resource")
def rerun_project_resource(
    project_id: int,
    payload: ResourceRerunRequest,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    source_path = Path(payload.source_path or "").expanduser().resolve()
    if not source_path.exists() or not source_path.is_file():
        raise HTTPException(status_code=404, detail="Source file not found for rerun")
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="reviewer")
        rerun_root = user_data_root() / "rerun_staging" / f"project_{project.id}"
        rerun_root.mkdir(parents=True, exist_ok=True)
        staged_dir = rerun_root / uuid.uuid4().hex
        staged_dir.mkdir(parents=True, exist_ok=True)
        staged_source = staged_dir / source_path.name
        shutil.copy2(source_path, staged_source)
        resource_document = (
            session.query(DocumentRecord)
            .filter(DocumentRecord.project_id == project.id, DocumentRecord.source_path == str(source_path))
            .order_by(DocumentRecord.created_at.asc(), DocumentRecord.id.asc())
            .first()
        )
        session.add(ProjectComment(
            user_id=user.id,
            project_id=project.id,
            document_id=resource_document.id if resource_document else None,
            body=f"Reran resource: {source_path.name}",
        ))
        request = ProcessRequest(
            project_id=project.id,
            source_dir=str(staged_dir),
            output_dir=project.output_dir,
            debug_image_dir=project.debug_image_dir,
            archive_source_dir="",
            project_name=project.project_name,
            ocr_backend=project.ocr_backend,
            handwriting_backend=project.handwriting_backend,
            trocr_model=project.trocr_model,
            ocr_profile=project.ocr_profile,
            export_image_mode=project.export_image_mode,
            naming_pattern=project.naming_pattern,
            lang=project.lang,
            dpi=project.dpi,
            single_item_per_page=project.single_item_per_page,
            save_text=project.save_text,
            use_angle_cls=project.use_angle_cls,
            move_processed_source=False,
            video_sample_seconds=getattr(project, "video_sample_seconds", 2),
            video_max_frames=getattr(project, "video_max_frames", 120),
            excel_name=project.excel_name,
        )
    job = enqueue_job(user.id, request)
    return {"job_id": job.job_id, "staged_source": str(staged_source)}


@app.get("/api/projects/{project_id}/export-results")
def export_project_results(
    project_id: int,
    format: Literal["csv", "xlsx"] = "csv",
    token: str = "",
    x_auth_token: str = Header(default=""),
) -> FileResponse:
    user = require_user(x_auth_token or token)
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="viewer")

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
            "TransactionDirection",
            "ProjectName",
            "MatchStatus",
            "MatchScore",
            "MatchedRecordSourceFile",
            "MatchedRecordOutputFile",
            "MatchedRecordSourceType",
            "MatchedRecordSourceTimestamp",
            "MatchedRecordDate",
            "MatchedRecordNumber",
            "MatchedRecordCompanyName",
            "MatchedRecordAmount",
            "MatchedRecordTransactionDirection",
            "MatchBasis",
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
                            document.transaction_direction,
                            project.project_name,
                            document.match_status,
                            document.match_score,
                            document.matched_record_source_file,
                            document.matched_record_output_file,
                            document.matched_record_source_type,
                            document.matched_record_source_timestamp,
                            document.matched_record_date,
                            document.matched_record_number,
                            document.matched_record_company_name,
                            document.matched_record_amount,
                            document.matched_record_transaction_direction,
                            document.match_basis,
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
                    transaction_direction=document.transaction_direction,
                    project_name=project.project_name,
                    confidence_score=document.confidence_score,
                    confidence_label=document.confidence_label,
                    raw_text=document.raw_text,
                    match_status=document.match_status,
                    match_score=document.match_score,
                    matched_record_source_file=document.matched_record_source_file,
                    matched_record_output_file=document.matched_record_output_file,
                    matched_record_source_type=document.matched_record_source_type,
                    matched_record_source_timestamp=document.matched_record_source_timestamp,
                    matched_record_date=document.matched_record_date,
                    matched_record_number=document.matched_record_number,
                    matched_record_company_name=document.matched_record_company_name,
                    matched_record_amount=document.matched_record_amount,
                    matched_record_transaction_direction=document.matched_record_transaction_direction,
                    match_basis=document.match_basis,
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
        project, _ = require_project_access(session, project_id, user, min_role="viewer")

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


@app.get("/api/projects/{project_id}/activity")
def project_activity(project_id: int, limit: int = 100, x_auth_token: str = Header(default="")) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    safe_limit = max(1, min(limit, 500))
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="viewer")

        user_rows = session.query(User).all()
        user_map = {item.id: item.username for item in user_rows}
        events: List[Dict[str, Any]] = []
        comments = (
            session.query(ProjectComment)
            .filter(ProjectComment.project_id == project.id)
            .order_by(ProjectComment.created_at.desc())
            .limit(safe_limit)
            .all()
        )
        for item in comments:
            events.append({
                "kind": "comment",
                "at": item.created_at.isoformat() if item.created_at else "",
                "document_id": item.document_id,
                "username": user_map.get(item.user_id, ""),
                "summary": item.body,
            })
        attachments = (
            session.query(DocumentAttachment)
            .filter(DocumentAttachment.project_id == project.id)
            .order_by(DocumentAttachment.created_at.desc())
            .limit(safe_limit)
            .all()
        )
        for item in attachments:
            events.append({
                "kind": "attachment",
                "at": item.created_at.isoformat() if item.created_at else "",
                "document_id": item.document_id,
                "username": user_map.get(item.user_id, ""),
                "summary": f"{item.label or item.file_name} attached",
            })
        searches = (
            session.query(SavedSearch)
            .filter(SavedSearch.project_id == project.id)
            .order_by(SavedSearch.created_at.desc())
            .limit(safe_limit)
            .all()
        )
        for item in searches:
            events.append({
                "kind": "saved_search",
                "at": item.created_at.isoformat() if item.created_at else "",
                "document_id": None,
                "username": user_map.get(item.user_id, ""),
                "summary": f"Saved search: {item.name}",
            })
        reviews = (
            session.query(DocumentRecord)
            .filter(DocumentRecord.project_id == project.id, DocumentRecord.review_updated_at.is_not(None))
            .order_by(DocumentRecord.review_updated_at.desc())
            .limit(safe_limit)
            .all()
        )
        for item in reviews:
            if not item.review_state or item.review_state == "unreviewed":
                continue
            events.append({
                "kind": "review",
                "at": item.review_updated_at.isoformat() if item.review_updated_at else "",
                "document_id": item.id,
                "username": user_map.get(item.user_id, ""),
                "summary": f"{item.review_state}: {item.company_name or item.source_file}",
            })
        procurement_reviews = (
            session.query(CompanyProcurementReview)
            .filter(CompanyProcurementReview.project_id == project.id)
            .order_by(CompanyProcurementReview.updated_at.desc())
            .limit(safe_limit)
            .all()
        )
        for item in procurement_reviews:
            assigned_username = user_map.get(item.assigned_user_id, "") if item.assigned_user_id else ""
            note_suffix = f" | {item.note}" if (item.note or "").strip() else ""
            assignment_suffix = f" -> {assigned_username}" if assigned_username else ""
            events.append({
                "kind": "procurement_review",
                "at": item.updated_at.isoformat() if item.updated_at else "",
                "document_id": None,
                "username": user_map.get(item.user_id, ""),
                "summary": f'procurement {item.match_flag}: {item.review_state}{assignment_suffix} | {item.supplier_name}{note_suffix}',
            })
        events.sort(key=lambda item: item.get("at", ""), reverse=True)
        return {"events": events[:safe_limit]}


@app.get("/api/projects/{project_id}/export-unresolved")
def export_project_unresolved(
    project_id: int,
    token: str = "",
    x_auth_token: str = Header(default=""),
) -> FileResponse:
    user = require_user(x_auth_token or token)
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="viewer")

        documents = (
            session.query(DocumentRecord)
            .filter(
                DocumentRecord.project_id == project.id,
                or_(
                    DocumentRecord.match_status == "missing_receipt",
                    DocumentRecord.review_state == "missing_receipt",
                    DocumentRecord.confidence_label == "low",
                    DocumentRecord.review_state == "reviewed",
                ),
            )
            .order_by(DocumentRecord.created_at.desc(), DocumentRecord.id.desc())
            .all()
        )
        if not documents:
            raise HTTPException(status_code=404, detail="No unresolved rows found for this project")

        export_dir = user_data_root() / "exports"
        export_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        safe_name = processor.sanitize_filename(project.name or "ULTRA_FORCE_Project")
        target = export_dir / f"{safe_name}_unresolved_{stamp}.csv"
        headers = [
            "CreatedAt",
            "SourceType",
            "SourceFile",
            "SourceTimestamp",
            "Type",
            "Date",
            "Number",
            "CompanyName",
            "CanonicalCompanyName",
            "Amount",
            "Currency",
            "TransactionDirection",
            "ConfidenceLabel",
            "MatchStatus",
            "ReviewState",
            "ReviewNote",
            "Category",
            "Subcategory",
            "MatchBasis",
        ]
        with target.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(headers)
            for document in documents:
                writer.writerow(
                    [
                        document.created_at.isoformat() if document.created_at else "",
                        document.source_type,
                        document.source_file,
                        document.source_timestamp,
                        document.doc_type,
                        document.date,
                        document.number,
                        document.company_name,
                        document.canonical_company_name,
                        document.amount,
                        document.currency,
                        document.transaction_direction,
                        document.confidence_label,
                        document.match_status,
                        document.review_state,
                        document.review_note,
                        document.category,
                        document.subcategory,
                        document.match_basis,
                    ]
                )
    return FileResponse(target, media_type="text/csv", filename=target.name)


@app.get("/api/projects/{project_id}/export-accounting")
def export_project_accounting(
    project_id: int,
    preset: str = "ultra_force",
    token: str = "",
    x_auth_token: str = Header(default=""),
) -> FileResponse:
    user = require_user(x_auth_token or token)
    if preset not in ACCOUNTING_EXPORT_PRESETS:
        raise HTTPException(status_code=400, detail="Unsupported accounting export preset")
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="viewer")
        documents = (
            session.query(DocumentRecord)
            .filter(DocumentRecord.project_id == project.id)
            .order_by(DocumentRecord.date.asc(), DocumentRecord.created_at.asc(), DocumentRecord.id.asc())
            .all()
        )
        if not documents:
            raise HTTPException(status_code=404, detail="No stored results found for this project")

        export_dir = user_data_root() / "exports"
        export_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        safe_name = processor.sanitize_filename(project.name or "ULTRA_FORCE_Project")
        target = export_dir / f"{safe_name}_accounting_export_{preset}_{stamp}.csv"
        headers = accounting_export_headers(preset)
        with target.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(headers)
            for document in documents:
                writer.writerow(accounting_export_row(project, document, preset))
    return FileResponse(target, media_type="text/csv", filename=target.name)


@app.get("/api/projects/{project_id}/evidence-pack")
def export_project_evidence_pack(
    project_id: int,
    scope: Literal["all", "selected", "unresolved"] = "all",
    ids: str = "",
    token: str = "",
    x_auth_token: str = Header(default=""),
) -> FileResponse:
    user = require_user(x_auth_token or token)
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="viewer")

        query = session.query(DocumentRecord).filter(DocumentRecord.project_id == project.id)
        if scope == "selected":
            selected_ids = [int(value) for value in ids.split(",") if value.strip().isdigit()]
            if not selected_ids:
                raise HTTPException(status_code=400, detail="No result rows were selected")
            query = query.filter(DocumentRecord.id.in_(selected_ids))
        elif scope == "unresolved":
            query = query.filter(
                or_(
                    DocumentRecord.match_status == "missing_receipt",
                    DocumentRecord.review_state == "missing_receipt",
                    DocumentRecord.confidence_label == "low",
                )
            )
        documents = query.order_by(DocumentRecord.created_at.desc(), DocumentRecord.id.desc()).all()
        if not documents:
            raise HTTPException(status_code=404, detail="No matching results found for evidence pack")

        document_ids = [item.id for item in documents]
        attachments = (
            session.query(DocumentAttachment)
            .filter(DocumentAttachment.document_id.in_(document_ids))
            .all()
        ) if document_ids else []
        attachment_user_map = {
            item.id: item.username
            for item in session.query(User).filter(User.id.in_({attachment.user_id for attachment in attachments})).all()
        } if attachments else {}
        attachments_by_document: Dict[int, List[DocumentAttachment]] = {}
        for attachment in attachments:
            attachments_by_document.setdefault(attachment.document_id, []).append(attachment)

        export_dir = user_data_root() / "exports"
        export_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        safe_name = processor.sanitize_filename(project.name or "ULTRA_FORCE_Project")
        target = export_dir / f"{safe_name}_evidence_pack_{scope}_{stamp}.zip"

        manifest_headers = [
            "DocumentId", "SourceFile", "OutputFile", "Type", "Date", "Number", "CompanyName",
            "CanonicalCompanyName", "Amount", "Currency", "MatchStatus", "ReviewState", "AttachmentCount",
            "Categories", "AttachmentLabels",
        ]
        added = 0
        with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            manifest_rows = [manifest_headers]
            attachment_rows = [[
                "AttachmentId", "DocumentId", "Type", "Label", "FileName", "Note", "AddedBy", "CreatedAt",
            ]]
            for document in documents:
                output_path = Path(document.output_path or "").expanduser()
                if output_path.exists() and output_path.is_file():
                    archive.write(output_path, arcname=f"outputs/{processor.sanitize_filename(document.output_file or output_path.name)}")
                    added += 1
                linked_path = Path(document.enhanced_output_path or "").expanduser()
                if linked_path.exists() and linked_path.is_file():
                    archive.write(linked_path, arcname=f"enhanced/{processor.sanitize_filename(linked_path.name)}")
                    added += 1
                for attachment in attachments_by_document.get(document.id, []):
                    attachment_path = Path(attachment.file_path or "").expanduser()
                    if attachment_path.exists() and attachment_path.is_file():
                        attachment_type = (getattr(attachment, "attachment_type", "") or "supporting_document").strip() or "supporting_document"
                        archive.write(
                            attachment_path,
                            arcname=f"attachments/{attachment_type}/{document.id}_{processor.sanitize_filename(attachment.file_name or attachment_path.name)}",
                        )
                        added += 1
                    attachment_rows.append([
                        attachment.id,
                        document.id,
                        getattr(attachment, "attachment_type", "supporting_document") or "supporting_document",
                        attachment.label,
                        attachment.file_name,
                        attachment.note,
                        attachment_user_map.get(attachment.user_id, ""),
                        attachment.created_at.isoformat() if attachment.created_at else "",
                    ])
                attachment_types = sorted({
                    (getattr(item, "attachment_type", "supporting_document") or "supporting_document")
                    for item in attachments_by_document.get(document.id, [])
                })
                manifest_rows.append(
                    [
                        document.id,
                        document.source_file,
                        document.output_file,
                        document.doc_type,
                        document.date,
                        document.number,
                        document.company_name,
                        document.canonical_company_name,
                        document.amount,
                        document.currency,
                        document.match_status,
                        document.review_state,
                        len(attachments_by_document.get(document.id, [])),
                        ", ".join(attachment_types),
                        ", ".join(item.label for item in attachments_by_document.get(document.id, []) if item.label),
                    ]
                )
            manifest_name = f"{safe_name}_evidence_manifest_{stamp}.csv"
            buffer = io.StringIO()
            writer = csv.writer(buffer)
            writer.writerows(manifest_rows)
            archive.writestr(manifest_name, buffer.getvalue())
            added += 1
            attachment_manifest_name = f"{safe_name}_evidence_attachments_{stamp}.csv"
            attachment_buffer = io.StringIO()
            attachment_writer = csv.writer(attachment_buffer)
            attachment_writer.writerows(attachment_rows)
            archive.writestr(attachment_manifest_name, attachment_buffer.getvalue())
            added += 1
        if added == 0:
            target.unlink(missing_ok=True)
            raise HTTPException(status_code=404, detail="No evidence files were available for export")
    return FileResponse(target, media_type="application/zip", filename=target.name)


@app.get("/api/projects/{project_id}/close-package")
def export_project_close_package(
    project_id: int,
    preset: str = "ultra_force",
    token: str = "",
    x_auth_token: str = Header(default=""),
) -> FileResponse:
    user = require_user(x_auth_token or token)
    if preset not in ACCOUNTING_EXPORT_PRESETS:
        raise HTTPException(status_code=400, detail="Unsupported accounting export preset")
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="viewer")
        documents = (
            session.query(DocumentRecord)
            .filter(DocumentRecord.project_id == project.id)
            .order_by(DocumentRecord.created_at.desc(), DocumentRecord.id.desc())
            .all()
        )
        if not documents:
            raise HTTPException(status_code=404, detail="No stored results found for this project")

        export_dir = user_data_root() / "exports"
        export_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        safe_name = processor.sanitize_filename(project.name or "ULTRA_FORCE_Project")
        target = export_dir / f"{safe_name}_close_package_{stamp}.zip"

        unresolved = [
            item for item in documents
            if item.match_status == "missing_receipt"
            or item.review_state == "missing_receipt"
            or item.confidence_label == "low"
        ]

        with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            accounting_buffer = io.StringIO()
            accounting_writer = csv.writer(accounting_buffer)
            accounting_writer.writerow(accounting_export_headers(preset))
            for document in documents:
                accounting_writer.writerow(accounting_export_row(project, document, preset))
            archive.writestr(f"{safe_name}_accounting_{preset}.csv", accounting_buffer.getvalue())

            unresolved_buffer = io.StringIO()
            unresolved_writer = csv.writer(unresolved_buffer)
            unresolved_writer.writerow([
                "Date", "Kind", "Vendor", "Amount", "Status", "ReviewState", "Confidence", "Reference", "SourceFile",
            ])
            for document in unresolved:
                unresolved_writer.writerow([
                    document.date,
                    document.source_type,
                    document.canonical_company_name or document.company_name,
                    document.amount,
                    document.match_status,
                    document.review_state,
                    document.confidence_label,
                    document.number,
                    document.source_file,
                ])
            archive.writestr(f"{safe_name}_unresolved.csv", unresolved_buffer.getvalue())

            summary_buffer = io.StringIO()
            summary_writer = csv.writer(summary_buffer)
            summary_writer.writerow(["Metric", "Value"])
            summary_writer.writerow(["TotalDocuments", len(documents)])
            summary_writer.writerow(["UnresolvedRows", len(unresolved)])
            summary_writer.writerow(["MatchedRows", sum(1 for item in documents if item.match_status == "matched")])
            summary_writer.writerow(["LowConfidenceRows", sum(1 for item in documents if item.confidence_label == "low")])
            summary_writer.writerow(["AccountingPreset", preset])
            archive.writestr(f"{safe_name}_close_summary.csv", summary_buffer.getvalue())

            for document in documents:
                output_path = Path(document.output_path or "").expanduser()
                if output_path.exists() and output_path.is_file():
                    archive.write(output_path, arcname=f"outputs/{processor.sanitize_filename(document.output_file or output_path.name)}")

    return FileResponse(target, media_type="application/zip", filename=target.name)


@app.get("/api/projects/{project_id}/close-summary")
def project_close_summary(
    project_id: int,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    today = datetime.now().date()
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="viewer")
        documents = (
            session.query(DocumentRecord)
            .filter(DocumentRecord.project_id == project.id)
            .order_by(DocumentRecord.date.asc(), DocumentRecord.created_at.asc(), DocumentRecord.id.asc())
            .all()
        )
        if not documents:
            return {
                "summary": {
                    "total_documents": 0,
                    "bank_transactions": 0,
                    "unresolved_count": 0,
                    "unresolved_amount": 0.0,
                    "matched_count": 0,
                    "reviewed_count": 0,
                },
                "aging": [],
                "attention": [],
            }

        unresolved_rows: List[Dict[str, Any]] = []
        matched_count = 0
        reviewed_count = 0
        bank_transactions = 0
        for document in documents:
            if document.source_type == "sheet" and document.doc_type == "BankTransaction":
                bank_transactions += 1
            status = (document.review_state or "").strip().lower()
            if status and status != "unreviewed":
                reviewed_count += 1
            normalized_status = (document.match_status or "").strip().lower()
            if normalized_status in {"matched", "linked_to_bank"}:
                matched_count += 1
            unresolved = (
                normalized_status == "missing_receipt"
                or status == "missing_receipt"
                or document.confidence_label == "low"
            )
            if not unresolved:
                continue
            amount = processor.amount_to_float(document.amount) or 0.0
            age_days = None
            try:
                if document.date and re.match(r"^\d{4}-\d{2}-\d{2}$", document.date):
                    age_days = (today - datetime.strptime(document.date, "%Y-%m-%d").date()).days
            except ValueError:
                age_days = None
            unresolved_rows.append({
                "id": document.id,
                "date": document.date or "",
                "company_name": document.canonical_company_name or document.company_name or "Unknown",
                "amount": amount,
                "source_type": document.source_type or "",
                "source_file": document.source_file or "",
                "number": document.number or "",
                "match_status": document.match_status or "",
                "review_state": document.review_state or "",
                "age_days": age_days,
            })

        buckets = [
            ("0-7 days", 0, 7),
            ("8-30 days", 8, 30),
            ("31-60 days", 31, 60),
            ("61-90 days", 61, 90),
            ("91+ days", 91, None),
            ("Unknown date", None, None),
        ]
        aging_rows = []
        for label, low, high in buckets:
            items = []
            for row in unresolved_rows:
                age = row["age_days"]
                if label == "Unknown date":
                    if age is None:
                        items.append(row)
                elif age is not None and age >= low and (high is None or age <= high):
                    items.append(row)
            aging_rows.append({
                "bucket": label,
                "count": len(items),
                "amount": sum(item["amount"] for item in items),
            })

        attention = sorted(
            unresolved_rows,
            key=lambda item: ((item["age_days"] if item["age_days"] is not None else -1), item["amount"]),
            reverse=True,
        )[:12]
        return {
            "summary": {
                "total_documents": len(documents),
                "bank_transactions": bank_transactions,
                "unresolved_count": len(unresolved_rows),
                "unresolved_amount": sum(item["amount"] for item in unresolved_rows),
                "matched_count": matched_count,
                "reviewed_count": reviewed_count,
            },
            "aging": aging_rows,
            "attention": attention,
        }


@app.get("/api/projects/{project_id}/exceptions")
def project_exception_cases(
    project_id: int,
    search: str = "",
    case_type: str = "",
    page: int = 1,
    page_size: int = 12,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="viewer")
        rules = (
            session.query(ProjectRule)
            .filter(ProjectRule.project_id == project.id)
            .order_by(ProjectRule.created_at.asc(), ProjectRule.id.asc())
            .all()
        )
        vendor_alias_map = {
            item.normalized_key: item.canonical_name
            for item in session.query(VendorAlias)
            .filter(VendorAlias.project_id == project.id)
            .all()
        }
        documents = (
            document_query_for_project(session, project.id)
            .order_by(DocumentRecord.created_at.desc(), DocumentRecord.id.desc())
            .all()
        )
        cases = build_exception_cases(documents, rules, vendor_alias_map)
        query = search.strip().lower()
        filtered = [
            item for item in cases
            if (
                (not case_type or item["type"] == case_type)
                and (
                    not query
                    or query in " ".join([
                        item["label"],
                        item["reason"],
                        item["company_name"],
                        f"{item['amount']:.2f}",
                    ]).lower()
                )
            )
        ]
        safe_page = max(1, page)
        safe_page_size = max(1, min(page_size, 100))
        total = len(filtered)
        start = (safe_page - 1) * safe_page_size
        rows = filtered[start:start + safe_page_size]
        return {
            "summary": {
                "total": len(cases),
                "installments": sum(1 for item in cases if item["type"] == "installment_chain"),
                "refund_pairs": sum(1 for item in cases if item["type"] == "refund_pair"),
                "split_groups": sum(1 for item in cases if item["type"] == "split_payment_group"),
                "duplicates": sum(1 for item in cases if item["type"] == "duplicate_cluster"),
                "mismatches": sum(1 for item in cases if item["type"] == "amount_mismatch_case"),
            },
            "rows": rows,
            "pagination": {
                "page": safe_page,
                "page_size": safe_page_size,
                "total": total,
                "total_pages": max(1, (total + safe_page_size - 1) // safe_page_size),
            },
        }


@app.get("/api/projects/{project_id}/feedback-insights")
def project_feedback_insights(
    project_id: int,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="viewer")
        documents = document_query_for_project(session, project.id).order_by(DocumentRecord.created_at.desc(), DocumentRecord.id.desc()).all()
        aliases = (
            session.query(VendorAlias)
            .filter(VendorAlias.project_id == project.id)
            .all()
        )
        rules = (
            session.query(ProjectRule)
            .filter(ProjectRule.project_id == project.id)
            .all()
        )
        suggestions = build_feedback_suggestions(
            documents,
            {item.normalized_key: item.canonical_name for item in aliases},
            {(item.keyword or "").strip().lower() for item in rules},
        )
        reviewed_rows = sum(1 for item in documents if (item.review_state or "") not in {"", "unreviewed"})
        corrected_rows = sum(
            1 for item in documents
            if (item.canonical_company_name or "").strip()
            and (item.canonical_company_name or "").strip().lower() != (item.company_name or "").strip().lower()
        )
        return {
            "summary": {
                "reviewed_rows": reviewed_rows,
                "corrected_rows": corrected_rows,
                "vendor_alias_suggestions": len(suggestions["alias_suggestions"]),
                "rule_suggestions": len(suggestions["rule_suggestions"]),
            },
            **suggestions,
        }


@app.post("/api/projects/{project_id}/feedback-insights/apply")
def apply_feedback_insight(
    project_id: int,
    payload: FeedbackApplyRequest,
    x_auth_token: str = Header(default=""),
) -> Dict[str, Any]:
    user = require_user(x_auth_token)
    with db_session() as session:
        project, _ = require_project_access(session, project_id, user, min_role="admin")
        suggestion_type = (payload.suggestion_type or "").strip()
        if suggestion_type == "vendor_alias":
            normalized_key = normalize_company_name(payload.normalized_key or "")
            if not normalized_key or not (payload.canonical_name or "").strip():
                raise HTTPException(status_code=400, detail="Invalid vendor alias suggestion")
            alias = (
                session.query(VendorAlias)
                .filter(VendorAlias.project_id == project.id, VendorAlias.normalized_key == normalized_key)
                .first()
            )
            if not alias:
                alias = VendorAlias(
                    user_id=user.id,
                    project_id=project.id,
                    normalized_key=normalized_key,
                    canonical_name=(payload.canonical_name or "").strip(),
                )
                session.add(alias)
                session.flush()
            else:
                alias.canonical_name = (payload.canonical_name or "").strip()
            return {"ok": True, "applied": "vendor_alias", "alias": serialize_vendor_alias(alias)}
        if suggestion_type == "project_rule":
            keyword = (payload.keyword or "").strip()
            if not keyword:
                raise HTTPException(status_code=400, detail="Invalid project rule suggestion")
            rule = ProjectRule(
                user_id=user.id,
                project_id=project.id,
                keyword=keyword,
                source_type=(payload.source_type or "").strip(),
                status=(payload.status or "").strip(),
                category=(payload.category or "").strip(),
                subcategory=(payload.subcategory or "").strip(),
            )
            session.add(rule)
            session.flush()
            return {"ok": True, "applied": "project_rule", "rule": serialize_rule(rule)}
        raise HTTPException(status_code=400, detail="Unsupported suggestion type")


@app.get("/api/file")
def get_file(path: str, token: str = "", x_auth_token: str = Header(default="")) -> FileResponse:
    auth_token = x_auth_token or token
    user = require_user(auth_token)
    target = Path(path).expanduser().resolve()
    if not target.exists() or not target.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    with db_session() as session:
        accessible_project_ids = {project.id for project in session.query(Project).filter(Project.user_id == user.id).all()}
        accessible_project_ids.update(
            item.project_id
            for item in session.query(ProjectMember).filter(ProjectMember.user_id == user.id).all()
        )
        documents = (
            session.query(DocumentRecord)
            .filter(DocumentRecord.project_id.in_(accessible_project_ids))
            .all()
        )
        attachments = (
            session.query(DocumentAttachment)
            .filter(DocumentAttachment.project_id.in_(accessible_project_ids))
            .all()
        )
        allowed_paths: set[Path] = set()
        for document in documents:
            for raw_path in (
                document.source_path,
                document.output_path,
                document.enhanced_output_path,
                document.original_debug_image,
                document.enhanced_debug_image,
            ):
                if not raw_path:
                    continue
                try:
                    allowed_paths.add(Path(raw_path).expanduser().resolve())
                except Exception:
                    continue
        for attachment in attachments:
            if not attachment.file_path:
                continue
            try:
                allowed_paths.add(Path(attachment.file_path).expanduser().resolve())
            except Exception:
                continue
    if target not in allowed_paths:
        raise HTTPException(status_code=403, detail="File access denied")
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
    purpose: Literal["video", "attachment"] = "video"


@app.post("/api/pick-file")
def pick_file(request: PickFileRequest) -> Dict[str, str]:
    prompt = {
        "video": "Choose video file",
        "attachment": "Choose attachment file",
    }[request.purpose]
    extensions = {
        "video": ["mp4", "mov", "m4v", "avi"],
        "attachment": ["pdf", "png", "jpg", "jpeg", "webp", "txt", "csv", "xlsx", "zip"],
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
