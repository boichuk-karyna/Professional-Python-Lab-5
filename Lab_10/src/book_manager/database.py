"""SQLAlchemy setup with configurable URL and persistent SQLite storage."""

from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from book_manager.config import get_settings

settings = get_settings()
DATABASE_URL = settings.database_url
if DATABASE_URL.startswith("sqlite:") and DATABASE_URL != "sqlite:///:memory:":
    # Ensure the parent directory exists for local and Docker SQLite databases.
    db_path = DATABASE_URL.removeprefix("sqlite:///")
    if db_path and db_path != ":memory:":
        Path(db_path).expanduser().parent.mkdir(parents=True, exist_ok=True)
_connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=_connect_args, future=True, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""


def get_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def init_database() -> None:
    """Create tables when the application starts."""
    from book_manager import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
