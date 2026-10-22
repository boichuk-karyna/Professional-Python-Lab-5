"""Database engine and SQLAlchemy session factory."""
from pathlib import Path
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

DATABASE_URL = "sqlite:///books.db"


def make_engine(url: str = DATABASE_URL, *, echo: bool = False) -> Engine:
    """Create an engine and enforce SQLite foreign-key constraints."""
    engine = create_engine(url, echo=echo)

    if url.startswith("sqlite"):
        @event.listens_for(engine, "connect")
        def _enable_foreign_keys(dbapi_connection, _connection_record) -> None:
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    return engine


engine = make_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False, class_=Session)


def get_session() -> Session:
    """Return a new application session; caller is responsible for closing it."""
    return SessionLocal()
