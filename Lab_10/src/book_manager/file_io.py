"""CSV import and JSON export helpers for the book catalog."""

import csv
import json
from io import StringIO
from typing import Any

from book_manager.models import Book
from book_manager.schemas import BookCreate

CSV_COLUMNS = ("title", "author_name", "year", "pages", "isbn")


def parse_books_csv(content: str) -> list[BookCreate]:
    """Parse and validate CSV rows into typed book input objects."""
    reader = csv.DictReader(StringIO(content))
    if reader.fieldnames is None or not set(CSV_COLUMNS).issubset(reader.fieldnames):
        required = ", ".join(CSV_COLUMNS)
        raise ValueError(f"CSV header must contain: {required}")

    books: list[BookCreate] = []
    for line_number, row in enumerate(reader, start=2):
        try:
            isbn = (row.get("isbn") or "").strip() or None
            books.append(
                BookCreate(
                    title=row.get("title", ""),
                    author_name=row.get("author_name", ""),
                    year=int(row.get("year", "")),
                    pages=int(row.get("pages", "")),
                    isbn=isbn,
                )
            )
        except (ValueError, TypeError) as exc:
            raise ValueError(f"Invalid CSV data on line {line_number}: {exc}") from exc
    return books


def serialize_books_json(books: list[Book]) -> str:
    """Serialize book records to a stable, UTF-8-friendly JSON string."""
    records: list[dict[str, Any]] = [
        {
            "id": book.id,
            "title": book.title,
            "year": book.year,
            "pages": book.pages,
            "isbn": book.isbn,
            "author_id": book.author_id,
            "author_name": book.author.name,
        }
        for book in books
    ]
    return json.dumps(records, ensure_ascii=False, indent=2)
