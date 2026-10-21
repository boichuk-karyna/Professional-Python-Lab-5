from __future__ import annotations

import csv
import json
from pathlib import Path
from threading import RLock
from typing import Iterable

from .performance_models import Book


class BookCatalog:
    """Thread-safe in-memory catalog with version-aware cached statistics."""

    def __init__(self, books: Iterable[Book] = ()) -> None:
        self._books = list(books)
        self._version = 0
        self._lock = RLock()
        self._author_cache: dict[tuple[str, int], dict[str, float | int]] = {}

    @property
    def version(self) -> int:
        return self._version

    def all_books(self) -> list[Book]:
        with self._lock:
            return list(self._books)

    def add_book(self, book: Book) -> None:
        with self._lock:
            self._books.append(book)
            self._version += 1
            self._author_cache.clear()

    def find_by_author(self, author: str) -> list[Book]:
        key = author.casefold()
        with self._lock:
            return [book for book in self._books if book.author.casefold() == key]

    def filter_by_year(self, year: int) -> list[Book]:
        with self._lock:
            return [book for book in self._books if book.year == year]

    def largest_book(self) -> Book | None:
        with self._lock:
            return max(self._books, key=lambda book: book.pages, default=None)

    def average_pages(self) -> float:
        with self._lock:
            return sum(book.pages for book in self._books) / len(self._books) if self._books else 0.0

    def author_statistics(self, author: str) -> dict[str, float | int]:
        key = (author.casefold(), self._version)
        with self._lock:
            if key not in self._author_cache:
                books = [b for b in self._books if b.author.casefold() == author.casefold()]
                self._author_cache[key] = {
                    "count": len(books),
                    "average_pages": sum(b.pages for b in books) / len(books) if books else 0.0,
                    "max_pages": max((b.pages for b in books), default=0),
                }
            return dict(self._author_cache[key])

    def export_json(self, path: str | Path) -> None:
        with self._lock:
            rows = [book.__dict__ if hasattr(book, "__dict__") else {
                "title": book.title, "author": book.author, "year": book.year, "pages": book.pages
            } for book in self._books]
        Path(path).write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    @classmethod
    def from_json(cls, path: str | Path) -> "BookCatalog":
        rows = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(Book(**row) for row in rows)

    @classmethod
    def from_csv(cls, path: str | Path) -> "BookCatalog":
        with Path(path).open(encoding="utf-8", newline="") as stream:
            return cls(Book(row["title"], row["author"], int(row["year"]), int(row["pages"]))
                       for row in csv.DictReader(stream))
