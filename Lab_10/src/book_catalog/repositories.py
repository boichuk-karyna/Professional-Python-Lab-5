"""Database access layer for authors and books."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from book_catalog.models import Author, Book


class AuthorRepository:
    """Persistence operations for authors."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, name: str) -> Author:
        author = Author(name=name.strip())
        self.session.add(author)
        self.session.commit()
        self.session.refresh(author)
        return author

    def list(self) -> list[Author]:
        return list(self.session.scalars(select(Author).order_by(Author.name)).all())

    def get(self, author_id: int) -> Author | None:
        return self.session.get(Author, author_id)


class BookRepository:
    """Persistence operations and queries for books."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, title: str, author_id: int, year: int, pages: int) -> Book:
        book = Book(
            title=title.strip(),
            author_id=author_id,
            year=year,
            pages=pages,
        )
        self.session.add(book)
        self.session.commit()
        self.session.refresh(book)
        return book

    def list(self, year: int | None = None) -> list[Book]:
        statement = select(Book).order_by(Book.id)
        if year is not None:
            statement = statement.where(Book.year == year)
        return list(self.session.scalars(statement).all())

    def find_by_author(self, query: str) -> list[Book]:
        statement = (
            select(Book)
            .join(Author)
            .where(Author.name.ilike(f"%{query.strip()}%"))
            .order_by(Book.id)
        )
        return list(self.session.scalars(statement).all())

    def by_author_id(self, author_id: int) -> list[Book]:
        return list(
            self.session.scalars(
                select(Book).where(Book.author_id == author_id).order_by(Book.id)
            ).all()
        )

    def statistics(self) -> dict[str, object]:
        count = self.session.scalar(select(func.count(Book.id))) or 0
        average = self.session.scalar(select(func.avg(Book.pages)))
        largest = self.session.scalar(
            select(Book).order_by(Book.pages.desc(), Book.id).limit(1)
        )
        return {
            "count": int(count),
            "average_pages": float(average) if average is not None else None,
            "largest_book": largest,
        }
