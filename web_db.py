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


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(512))
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
    name: Mapped[str] = mapped_column(String(200), index=True)
    description: Mapped[str] = mapped_column(Text, default="")

    source_dir: Mapped[str] = mapped_column(Text, default="")
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
    excel_name: Mapped[str] = mapped_column(String(200), default="document_summary.xlsx")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    user: Mapped[User] = relationship(back_populates="projects")
    documents: Mapped[list["DocumentRecord"]] = relationship(back_populates="project", cascade="all, delete-orphan")


class DocumentRecord(Base):
    __tablename__ = "document_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    source_file: Mapped[str] = mapped_column(String(255))
    source_path: Mapped[str] = mapped_column(Text, default="")
    source_hash: Mapped[str] = mapped_column(String(64), default="")
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
    confidence_score: Mapped[int] = mapped_column(Integer, default=0)
    confidence_label: Mapped[str] = mapped_column(String(32), default="low")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    project: Mapped[Project] = relationship(back_populates="documents")


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    ensure_compatible_schema()


def ensure_compatible_schema() -> None:
    inspector = inspect(engine)
    table_names = set(inspector.get_table_names())
    statements = []

    if "projects" in table_names:
        project_columns = {column["name"] for column in inspector.get_columns("projects")}
        if "archive_source_dir" not in project_columns:
            statements.append("ALTER TABLE projects ADD COLUMN archive_source_dir TEXT DEFAULT ''")
        if "move_processed_source" not in project_columns:
            statements.append("ALTER TABLE projects ADD COLUMN move_processed_source BOOLEAN DEFAULT 0")

    if "document_records" not in table_names:
        if statements:
            with engine.begin() as connection:
                for statement in statements:
                    connection.execute(text(statement))
        return
    columns = {column["name"] for column in inspector.get_columns("document_records")}
    if "source_path" not in columns:
        statements.append(
            "ALTER TABLE document_records ADD COLUMN source_path TEXT DEFAULT ''"
        )
    if "source_hash" not in columns:
        statements.append(
            "ALTER TABLE document_records ADD COLUMN source_hash TEXT DEFAULT ''"
        )
    if "confidence_score" not in columns:
        statements.append(
            "ALTER TABLE document_records ADD COLUMN confidence_score INTEGER DEFAULT 0"
        )
    if "confidence_label" not in columns:
        statements.append(
            "ALTER TABLE document_records ADD COLUMN confidence_label TEXT DEFAULT 'low'"
        )
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
