"""Database engine and session management."""

from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from book_catalog.config import get_settings


class Base(DeclarativeBase):
    """Base class for ORM models."""


def _make_engine():
    url = get_settings().database_url
    connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
    if url.startswith("sqlite:///./"):
        Path(url.removeprefix("sqlite:///./")).parent.mkdir(parents=True, exist_ok=True)
    return create_engine(url, connect_args=connect_args, pool_pre_ping=True)


engine = _make_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_session() -> Generator[Session, None, None]:
    """Yield a database session and always close it."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
