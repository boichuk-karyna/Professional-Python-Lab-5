import json
import pytest
from books.io import BookImportError, export_json, import_csv
from books.models import Book


def test_export_json_round_trip(tmp_path, book):
    path = tmp_path / "nested" / "books.json"
    export_json(path, [book])
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data == [book.to_dict()]


def test_import_csv(tmp_path, service):
    path = tmp_path / "books.csv"
    path.write_text(
        "title,author,year,pages\nThe Hobbit,Tolkien,1937,310\nEmma,Austen,1815,474\n",
        encoding="utf-8",
    )
    assert import_csv(path, service) == (2, 0)
    assert len(service.all_books()) == 2


def test_malformed_csv_strict_mode_raises(tmp_path, service):
    path = tmp_path / "bad.csv"
    path.write_text("title,author,year,pages\nBroken,Writer,not-year,10\n", encoding="utf-8")
    with pytest.raises(BookImportError, match="line 2") as exc_info:
        import_csv(path, service)
    assert exc_info.value.__cause__ is not None


def test_malformed_csv_tolerant_mode_counts_invalid(tmp_path, service):
    path = tmp_path / "mixed.csv"
    path.write_text(
        "title,author,year,pages\nGood,Writer,2000,100\nBad,Writer,abc,20\n",
        encoding="utf-8",
    )
    assert import_csv(path, service, strict=False) == (1, 1)


def test_csv_missing_columns_raises(tmp_path, service):
    path = tmp_path / "missing.csv"
    path.write_text("title,author\nA,B\n", encoding="utf-8")
    with pytest.raises(BookImportError, match="columns"):
        import_csv(path, service)


def test_csv_file_missing_raises(tmp_path, service):
    with pytest.raises(BookImportError, match="Cannot read"):
        import_csv(tmp_path / "absent.csv", service)
