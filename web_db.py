import hashlib
import hmac
import os
import secrets
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Generator, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy import inspect, text
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, sessionmaker

from app_paths import user_data_root

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    f"sqlite:///{(user_data_root() / 'ultra_force.db').as_posix()}",
)

CONNECT_ARGS = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, future=True, connect_args=CONNECT_ARGS)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


class Base(DeclarativeBase):
    pass


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    name: Mapped[str] = mapped_column(String(200), default="My Company")
    base_currency: Mapped[str] = mapped_column(String(16), default="AED")
    fiscal_year_start_month: Mapped[int] = mapped_column(Integer, default=1)
    vat_registration_number: Mapped[str] = mapped_column(String(64), default="")
    vat_rate: Mapped[str] = mapped_column(String(32), default="5.00")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class CompanyParty(Base):
    __tablename__ = "company_parties"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), index=True)
    party_type: Mapped[str] = mapped_column(String(32), default="supplier", index=True)
    name: Mapped[str] = mapped_column(String(255), default="")
    tax_registration_number: Mapped[str] = mapped_column(String(64), default="")
    contact_email: Mapped[str] = mapped_column(String(255), default="")
    contact_phone: Mapped[str] = mapped_column(String(64), default="")
    default_account_code: Mapped[str] = mapped_column(String(64), default="")
    payment_terms_days: Mapped[int] = mapped_column(Integer, default=30)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class CompanyDimension(Base):
    __tablename__ = "company_dimensions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), index=True)
    dimension_type: Mapped[str] = mapped_column(String(32), default="project_code", index=True)
    code: Mapped[str] = mapped_column(String(120), default="", index=True)
    name: Mapped[str] = mapped_column(String(255), default="")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class CompanyAllocation(Base):
    __tablename__ = "company_allocations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), index=True)
    allocation_type: Mapped[str] = mapped_column(String(32), default="payable", index=True)
    payment_document_id: Mapped[int] = mapped_column(ForeignKey("document_records.id"), index=True)
    target_document_id: Mapped[int] = mapped_column(ForeignKey("document_records.id"), index=True)
    amount: Mapped[str] = mapped_column(String(64), default="")
    note: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class CompanyBillingEvent(Base):
    __tablename__ = "company_billing_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    event_type: Mapped[str] = mapped_column(String(32), default="progress_claim", index=True)
    label: Mapped[str] = mapped_column(String(255), default="")
    event_date: Mapped[str] = mapped_column(String(32), default="")
    amount: Mapped[str] = mapped_column(String(64), default="")
    status: Mapped[str] = mapped_column(String(32), default="draft", index=True)
    note: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class CompanyPurchaseOrder(Base):
    __tablename__ = "company_purchase_orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    supplier_party_id: Mapped[int | None] = mapped_column(ForeignKey("company_parties.id"), nullable=True, index=True)
    cost_code: Mapped[str] = mapped_column(String(120), default="")
    po_number: Mapped[str] = mapped_column(String(120), default="", index=True)
    po_date: Mapped[str] = mapped_column(String(32), default="")
    amount: Mapped[str] = mapped_column(String(64), default="")
    status: Mapped[str] = mapped_column(String(32), default="open", index=True)
    note: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class CompanyReceipt(Base):
    __tablename__ = "company_receipts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), index=True)
    purchase_order_id: Mapped[int] = mapped_column(ForeignKey("company_purchase_orders.id"), index=True)
    receipt_type: Mapped[str] = mapped_column(String(32), default="goods_receipt", index=True)
    receipt_number: Mapped[str] = mapped_column(String(120), default="", index=True)
    receipt_date: Mapped[str] = mapped_column(String(32), default="")
    amount: Mapped[str] = mapped_column(String(64), default="")
    status: Mapped[str] = mapped_column(String(32), default="received", index=True)
    note: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class CompanyAccountingRule(Base):
    __tablename__ = "company_accounting_rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), index=True)
    keyword: Mapped[str] = mapped_column(String(255), index=True)
    source_type: Mapped[str] = mapped_column(String(50), default="")
    status: Mapped[str] = mapped_column(String(32), default="")
    category: Mapped[str] = mapped_column(String(120), default="")
    subcategory: Mapped[str] = mapped_column(String(120), default="")
    account_code: Mapped[str] = mapped_column(String(64), default="")
    offset_account_code: Mapped[str] = mapped_column(String(64), default="")
    project_code: Mapped[str] = mapped_column(String(120), default="")
    cost_code: Mapped[str] = mapped_column(String(120), default="")
    cost_center: Mapped[str] = mapped_column(String(120), default="")
    payment_method: Mapped[str] = mapped_column(String(120), default="")
    vat_flag: Mapped[bool] = mapped_column(Boolean, default=False)
    auto_post: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class CompanyProcurementReview(Base):
    __tablename__ = "company_procurement_reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    supplier_name: Mapped[str] = mapped_column(String(255), default="", index=True)
    match_flag: Mapped[str] = mapped_column(String(64), default="", index=True)
    assigned_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    review_state: Mapped[str] = mapped_column(String(32), default="open", index=True)
    note: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_id: Mapped[int | None] = mapped_column(ForeignKey("companies.id"), nullable=True, index=True)
    username: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(512))
    role: Mapped[str] = mapped_column(String(32), default="admin")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    projects: Mapped[list["Project"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    sessions: Mapped[list["AuthSession"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class AuthSession(Base):
    __tablename__ = "auth_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    token: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user: Mapped[User] = relationship(back_populates="sessions")


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    company_id: Mapped[int | None] = mapped_column(ForeignKey("companies.id"), nullable=True, index=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    description: Mapped[str] = mapped_column(Text, default="")
    job_code: Mapped[str] = mapped_column(String(120), default="")
    client_name: Mapped[str] = mapped_column(String(255), default="")
    site_name: Mapped[str] = mapped_column(String(255), default="")
    contract_number: Mapped[str] = mapped_column(String(120), default="")
    budget_amount: Mapped[str] = mapped_column(String(64), default="")
    contract_value: Mapped[str] = mapped_column(String(64), default="")
    variation_amount: Mapped[str] = mapped_column(String(64), default="")
    billed_to_date: Mapped[str] = mapped_column(String(64), default="")
    certified_progress_pct: Mapped[str] = mapped_column(String(32), default="")
    retention_percent: Mapped[str] = mapped_column(String(32), default="")
    advance_received: Mapped[str] = mapped_column(String(64), default="")
    project_status: Mapped[str] = mapped_column(String(64), default="active")

    source_dir: Mapped[str] = mapped_column(Text, default="")
    source_mode: Mapped[str] = mapped_column(String(50), default="pdf")
    video_source_path: Mapped[str] = mapped_column(Text, default="")
    output_dir: Mapped[str] = mapped_column(Text, default="")
    debug_image_dir: Mapped[str] = mapped_column(Text, default="")
    archive_source_dir: Mapped[str] = mapped_column(Text, default="")
    project_name: Mapped[str] = mapped_column(String(200), default="MyProject")
    ocr_backend: Mapped[str] = mapped_column(String(50), default="normal")
    handwriting_backend: Mapped[str] = mapped_column(String(50), default="none")
    trocr_model: Mapped[str] = mapped_column(String(200), default="microsoft/trocr-base-handwritten")
    ocr_profile: Mapped[str] = mapped_column(String(50), default="mixed")
    export_image_mode: Mapped[str] = mapped_column(String(50), default="original")
    naming_pattern: Mapped[str] = mapped_column(Text)
    lang: Mapped[str] = mapped_column(String(50), default="en")
    dpi: Mapped[int] = mapped_column(Integer, default=300)
    single_item_per_page: Mapped[bool] = mapped_column(Boolean, default=True)
    save_text: Mapped[bool] = mapped_column(Boolean, default=True)
    use_angle_cls: Mapped[bool] = mapped_column(Boolean, default=True)
    move_processed_source: Mapped[bool] = mapped_column(Boolean, default=False)
    video_sample_seconds: Mapped[int] = mapped_column(Integer, default=2)
    video_max_frames: Mapped[int] = mapped_column(Integer, default=120)
    excel_name: Mapped[str] = mapped_column(String(200), default="document_summary.xlsx")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    user: Mapped[User] = relationship(back_populates="projects")
    documents: Mapped[list["DocumentRecord"]] = relationship(back_populates="project", cascade="all, delete-orphan")
    rules: Mapped[list["ProjectRule"]] = relationship(back_populates="project", cascade="all, delete-orphan")
    vendor_aliases: Mapped[list["VendorAlias"]] = relationship(back_populates="project", cascade="all, delete-orphan")
    comments: Mapped[list["ProjectComment"]] = relationship(back_populates="project", cascade="all, delete-orphan")
    saved_searches: Mapped[list["SavedSearch"]] = relationship(back_populates="project", cascade="all, delete-orphan")
    members: Mapped[list["ProjectMember"]] = relationship(back_populates="project", cascade="all, delete-orphan")
    accounts: Mapped[list["AccountingAccount"]] = relationship(back_populates="project", cascade="all, delete-orphan")
    periods: Mapped[list["AccountingPeriod"]] = relationship(back_populates="project", cascade="all, delete-orphan")
    journal_entries: Mapped[list["JournalEntry"]] = relationship(back_populates="project", cascade="all, delete-orphan")


class DocumentRecord(Base):
    __tablename__ = "document_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    assigned_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    source_file: Mapped[str] = mapped_column(String(255))
    source_path: Mapped[str] = mapped_column(Text, default="")
    source_hash: Mapped[str] = mapped_column(String(64), default="")
    source_type: Mapped[str] = mapped_column(String(50), default="pdf")
    source_origin: Mapped[str] = mapped_column(String(120), default="pdf_upload")
    source_timestamp: Mapped[str] = mapped_column(String(120), default="")
    output_file: Mapped[str] = mapped_column(String(255))
    output_path: Mapped[str] = mapped_column(Text, default="")
    enhanced_output_path: Mapped[str] = mapped_column(Text, default="")
    original_debug_image: Mapped[str] = mapped_column(Text, default="")
    enhanced_debug_image: Mapped[str] = mapped_column(Text, default="")
    doc_type: Mapped[str] = mapped_column(String(120), default="Unknown")
    date: Mapped[str] = mapped_column(String(120), default="Unknown")
    number: Mapped[str] = mapped_column(String(255), default="Unknown")
    company_name: Mapped[str] = mapped_column(String(255), default="Unknown")
    amount: Mapped[str] = mapped_column(String(120), default="Unknown")
    currency: Mapped[str] = mapped_column(String(50), default="Unknown")
    transaction_direction: Mapped[str] = mapped_column(String(32), default="unknown")
    confidence_score: Mapped[int] = mapped_column(Integer, default=0)
    confidence_label: Mapped[str] = mapped_column(String(32), default="low")
    raw_text: Mapped[str] = mapped_column(Text, default="")
    match_status: Mapped[str] = mapped_column(String(32), default="unreviewed")
    match_score: Mapped[int] = mapped_column(Integer, default=0)
    matched_record_source_file: Mapped[str] = mapped_column(String(255), default="")
    matched_record_output_file: Mapped[str] = mapped_column(String(255), default="")
    matched_record_source_type: Mapped[str] = mapped_column(String(50), default="")
    matched_record_source_timestamp: Mapped[str] = mapped_column(String(120), default="")
    matched_record_date: Mapped[str] = mapped_column(String(120), default="")
    matched_record_number: Mapped[str] = mapped_column(String(255), default="")
    matched_record_company_name: Mapped[str] = mapped_column(String(255), default="")
    matched_record_amount: Mapped[str] = mapped_column(String(120), default="")
    matched_record_transaction_direction: Mapped[str] = mapped_column(String(32), default="")
    match_basis: Mapped[str] = mapped_column(Text, default="")
    canonical_company_name: Mapped[str] = mapped_column(String(255), default="")
    review_state: Mapped[str] = mapped_column(String(32), default="unreviewed")
    review_note: Mapped[str] = mapped_column(Text, default="")
    category: Mapped[str] = mapped_column(String(120), default="")
    subcategory: Mapped[str] = mapped_column(String(120), default="")
    account_code: Mapped[str] = mapped_column(String(64), default="")
    offset_account_code: Mapped[str] = mapped_column(String(64), default="")
    cost_code: Mapped[str] = mapped_column(String(120), default="")
    cost_center: Mapped[str] = mapped_column(String(120), default="")
    project_code: Mapped[str] = mapped_column(String(120), default="")
    purchase_order_id: Mapped[int | None] = mapped_column(Integer, nullable=True, default=None)
    payment_method: Mapped[str] = mapped_column(String(120), default="")
    vat_flag: Mapped[bool] = mapped_column(Boolean, default=False)
    review_updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    project: Mapped[Project] = relationship(back_populates="documents")


class ProjectRule(Base):
    __tablename__ = "project_rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    keyword: Mapped[str] = mapped_column(String(255), index=True)
    source_type: Mapped[str] = mapped_column(String(50), default="")
    status: Mapped[str] = mapped_column(String(32), default="")
    category: Mapped[str] = mapped_column(String(120), default="")
    subcategory: Mapped[str] = mapped_column(String(120), default="")
    account_code: Mapped[str] = mapped_column(String(64), default="")
    offset_account_code: Mapped[str] = mapped_column(String(64), default="")
    project_code: Mapped[str] = mapped_column(String(120), default="")
    cost_code: Mapped[str] = mapped_column(String(120), default="")
    cost_center: Mapped[str] = mapped_column(String(120), default="")
    payment_method: Mapped[str] = mapped_column(String(120), default="")
    vat_flag: Mapped[bool] = mapped_column(Boolean, default=False)
    auto_post: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    project: Mapped[Project] = relationship(back_populates="rules")


class VendorAlias(Base):
    __tablename__ = "vendor_aliases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    normalized_key: Mapped[str] = mapped_column(String(255), index=True)
    canonical_name: Mapped[str] = mapped_column(String(255), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    project: Mapped[Project] = relationship(back_populates="vendor_aliases")


class ProjectComment(Base):
    __tablename__ = "project_comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    document_id: Mapped[int | None] = mapped_column(ForeignKey("document_records.id"), nullable=True, index=True)
    body: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    project: Mapped[Project] = relationship(back_populates="comments")


class DocumentAttachment(Base):
    __tablename__ = "document_attachments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("document_records.id"), index=True)
    attachment_type: Mapped[str] = mapped_column(String(64), default="supporting_document")
    label: Mapped[str] = mapped_column(String(255), default="")
    file_path: Mapped[str] = mapped_column(Text, default="")
    file_name: Mapped[str] = mapped_column(String(255), default="")
    note: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class SavedSearch(Base):
    __tablename__ = "saved_searches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    name: Mapped[str] = mapped_column(String(255), default="")
    scope: Mapped[str] = mapped_column(String(64), default="global_search")
    query_json: Mapped[str] = mapped_column(Text, default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    project: Mapped[Project] = relationship(back_populates="saved_searches")


class ProjectMember(Base):
    __tablename__ = "project_members"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    role: Mapped[str] = mapped_column(String(32), default="reviewer")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    project: Mapped[Project] = relationship(back_populates="members")


class AccountingAccount(Base):
    __tablename__ = "accounting_accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    company_id: Mapped[int | None] = mapped_column(ForeignKey("companies.id"), nullable=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    code: Mapped[str] = mapped_column(String(64), index=True)
    name: Mapped[str] = mapped_column(String(255), default="")
    account_type: Mapped[str] = mapped_column(String(64), default="expense")
    subtype: Mapped[str] = mapped_column(String(120), default="")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    project: Mapped[Project] = relationship(back_populates="accounts")


class AccountingPeriod(Base):
    __tablename__ = "accounting_periods"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    company_id: Mapped[int | None] = mapped_column(ForeignKey("companies.id"), nullable=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    name: Mapped[str] = mapped_column(String(120), default="")
    start_date: Mapped[str] = mapped_column(String(32), default="")
    end_date: Mapped[str] = mapped_column(String(32), default="")
    status: Mapped[str] = mapped_column(String(32), default="open")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    project: Mapped[Project] = relationship(back_populates="periods")


class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    company_id: Mapped[int | None] = mapped_column(ForeignKey("companies.id"), nullable=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    document_id: Mapped[int | None] = mapped_column(ForeignKey("document_records.id"), nullable=True, index=True)
    entry_date: Mapped[str] = mapped_column(String(32), default="")
    reference: Mapped[str] = mapped_column(String(255), default="")
    memo: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(32), default="posted")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    project: Mapped[Project] = relationship(back_populates="journal_entries")
    lines: Mapped[list["JournalEntryLine"]] = relationship(back_populates="entry", cascade="all, delete-orphan")


class JournalEntryLine(Base):
    __tablename__ = "journal_entry_lines"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    entry_id: Mapped[int] = mapped_column(ForeignKey("journal_entries.id"), index=True)
    account_code: Mapped[str] = mapped_column(String(64), default="")
    debit: Mapped[str] = mapped_column(String(64), default="")
    credit: Mapped[str] = mapped_column(String(64), default="")
    cost_center: Mapped[str] = mapped_column(String(120), default="")
    project_code: Mapped[str] = mapped_column(String(120), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    entry: Mapped[JournalEntry] = relationship(back_populates="lines")


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    ensure_compatible_schema()


def ensure_compatible_schema() -> None:
    inspector = inspect(engine)
    table_names = set(inspector.get_table_names())
    statements = []

    if "projects" in table_names:
        project_columns = {column["name"] for column in inspector.get_columns("projects")}
        if "source_mode" not in project_columns:
            statements.append("ALTER TABLE projects ADD COLUMN source_mode TEXT DEFAULT 'pdf'")
        if "video_source_path" not in project_columns:
            statements.append("ALTER TABLE projects ADD COLUMN video_source_path TEXT DEFAULT ''")
        if "archive_source_dir" not in project_columns:
            statements.append("ALTER TABLE projects ADD COLUMN archive_source_dir TEXT DEFAULT ''")
        if "move_processed_source" not in project_columns:
            statements.append("ALTER TABLE projects ADD COLUMN move_processed_source BOOLEAN DEFAULT 0")
        if "video_sample_seconds" not in project_columns:
            statements.append("ALTER TABLE projects ADD COLUMN video_sample_seconds INTEGER DEFAULT 2")
        if "video_max_frames" not in project_columns:
            statements.append("ALTER TABLE projects ADD COLUMN video_max_frames INTEGER DEFAULT 120")

    if "document_records" not in table_names:
        if statements:
            with engine.begin() as connection:
                for statement in statements:
                    connection.execute(text(statement))
        return
    if "users" in table_names:
        user_columns = {column["name"] for column in inspector.get_columns("users")}
        if "role" not in user_columns:
            statements.append("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'admin'")
        if "company_id" not in user_columns:
            statements.append("ALTER TABLE users ADD COLUMN company_id INTEGER")

    if "companies" in table_names:
        company_columns = {column["name"] for column in inspector.get_columns("companies")}
        if "base_currency" not in company_columns:
            statements.append("ALTER TABLE companies ADD COLUMN base_currency TEXT DEFAULT 'AED'")
        if "fiscal_year_start_month" not in company_columns:
            statements.append("ALTER TABLE companies ADD COLUMN fiscal_year_start_month INTEGER DEFAULT 1")
        if "vat_registration_number" not in company_columns:
            statements.append("ALTER TABLE companies ADD COLUMN vat_registration_number TEXT DEFAULT ''")
        if "vat_rate" not in company_columns:
            statements.append("ALTER TABLE companies ADD COLUMN vat_rate TEXT DEFAULT '5.00'")
    if "company_parties" not in table_names:
        CompanyParty.__table__.create(bind=engine, checkfirst=True)
    if "company_dimensions" not in table_names:
        CompanyDimension.__table__.create(bind=engine, checkfirst=True)
    if "company_allocations" not in table_names:
        CompanyAllocation.__table__.create(bind=engine, checkfirst=True)
    if "company_billing_events" not in table_names:
        CompanyBillingEvent.__table__.create(bind=engine, checkfirst=True)
    if "company_purchase_orders" not in table_names:
        CompanyPurchaseOrder.__table__.create(bind=engine, checkfirst=True)
    if "company_receipts" not in table_names:
        CompanyReceipt.__table__.create(bind=engine, checkfirst=True)
    if "company_procurement_reviews" not in table_names:
        CompanyProcurementReview.__table__.create(bind=engine, checkfirst=True)

    if "projects" in table_names:
        project_columns = {column["name"] for column in inspector.get_columns("projects")}
        if "company_id" not in project_columns:
            statements.append("ALTER TABLE projects ADD COLUMN company_id INTEGER")
        if "job_code" not in project_columns:
            statements.append("ALTER TABLE projects ADD COLUMN job_code TEXT DEFAULT ''")
        if "client_name" not in project_columns:
            statements.append("ALTER TABLE projects ADD COLUMN client_name TEXT DEFAULT ''")
        if "site_name" not in project_columns:
            statements.append("ALTER TABLE projects ADD COLUMN site_name TEXT DEFAULT ''")
        if "contract_number" not in project_columns:
            statements.append("ALTER TABLE projects ADD COLUMN contract_number TEXT DEFAULT ''")
        if "budget_amount" not in project_columns:
            statements.append("ALTER TABLE projects ADD COLUMN budget_amount TEXT DEFAULT ''")
        if "contract_value" not in project_columns:
            statements.append("ALTER TABLE projects ADD COLUMN contract_value TEXT DEFAULT ''")
        if "variation_amount" not in project_columns:
            statements.append("ALTER TABLE projects ADD COLUMN variation_amount TEXT DEFAULT ''")
        if "billed_to_date" not in project_columns:
            statements.append("ALTER TABLE projects ADD COLUMN billed_to_date TEXT DEFAULT ''")
        if "certified_progress_pct" not in project_columns:
            statements.append("ALTER TABLE projects ADD COLUMN certified_progress_pct TEXT DEFAULT ''")
        if "retention_percent" not in project_columns:
            statements.append("ALTER TABLE projects ADD COLUMN retention_percent TEXT DEFAULT ''")
        if "advance_received" not in project_columns:
            statements.append("ALTER TABLE projects ADD COLUMN advance_received TEXT DEFAULT ''")
        if "project_status" not in project_columns:
            statements.append("ALTER TABLE projects ADD COLUMN project_status TEXT DEFAULT 'active'")

    if "project_members" not in table_names:
        pass

    columns = {column["name"] for column in inspector.get_columns("document_records")}
    if "assigned_user_id" not in columns:
        statements.append("ALTER TABLE document_records ADD COLUMN assigned_user_id INTEGER")
    columns = {column["name"] for column in inspector.get_columns("document_records")}
    if "source_path" not in columns:
        statements.append(
            "ALTER TABLE document_records ADD COLUMN source_path TEXT DEFAULT ''"
        )
    if "source_hash" not in columns:
        statements.append(
            "ALTER TABLE document_records ADD COLUMN source_hash TEXT DEFAULT ''"
        )
    if "source_type" not in columns:
        statements.append(
            "ALTER TABLE document_records ADD COLUMN source_type TEXT DEFAULT 'pdf'"
        )
    if "cost_code" not in columns:
        statements.append("ALTER TABLE document_records ADD COLUMN cost_code TEXT DEFAULT ''")
    if "source_origin" not in columns:
        statements.append(
            "ALTER TABLE document_records ADD COLUMN source_origin TEXT DEFAULT 'pdf_upload'"
        )
    if "source_timestamp" not in columns:
        statements.append(
            "ALTER TABLE document_records ADD COLUMN source_timestamp TEXT DEFAULT ''"
        )
    if "confidence_score" not in columns:
        statements.append(
            "ALTER TABLE document_records ADD COLUMN confidence_score INTEGER DEFAULT 0"
        )
    if "confidence_label" not in columns:
        statements.append(
            "ALTER TABLE document_records ADD COLUMN confidence_label TEXT DEFAULT 'low'"
        )
    if "raw_text" not in columns:
        statements.append(
            "ALTER TABLE document_records ADD COLUMN raw_text TEXT DEFAULT ''"
        )
    if "transaction_direction" not in columns:
        statements.append(
            "ALTER TABLE document_records ADD COLUMN transaction_direction TEXT DEFAULT 'unknown'"
        )
    if "match_status" not in columns:
        statements.append(
            "ALTER TABLE document_records ADD COLUMN match_status TEXT DEFAULT 'unreviewed'"
        )
    if "match_score" not in columns:
        statements.append(
            "ALTER TABLE document_records ADD COLUMN match_score INTEGER DEFAULT 0"
        )
    if "matched_record_source_file" not in columns:
        statements.append(
            "ALTER TABLE document_records ADD COLUMN matched_record_source_file TEXT DEFAULT ''"
        )
    if "matched_record_output_file" not in columns:
        statements.append(
            "ALTER TABLE document_records ADD COLUMN matched_record_output_file TEXT DEFAULT ''"
        )
    if "matched_record_source_type" not in columns:
        statements.append(
            "ALTER TABLE document_records ADD COLUMN matched_record_source_type TEXT DEFAULT ''"
        )
    if "matched_record_source_timestamp" not in columns:
        statements.append(
            "ALTER TABLE document_records ADD COLUMN matched_record_source_timestamp TEXT DEFAULT ''"
        )
    if "matched_record_date" not in columns:
        statements.append(
            "ALTER TABLE document_records ADD COLUMN matched_record_date TEXT DEFAULT ''"
        )
    if "matched_record_number" not in columns:
        statements.append(
            "ALTER TABLE document_records ADD COLUMN matched_record_number TEXT DEFAULT ''"
        )
    if "matched_record_company_name" not in columns:
        statements.append(
            "ALTER TABLE document_records ADD COLUMN matched_record_company_name TEXT DEFAULT ''"
        )
    if "matched_record_amount" not in columns:
        statements.append(
            "ALTER TABLE document_records ADD COLUMN matched_record_amount TEXT DEFAULT ''"
        )
    if "matched_record_transaction_direction" not in columns:
        statements.append(
            "ALTER TABLE document_records ADD COLUMN matched_record_transaction_direction TEXT DEFAULT ''"
        )
    if "match_basis" not in columns:
        statements.append(
            "ALTER TABLE document_records ADD COLUMN match_basis TEXT DEFAULT ''"
        )
    if "canonical_company_name" not in columns:
        statements.append(
            "ALTER TABLE document_records ADD COLUMN canonical_company_name TEXT DEFAULT ''"
        )
    if "review_state" not in columns:
        statements.append(
            "ALTER TABLE document_records ADD COLUMN review_state TEXT DEFAULT 'unreviewed'"
        )
    if "review_note" not in columns:
        statements.append(
            "ALTER TABLE document_records ADD COLUMN review_note TEXT DEFAULT ''"
        )
    if "category" not in columns:
        statements.append(
            "ALTER TABLE document_records ADD COLUMN category TEXT DEFAULT ''"
        )
    if "subcategory" not in columns:
        statements.append(
            "ALTER TABLE document_records ADD COLUMN subcategory TEXT DEFAULT ''"
        )
    if "account_code" not in columns:
        statements.append(
            "ALTER TABLE document_records ADD COLUMN account_code TEXT DEFAULT ''"
        )
    if "offset_account_code" not in columns:
        statements.append(
            "ALTER TABLE document_records ADD COLUMN offset_account_code TEXT DEFAULT ''"
        )
    if "cost_center" not in columns:
        statements.append(
            "ALTER TABLE document_records ADD COLUMN cost_center TEXT DEFAULT ''"
        )
    if "project_code" not in columns:
        statements.append(
            "ALTER TABLE document_records ADD COLUMN project_code TEXT DEFAULT ''"
        )
    if "purchase_order_id" not in columns:
        statements.append(
            "ALTER TABLE document_records ADD COLUMN purchase_order_id INTEGER"
        )
    if "payment_method" not in columns:
        statements.append(
            "ALTER TABLE document_records ADD COLUMN payment_method TEXT DEFAULT ''"
        )
    if "vat_flag" not in columns:
        statements.append(
            "ALTER TABLE document_records ADD COLUMN vat_flag BOOLEAN DEFAULT 0"
        )
    if "review_updated_at" not in columns:
        statements.append(
            "ALTER TABLE document_records ADD COLUMN review_updated_at DATETIME"
        )
    if "document_attachments" in table_names:
        attachment_columns = {column["name"] for column in inspector.get_columns("document_attachments")}
        if "attachment_type" not in attachment_columns:
            statements.append(
                "ALTER TABLE document_attachments ADD COLUMN attachment_type TEXT DEFAULT 'supporting_document'"
            )
    if "project_rules" in table_names:
        rule_columns = {column["name"] for column in inspector.get_columns("project_rules")}
        if "account_code" not in rule_columns:
            statements.append("ALTER TABLE project_rules ADD COLUMN account_code TEXT DEFAULT ''")
        if "offset_account_code" not in rule_columns:
            statements.append("ALTER TABLE project_rules ADD COLUMN offset_account_code TEXT DEFAULT ''")
        if "project_code" not in rule_columns:
            statements.append("ALTER TABLE project_rules ADD COLUMN project_code TEXT DEFAULT ''")
        if "cost_code" not in rule_columns:
            statements.append("ALTER TABLE project_rules ADD COLUMN cost_code TEXT DEFAULT ''")
        if "cost_center" not in rule_columns:
            statements.append("ALTER TABLE project_rules ADD COLUMN cost_center TEXT DEFAULT ''")
        if "payment_method" not in rule_columns:
            statements.append("ALTER TABLE project_rules ADD COLUMN payment_method TEXT DEFAULT ''")
        if "vat_flag" not in rule_columns:
            statements.append("ALTER TABLE project_rules ADD COLUMN vat_flag BOOLEAN DEFAULT 0")
        if "auto_post" not in rule_columns:
            statements.append("ALTER TABLE project_rules ADD COLUMN auto_post BOOLEAN DEFAULT 1")
    if "accounting_accounts" in table_names:
        account_columns = {column["name"] for column in inspector.get_columns("accounting_accounts")}
        if "company_id" not in account_columns:
            statements.append("ALTER TABLE accounting_accounts ADD COLUMN company_id INTEGER")
    if "accounting_periods" in table_names:
        period_columns = {column["name"] for column in inspector.get_columns("accounting_periods")}
        if "company_id" not in period_columns:
            statements.append("ALTER TABLE accounting_periods ADD COLUMN company_id INTEGER")
    if "journal_entries" in table_names:
        journal_columns = {column["name"] for column in inspector.get_columns("journal_entries")}
        if "company_id" not in journal_columns:
            statements.append("ALTER TABLE journal_entries ADD COLUMN company_id INTEGER")
    if statements:
        with engine.begin() as connection:
            for statement in statements:
                connection.execute(text(statement))


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000)
    return f"{salt.hex()}:{digest.hex()}"


def verify_password(password: str, password_hash: str) -> bool:
    salt_hex, digest_hex = password_hash.split(":", 1)
    salt = bytes.fromhex(salt_hex)
    expected = bytes.fromhex(digest_hex)
    actual = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000)
    return hmac.compare_digest(actual, expected)


def create_session_token() -> str:
    return secrets.token_urlsafe(32)


@contextmanager
def db_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_user_by_token(session: Session, token: str) -> Optional[User]:
    auth_session = session.query(AuthSession).filter(AuthSession.token == token).first()
    if not auth_session:
        return None
    return auth_session.user
