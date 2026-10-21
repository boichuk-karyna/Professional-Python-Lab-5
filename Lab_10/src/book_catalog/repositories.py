"""Persistence operations for books."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from book_catalog.models import Book
from book_catalog.schemas import BookCreate, BookUpdate


class BookRepository:
    """Encapsulate database queries for the book catalog."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def list_books(
        self,
        author: str | None = None,
        year: int | None = None,
        search: str | None = None,
    ) -> list[Book]:
        """List books with optional author, year and title filters."""
        statement = select(Book)
        if author:
            statement = statement.where(Book.author.ilike(f"%{author}%"))
        if year is not None:
            statement = statement.where(Book.year == year)
        if search:
            statement = statement.where(Book.title.ilike(f"%{search}%"))
        statement = statement.order_by(Book.title, Book.id)
        return list(self.session.scalars(statement).all())

    def get(self, book_id: int) -> Book | None:
        """Return a book by its identifier."""
        return self.session.get(Book, book_id)

    def add(self, data: BookCreate) -> Book:
        """Persist a new book."""
        book = Book(**data.model_dump())
        self.session.add(book)
        self.session.commit()
        self.session.refresh(book)
        return book

    def update(self, book: Book, data: BookUpdate) -> Book:
        """Update only fields explicitly provided by the client."""
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(book, field, value)
        self.session.commit()
        self.session.refresh(book)
        return book

    def delete(self, book: Book) -> None:
        """Delete a book from the catalog."""
        self.session.delete(book)
        self.session.commit()

    def authors(self) -> list[str]:
        """Return distinct author names in alphabetical order."""
        statement = select(Book.author).distinct().order_by(Book.author)
        return list(self.session.scalars(statement).all())

    def author_books(self, author_id: int) -> list[Book] | None:
        """Return books for an author identified by its one-based list position."""
        authors = self.authors()
        if author_id < 1 or author_id > len(authors):
            return None
        author = authors[author_id - 1]
        statement = select(Book).where(Book.author == author).order_by(Book.title)
        return list(self.session.scalars(statement).all())

    def statistics(self) -> tuple[int, float, Book | None]:
        """Calculate count, average page count and the largest book."""
        total = self.session.scalar(select(func.count(Book.id))) or 0
        average = self.session.scalar(select(func.avg(Book.pages))) or 0.0
        largest = self.session.scalar(
            select(Book).order_by(Book.pages.desc(), Book.title).limit(1)
        )
        return int(total), float(average), largest
