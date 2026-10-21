"""Database engine and session dependency."""

from collections.abc import Generator
from pathlib import Path

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from book_catalog.config import get_settings


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""


def build_engine(database_url: str) -> Engine:
    """Create a database engine and prepare a local SQLite directory."""
    connect_args: dict[str, object] = {}
    if database_url.startswith("sqlite:///"):
        raw_path = database_url.removeprefix("sqlite:///")
        if raw_path != ":memory:" and not raw_path.startswith("/"):
            Path(raw_path).parent.mkdir(parents=True, exist_ok=True)
        connect_args = {"check_same_thread": False}
    return create_engine(database_url, connect_args=connect_args, pool_pre_ping=True)


engine = build_engine(get_settings().database_url)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_session() -> Generator[Session, None, None]:
    """Yield a database session and always close it."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def create_db_and_tables() -> None:
    """Create tables required by the application."""
    from book_catalog import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
