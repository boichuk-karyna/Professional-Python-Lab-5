from book_manager.schemas import BookCreate
from pydantic import ValidationError
import pytest


def test_book_create_normalizes_text():
    book = BookCreate(title="  Кобзар  ", author_name=" Тарас Шевченко ", year=1840, pages=320)
    assert book.title == "Кобзар"
    assert book.author_name == "Тарас Шевченко"


def test_book_create_rejects_non_positive_pages():
    with pytest.raises(ValidationError):
        BookCreate(title="Кобзар", author_name="Тарас Шевченко", year=1840, pages=0)


def test_book_create_rejects_year_out_of_range():
    with pytest.raises(ValidationError):
        BookCreate(title="Кобзар", author_name="Тарас Шевченко", year=2200, pages=320)
