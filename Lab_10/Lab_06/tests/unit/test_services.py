from unittest.mock import Mock
import pytest
from books.models import Book
from books.services import BookService


def make_service(books):
    repository = Mock()
    repository.all.return_value = books
    return BookService(repository, year_range=(1, 2100)), repository


def test_search_by_author(books):
    service, _ = make_service(books)
    assert len(service.search_by_author("tolkien")) == 2
    assert service.search_by_author("nobody") == []


def test_search_by_title(books):
    service, _ = make_service(books)
    assert [b.title for b in service.search_by_title("HOBBIT")] == ["The Hobbit"]


def test_search_ignores_surrounding_spaces(books):
    service, _ = make_service(books)
    assert len(service.search_by_author("  J. R. R. Tolkien  ")) == 2


def test_empty_search_returns_empty(books):
    service, _ = make_service(books)
    assert service.search_by_title("  ") == []


def test_filter_by_year(books):
    service, _ = make_service(books)
    assert [b.title for b in service.filter_by_year(1937)] == ["The Hobbit"]


def test_filter_year_invalid_type(books):
    service, _ = make_service(books)
    with pytest.raises(ValueError, match="integer"):
        service.filter_by_year("1937")


def test_largest_book(books):
    service, _ = make_service(books)
    assert service.largest_book().title == "The Lord of the Rings"


def test_largest_book_empty_catalog():
    service, _ = make_service([])
    assert service.largest_book() is None


def test_average_pages(books):
    service, _ = make_service(books)
    assert service.average_pages() == pytest.approx((310 + 1178 + 432) / 3)


def test_average_pages_empty_catalog():
    service, _ = make_service([])
    assert service.average_pages() == pytest.approx(0.0)


def test_add_book_calls_repository_once(book):
    repository = Mock()
    service = BookService(repository, year_range=(1, 2100))
    assert service.add_book(book) == book
    repository.add.assert_called_once_with(book)


def test_add_book_rejects_year_outside_configuration(book):
    service = BookService(Mock(), year_range=(2000, 2020))
    with pytest.raises(ValueError, match="between"):
        service.add_book(book)


def test_repository_failure_propagates(book):
    repository = Mock()
    repository.add.side_effect = RuntimeError("repository unavailable")
    service = BookService(repository, year_range=(1, 2100))
    with pytest.raises(RuntimeError, match="unavailable"):
        service.add_book(book)


def test_mock_return_value(books):
    repository = Mock()
    repository.all.return_value = books
    service = BookService(repository, year_range=(1, 2100))
    assert len(service.all_books()) == 3
    repository.all.assert_called_once_with()


def test_repository_all_returns_copy(repository, book):
    repository.add(book)
    result = repository.all()
    result.clear()
    assert repository.all() == [book]
