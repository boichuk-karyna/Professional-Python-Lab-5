import json
import pytest
from unittest.mock import AsyncMock
from books.io import export_json, import_csv
from books.services import BookService
from books.repositories import BookRepository


@pytest.mark.integration
def test_csv_import_search_and_json_export(tmp_path):
    csv_path = tmp_path / "catalog.csv"
    csv_path.write_text(
        "title,author,year,pages\n"
        "The Hobbit,J. R. R. Tolkien,1937,310\n"
        "The Lord of the Rings,J. R. R. Tolkien,1954,1178\n"
        "Emma,Jane Austen,1815,474\n",
        encoding="utf-8",
    )
    service = BookService(BookRepository(), year_range=(1, 2100))
    assert import_csv(csv_path, service) == (3, 0)
    matches = service.search_by_author("tolkien")
    assert len(matches) == 2
    output = tmp_path / "report.json"
    export_json(output, matches)
    data = json.loads(output.read_text(encoding="utf-8"))
    assert {item["title"] for item in data} == {"The Hobbit", "The Lord of the Rings"}


@pytest.mark.integration
def test_config_controls_imported_book_year(tmp_path, monkeypatch):
    monkeypatch.setenv("BOOKS_MIN_YEAR", "1900")
    monkeypatch.setenv("BOOKS_MAX_YEAR", "2000")
    from books.config import get_year_range
    service = BookService(BookRepository(), year_range=get_year_range())
    csv_path = tmp_path / "old.csv"
    csv_path.write_text("title,author,year,pages\nOld book,Author,1800,50\n", encoding="utf-8")
    with pytest.raises(Exception):
        import_csv(csv_path, service)


@pytest.mark.integration
async def test_async_external_catalog_import_then_search_export(tmp_path):
    external = AsyncMock()
    external.fetch_books.return_value = [
        {"title": "Dune", "author": "Frank Herbert", "year": 1965, "pages": 412},
        {"title": "Emma", "author": "Jane Austen", "year": 1815, "pages": 474},
    ]
    service = BookService(BookRepository(), year_range=(1, 2100))
    imported = await service.import_external(external)
    external.fetch_books.assert_awaited_once_with()
    assert len(imported) == 2
    result = service.search_by_author("herbert")
    out = tmp_path / "external.json"
    export_json(out, result)
    assert json.loads(out.read_text(encoding="utf-8"))[0]["title"] == "Dune"
