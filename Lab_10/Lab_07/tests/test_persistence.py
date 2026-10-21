import sqlite3
import pytest
from sqlalchemy.exc import IntegrityError

from books.models import Author, Book
from books.repositories import AuthorRepository, BookRepository
from books.services import add_author_with_books


pytestmark = pytest.mark.integration


def seed(session):
    author = AuthorRepository(session).add("Jane Austen")
    repo = BookRepository(session)
    first = repo.add(Book(title="Pride and Prejudice", year=1813, pages=432, author_id=author.id, isbn="978-1111111111"))
    second = repo.add(Book(title="Emma", year=1815, pages=474, author_id=author.id, isbn="978-2222222222"))
    return author, first, second


def test_create_author_and_book(session):
    author = AuthorRepository(session).add("George Orwell")
    saved = BookRepository(session).add(Book(title="1984", year=1949, pages=328, author_id=author.id))
    assert author.id is not None
    assert saved.id is not None
    assert saved.title == "1984"


def test_read_author_and_book(session):
    author, book, _ = seed(session)
    assert AuthorRepository(session).get_by_id(author.id).name == "Jane Austen"
    assert BookRepository(session).get_by_id(book.id).title == "Pride and Prejudice"


def test_get_all_authors_and_books(session):
    seed(session)
    assert len(AuthorRepository(session).get_all()) == 1
    assert len(BookRepository(session).get_all()) == 2


def test_update_author(session):
    author = AuthorRepository(session).add("Old Name")
    updated = AuthorRepository(session).update(author.id, name="New Name")
    assert updated.name == "New Name"


def test_update_book(session):
    _, book, _ = seed(session)
    updated = BookRepository(session).update(book.id, title="P&P Revised", pages=450)
    assert updated.title == "P&P Revised"
    assert updated.pages == 450


def test_delete_book(session):
    _, book, _ = seed(session)
    repo = BookRepository(session)
    assert repo.delete(book.id) is True
    assert repo.get_by_id(book.id) is None


def test_delete_author_cascades_books(session):
    author, _, _ = seed(session)
    assert AuthorRepository(session).delete(author.id) is True
    assert AuthorRepository(session).get_by_id(author.id) is None
    assert BookRepository(session).count() == 0


def test_relationship_author_books(session):
    author, _, _ = seed(session)
    loaded = session.get(Author, author.id)
    assert sorted(book.title for book in loaded.books) == ["Emma", "Pride and Prejudice"]


def test_find_by_author(session):
    author, _, _ = seed(session)
    found = BookRepository(session).find_by_author(author.name)
    assert [book.title for book in found] == ["Emma", "Pride and Prejudice"]


def test_filter_by_year(session):
    seed(session)
    assert [b.title for b in BookRepository(session).filter_by_year(1815)] == ["Emma"]
    assert BookRepository(session).filter_by_year(1900) == []


def test_largest_book(session):
    seed(session)
    assert BookRepository(session).largest_book().title == "Emma"


def test_average_pages(session):
    seed(session)
    assert BookRepository(session).average_pages() == pytest.approx(453.0)


def test_isbn_unique_constraint(session):
    author = AuthorRepository(session).add("Author")
    repo = BookRepository(session)
    repo.add(Book(title="First", year=2000, pages=100, author_id=author.id, isbn="ISBN-UNIQUE"))
    with pytest.raises(IntegrityError):
        repo.add(Book(title="Second", year=2001, pages=120, author_id=author.id, isbn="ISBN-UNIQUE"))
    session.rollback()


def test_invalid_pages_constraint(session):
    author = AuthorRepository(session).add("Author")
    with pytest.raises(IntegrityError):
        session.add(Book(title="Bad Pages", year=2000, pages=0, author_id=author.id))
        session.commit()
    session.rollback()


def test_transaction_add_author_and_books(session):
    author = add_author_with_books(session, "Mary Shelley", [
        {"title": "Frankenstein", "year": 1818, "pages": 280, "isbn": "ISBN-FRANK"},
        {"title": "The Last Man", "year": 1826, "pages": 360, "isbn": "ISBN-LAST"},
    ])
    assert author.id is not None
    assert len(author.books) == 2
    assert BookRepository(session).count() == 2


def test_transaction_rollback_when_one_book_invalid(session):
    with pytest.raises((ValueError, TypeError, IntegrityError, KeyError)):
        add_author_with_books(session, "Must Roll Back", [
            {"title": "Valid", "year": 2000, "pages": 100},
            {"title": "Invalid", "year": 2000, "pages": 0},
        ])
    assert AuthorRepository(session).get_by_name("Must Roll Back") is None
    assert BookRepository(session).count() == 0


def test_crud_missing_ids(session):
    authors = AuthorRepository(session)
    books = BookRepository(session)
    assert authors.update(999, name="Nobody") is None
    assert authors.delete(999) is False
    assert books.update(999, title="Nobody") is None
    assert books.delete(999) is False


def test_count_empty_and_nonempty(session):
    repo = BookRepository(session)
    assert repo.count() == 0
    seed(session)
    assert repo.count() == 2


def test_db_api_parameterized_query(tmp_path, session):
    author, _, _ = seed(session)
    db_path = tmp_path / "db_api.sqlite"
    raw = sqlite3.connect(db_path)
    raw.execute("PRAGMA foreign_keys=ON")
    raw.executescript("""
        CREATE TABLE authors (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
        CREATE TABLE books (id INTEGER PRIMARY KEY, title TEXT NOT NULL, year INTEGER NOT NULL,
                           pages INTEGER NOT NULL, author_id INTEGER NOT NULL, isbn TEXT,
                           FOREIGN KEY(author_id) REFERENCES authors(id));
    """)
    raw.execute("INSERT INTO authors(id, name) VALUES (?, ?)", (1, author.name))
    raw.execute("INSERT INTO books(id, title, year, pages, author_id, isbn) VALUES (?, ?, ?, ?, ?, ?)",
                (1, "Emma", 1815, 474, 1, None))
    raw.commit()
    raw.close()
    from books.db_api import find_books_by_author
    result = find_books_by_author(db_path, author.name)
    assert len(result) == 1 and result[0][1] == "Emma"
    assert find_books_by_author(db_path, "' OR 1=1 --") == []
