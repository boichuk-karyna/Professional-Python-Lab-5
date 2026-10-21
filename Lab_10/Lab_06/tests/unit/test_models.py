import pytest
from books.models import Book, BookValidationError


def test_book_creation(book):
    assert book.title == "The Hobbit"
    assert book.author == "J. R. R. Tolkien"
    assert book.year == 1937
    assert book.pages == 310


@pytest.mark.parametrize(("field", "value"), [
    ("title", ""), ("title", "   "), ("author", ""), ("author", "  "),
])
def test_required_text_fields_rejected(field, value):
    data = dict(title="Valid title", author="Valid author", year=2000, pages=100)
    data[field] = value
    with pytest.raises(BookValidationError):
        Book(**data)


@pytest.mark.parametrize(("year", "valid"), [
    (1, True), (2000, True), (2100, True), (0, False), (2101, False), (-1, False),
])
def test_year_boundaries(year, valid):
    if valid:
        assert Book("T", "A", year, 1).year == year
    else:
        with pytest.raises(BookValidationError, match="Year"):
            Book("T", "A", year, 1)


@pytest.mark.parametrize("pages", [0, -1, -100])
def test_invalid_page_counts(pages):
    with pytest.raises(BookValidationError, match="Pages"):
        Book("T", "A", 2000, pages)


def test_pages_must_be_integer():
    with pytest.raises(BookValidationError, match="integer"):
        Book("T", "A", 2000, 1.5)


def test_year_must_be_integer():
    with pytest.raises(BookValidationError, match="integer"):
        Book("T", "A", 2000.5, 100)


def test_boolean_year_and_pages_are_rejected():
    with pytest.raises(BookValidationError):
        Book("T", "A", True, 10)
    with pytest.raises(BookValidationError):
        Book("T", "A", 2000, True)


def test_book_to_dict(book):
    assert book.to_dict() == {
        "title": "The Hobbit", "author": "J. R. R. Tolkien",
        "year": 1937, "pages": 310,
    }
