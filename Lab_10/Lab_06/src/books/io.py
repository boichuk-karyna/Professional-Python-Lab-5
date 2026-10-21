"""CSV import and JSON export helpers."""
import csv
import json
from pathlib import Path
from .models import Book, BookValidationError
from .services import BookService


class BookImportError(ValueError):
    """Raised when a CSV row cannot be imported."""


def import_csv(path: str | Path, service: BookService, *, strict: bool = True) -> tuple[int, int]:
    """Import CSV records. Return (imported_count, invalid_count)."""
    imported = invalid = 0
    try:
        with Path(path).open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            required = {"title", "author", "year", "pages"}
            if not reader.fieldnames or not required.issubset(set(reader.fieldnames)):
                raise BookImportError("CSV must contain title, author, year, pages columns.")
            for line_number, row in enumerate(reader, start=2):
                try:
                    book = Book(
                        title=row["title"],
                        author=row["author"],
                        year=int(row["year"]),
                        pages=int(row["pages"]),
                    )
                    service.add_book(book)
                    imported += 1
                except (ValueError, TypeError, KeyError) as exc:
                    invalid += 1
                    if strict:
                        raise BookImportError(f"Invalid CSV record on line {line_number}.") from exc
    except OSError as exc:
        raise BookImportError(f"Cannot read CSV file: {path}") from exc
    return imported, invalid


def export_json(path: str | Path, books: list[Book]) -> None:
    """Write books to JSON, creating parent directories if needed."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".tmp")
    try:
        temporary.write_text(
            json.dumps([book.to_dict() for book in books], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        temporary.replace(destination)
    except OSError:
        temporary.unlink(missing_ok=True)
        raise
