import pytest
from sqlalchemy.exc import IntegrityError
from book_manager.models import Author, Book
from book_manager.repositories import AuthorRepository, BookRepository

def seed(session):
    author = AuthorRepository(session).add(Author(name="Ukrainian Author"))
    repo = BookRepository(session)
    one = repo.add(Book(title="Short Book", year=2001, pages=100, author_id=author.id))
    two = repo.add(Book(title="Long Book", year=2005, pages=500, author_id=author.id))
    return author, one, two

def test_author_crud(session):
    repo = AuthorRepository(session)
    author = repo.add(Author(name="Author A", biography="Bio"))
    assert repo.get_by_id(author.id).name == "Author A"
    assert repo.get_by_name("Author A").id == author.id
    assert len(repo.get_all()) == 1
    updated = repo.update(author.id, name="Author B")
    assert updated.name == "Author B"
    assert repo.delete(author.id) is True
    assert repo.get_by_id(author.id) is None
    assert repo.delete(author.id) is False

def test_book_create_read_update_delete(session):
    author, book, _ = seed(session)
    repo = BookRepository(session)
    loaded = repo.get_by_id(book.id)
    assert loaded is not None and loaded.title == "Short Book"
    updated = repo.update(book.id, title="Updated", pages=150, year=2002)
    assert updated.title == "Updated" and updated.pages == 150 and updated.year == 2002
    assert repo.delete(book.id) is True
    assert repo.get_by_id(book.id) is None
    assert repo.delete(book.id) is False

def test_author_books_relationship(session):
    author, _, _ = seed(session)
    session.refresh(author)
    assert len(author.books) == 2
    assert all(book.author.name == author.name for book in author.books)

def test_find_by_author(session):
    seed(session)
    assert [b.title for b in BookRepository(session).find_by_author("Ukrainian Author")] == ["Long Book", "Short Book"]
    assert BookRepository(session).find_by_author("Missing") == []

def test_filter_by_year(session):
    seed(session)
    repo = BookRepository(session)
    assert [b.title for b in repo.filter_by_year(2001)] == ["Short Book"]
    assert repo.filter_by_year(1900) == []

def test_largest_book(session):
    seed(session)
    assert BookRepository(session).largest_book().title == "Long Book"

def test_average_pages(session):
    seed(session)
    assert BookRepository(session).average_pages() == 300.0

def test_average_pages_empty(session):
    assert BookRepository(session).average_pages() == 0.0

def test_unique_author_name(session):
    repo = AuthorRepository(session)
    repo.add(Author(name="Unique"))
    with pytest.raises(IntegrityError):
        repo.add(Author(name="Unique"))
    session.rollback()

def test_check_constraint_pages(session):
    author = AuthorRepository(session).add(Author(name="Constraint Author"))
    with pytest.raises(IntegrityError):
        BookRepository(session).add(Book(title="Invalid", year=2020, pages=0, author_id=author.id))
    session.rollback()
