from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from book_manager.models import Author, Book
from book_manager.repositories import AuthorRepository, BookRepository
from book_manager.schemas import BookCreate, BookPatch


class DuplicateResourceError(Exception):
    """Raised when a unique book or author already exists."""


class ResourceNotFoundError(Exception):
    """Raised when a requested book or author does not exist."""


class BookService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.books = BookRepository(session)
        self.authors = AuthorRepository(session)

    def create_author(self, name: str, biography: str | None = None) -> Author:
        existing = self.authors.get_by_name(name)
        if existing:
            raise DuplicateResourceError("An author with this name already exists")
        author = Author(name=name, biography=biography)
        try:
            return self.authors.add(author)
        except IntegrityError as exc:
            self.session.rollback()
            raise DuplicateResourceError("An author with this name already exists") from exc

    def create_book(self, data: BookCreate) -> Book:
        author = self.authors.get_by_name(data.author_name)
        if author is None:
            author = Author(name=data.author_name)
            self.session.add(author)
            self.session.flush()
        book = Book(
            title=data.title, year=data.year, pages=data.pages,
            isbn=data.isbn, author_id=author.id,
        )
        try:
            return self.books.add(book)
        except IntegrityError as exc:
            self.session.rollback()
            raise DuplicateResourceError("A book with this ISBN already exists") from exc

    def update_book(self, book_id: int, changes: BookPatch) -> Book:
        book = self.books.get_by_id(book_id)
        if book is None:
            raise ResourceNotFoundError("Book not found")
        data = changes.model_dump(exclude_unset=True)
        author_name = data.pop("author_name", None)
        if author_name is not None:
            author = self.authors.get_by_name(author_name)
            if author is None:
                author = Author(name=author_name)
                self.session.add(author)
                self.session.flush()
            book.author_id = author.id
        for field, value in data.items():
            setattr(book, field, value)
        try:
            self.session.commit()
            return self.books.get_by_id(book_id) or book
        except IntegrityError as exc:
            self.session.rollback()
            raise DuplicateResourceError("A book with this ISBN already exists") from exc

    def delete_book(self, book_id: int) -> None:
        book = self.books.get_by_id(book_id)
        if book is None:
            raise ResourceNotFoundError("Book not found")
        self.books.delete(book)
