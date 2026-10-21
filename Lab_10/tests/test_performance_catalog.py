import pytest

from book_manager.performance_models import Book
from book_manager.performance_catalog import BookCatalog


def test_book_validates_empty_title():
    with pytest.raises(ValueError):
        Book("", "Author", 2000, 100)


def test_book_validates_pages():
    with pytest.raises(ValueError):
        Book("Title", "Author", 2000, 0)


def test_book_validates_year():
    with pytest.raises(ValueError):
        Book("Title", "Author", 2200, 100)


def test_add_and_search_author():
    catalog = BookCatalog([Book("A", "Jane Doe", 2000, 100)])
    catalog.add_book(Book("B", "Jane Doe", 2001, 200))
    assert len(catalog.find_by_author("jane doe")) == 2


def test_filter_by_year():
    catalog = BookCatalog([Book("A", "X", 2000, 100), Book("B", "Y", 2001, 200)])
    assert [b.title for b in catalog.filter_by_year(2001)] == ["B"]


def test_largest_book():
    catalog = BookCatalog([Book("A", "X", 2000, 100), Book("B", "Y", 2001, 200)])
    assert catalog.largest_book().title == "B"


def test_average_pages():
    catalog = BookCatalog([Book("A", "X", 2000, 100), Book("B", "Y", 2001, 200)])
    assert catalog.average_pages() == 150


def test_empty_catalog():
    catalog = BookCatalog()
    assert catalog.largest_book() is None
    assert catalog.average_pages() == 0


def test_json_roundtrip(tmp_path):
    catalog = BookCatalog([Book("Назва", "Автор", 2020, 123)])
    path = tmp_path / "books.json"
    catalog.export_json(path)
    restored = BookCatalog.from_json(path)
    assert restored.all_books() == catalog.all_books()


def test_author_cache_invalidates_after_add():
    catalog = BookCatalog([Book("A", "Jane", 2000, 100)])
    assert catalog.author_statistics("Jane")["count"] == 1
    catalog.add_book(Book("B", "Jane", 2001, 300))
    assert catalog.author_statistics("Jane")["count"] == 2


@pytest.mark.parametrize("pages,expected", [(1, 1), (10, 10), (999, 999)])
def test_page_values(pages, expected):
    assert Book("T", "A", 2000, pages).pages == expected
