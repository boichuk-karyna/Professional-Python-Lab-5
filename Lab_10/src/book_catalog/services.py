import csv
import json
from pathlib import Path
from typing import Any

from book_catalog.repositories import BookRepository


class BookImportError(ValueError):
    pass


def import_books_csv(path: str | Path, repository: BookRepository) -> int:
    required = {"title", "author", "year", "pages"}
    try:
        with Path(path).open("r", encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            if not reader.fieldnames or not required.issubset(set(reader.fieldnames)):
                raise BookImportError("CSV must contain title, author, year and pages columns")
            count = 0
            for row_number, row in enumerate(reader, start=2):
                try:
                    repository.create_book(
                        title=(row.get("title") or "").strip(),
                        author_name=(row.get("author") or "").strip(),
                        year=int(row.get("year") or ""),
                        pages=int(row.get("pages") or ""),
                        description=(row.get("description") or "").strip() or None,
                    )
                except (TypeError, ValueError) as exc:
                    raise BookImportError(f"Invalid data on CSV row {row_number}") from exc
                count += 1
            return count
    except OSError as exc:
        raise BookImportError(f"Cannot read CSV file: {path}") from exc


def export_books_json(books: list[dict[str, Any]], path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(books, ensure_ascii=False, indent=2), encoding="utf-8")
