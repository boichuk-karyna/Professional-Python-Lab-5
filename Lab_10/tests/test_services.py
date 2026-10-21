import csv
from collections.abc import Generator
import json
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

from book_catalog.database import Base
from book_catalog.repositories import BookRepository
from book_catalog.services import BookImportError, export_books_json, import_books_csv


@pytest.fixture
def repository() -> Generator[BookRepository, None, None]:
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    from sqlalchemy.orm import sessionmaker
    session = sessionmaker(bind=engine, expire_on_commit=False)()
    yield BookRepository(session)
    session.close()
    Base.metadata.drop_all(engine)
    engine.dispose()


def test_csv_import_and_json_export(repository: BookRepository, tmp_path: Path) -> None:
    source = tmp_path / "books.csv"
    with source.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["title", "author", "year", "pages"])
        writer.writeheader()
        writer.writerow({"title": "Pride and Prejudice", "author": "Jane Austen", "year": 1813, "pages": 432})
    assert import_books_csv(source, repository) == 1
    books = repository.list_books(author="Austen")
    target = tmp_path / "out" / "books.json"
    export_books_json([{"title": books[0].title}], target)
    assert json.loads(target.read_text(encoding="utf-8")) == [{"title": "Pride and Prejudice"}]


def test_bad_csv_header_raises(repository: BookRepository, tmp_path: Path) -> None:
    source = tmp_path / "bad.csv"
    source.write_text("name,year\nBook,2000\n", encoding="utf-8")
    with pytest.raises(BookImportError):
        import_books_csv(source, repository)


def test_invalid_csv_row_raises(repository: BookRepository, tmp_path: Path) -> None:
    source = tmp_path / "bad-row.csv"
    source.write_text("title,author,year,pages\nBook,Author,not-year,200\n", encoding="utf-8")
    with pytest.raises(BookImportError):
        import_books_csv(source, repository)


def test_export_empty_list(repository: BookRepository, tmp_path: Path) -> None:
    target = tmp_path / "empty.json"
    export_books_json([], target)
    assert json.loads(target.read_text(encoding="utf-8")) == []
