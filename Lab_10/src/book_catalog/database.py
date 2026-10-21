"""SQLite persistence layer."""
import os
import sqlite3
from pathlib import Path
from typing import Any

from book_catalog.config import get_settings


def _database_path() -> str:
    url = get_settings().database_url
    if url.startswith("sqlite:////"):
        return "/" + url.removeprefix("sqlite:////")
    if url.startswith("sqlite:///"):
        return url.removeprefix("sqlite:///")
    raise ValueError("Only SQLite DATABASE_URL values are supported by this version.")


def connect() -> sqlite3.Connection:
    path = _database_path()
    if path != ":memory:":
        Path(path).parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with connect() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS authors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            );
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author_id INTEGER NOT NULL REFERENCES authors(id),
                year INTEGER NOT NULL CHECK(year > 0),
                pages INTEGER NOT NULL CHECK(pages > 0)
            );
            CREATE INDEX IF NOT EXISTS idx_books_year ON books(year);
            CREATE INDEX IF NOT EXISTS idx_books_author ON books(author_id);
            """
        )


def row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
    return dict(row)
