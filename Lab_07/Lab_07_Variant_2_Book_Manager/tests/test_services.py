import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from book_manager.models import Author, Book
from book_manager.repositories import AuthorRepository, BookRepository
from book_manager.services import add_author_with_books

def test_add_author_with_books_commits_atomically(session):
    author = add_author_with_books(session, "Test Author", [
        {"title": "Book One", "year": 2000, "pages": 100},
        {"title": "Book Two", "year": 2001, "pages": 200, "isbn": "ISBN-2001"},
    ])
    assert author.id is not None
    assert len(BookRepository(session).find_by_author("Test Author")) == 2

def test_transaction_rolls_back_all_when_any_book_invalid(session):
    with pytest.raises(IntegrityError):
        add_author_with_books(session, "Should Roll Back", [
            {"title": "Valid", "year": 2000, "pages": 100},
            {"title": "Invalid", "year": 2001, "pages": 0},
        ])
    assert AuthorRepository(session).get_by_name("Should Roll Back") is None
    assert session.scalar(select(Book).where(Book.title.in_(["Valid", "Invalid"]))) is None

def test_duplicate_isbn_rolls_back_author_and_books(session):
    author = AuthorRepository(session).add(Author(name="Existing"))
    BookRepository(session).add(Book(title="Existing ISBN", year=2000, pages=10,
                                     isbn="DUPLICATE", author_id=author.id))
    with pytest.raises(IntegrityError):
        add_author_with_books(session, "New Author", [
            {"title": "Conflict", "year": 2020, "pages": 20, "isbn": "DUPLICATE"}
        ])
    assert AuthorRepository(session).get_by_name("New Author") is None
