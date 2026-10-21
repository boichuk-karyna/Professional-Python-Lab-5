from book_manager.models import Author, Book
from book_manager.performance import (
    cached_author_summary,
    clear_analytics_cache,
    page_statistics_numpy,
    page_statistics_python,
)


def make_books() -> list[Book]:
    author = Author(id=1, name="Test Author")
    return [
        Book(id=1, title="Book One", year=2000, pages=100, author=author),
        Book(id=2, title="Book Two", year=2001, pages=300, author=author),
    ]


def test_python_and_numpy_page_statistics_match() -> None:
    books = make_books()
    assert page_statistics_python(books) == page_statistics_numpy(books)


def test_page_statistics_for_empty_catalog() -> None:
    assert page_statistics_numpy([])["count"] == 0
    assert page_statistics_python([])["average"] == 0.0


def test_cached_author_summary() -> None:
    clear_analytics_cache()
    count, average, largest = cached_author_summary(make_books(), "test author")
    assert (count, average, largest) == (2, 200.0, 300)
