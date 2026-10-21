"""Unit tests for book catalog business rules."""

import pytest
from pydantic import ValidationError

from book_catalog.schemas import BookCreate, BookUpdate


def test_book_create_schema_accepts_valid_data() -> None:
    book = BookCreate(title="Title", author="Author", year=2020, pages=100)
    assert book.pages == 100


@pytest.mark.parametrize("pages", [0, -1])
def test_book_pages_must_be_positive(pages: int) -> None:
    with pytest.raises(ValidationError):
        BookCreate(title="Title", author="Author", year=2020, pages=pages)


@pytest.mark.parametrize("year", [-1, 2101])
def test_book_year_must_be_in_range(year: int) -> None:
    with pytest.raises(ValidationError):
        BookCreate(title="Title", author="Author", year=year, pages=100)


def test_update_schema_allows_partial_updates() -> None:
    update = BookUpdate(pages=250)
    assert update.model_dump(exclude_unset=True) == {"pages": 250}
