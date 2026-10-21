"""Repository Pattern: persistence operations isolated from business logic."""
from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from .models import Author, Book


class AuthorRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, name: str) -> Author:
        author = Author(name=name.strip())
        self.session.add(author)
        self.session.commit()
        self.session.refresh(author)
        return author

    def get_by_id(self, author_id: int) -> Author | None:
        return self.session.get(Author, author_id)

    def get_by_name(self, name: str) -> Author | None:
        return self.session.scalar(select(Author).where(Author.name == name.strip()))

    def get_all(self) -> list[Author]:
        return list(self.session.scalars(select(Author).order_by(Author.name)))

    def update(self, author_id: int, *, name: str) -> Author | None:
        author = self.get_by_id(author_id)
        if author is None:
            return None
        author.name = name.strip()
        self.session.commit()
        self.session.refresh(author)
        return author

    def delete(self, author_id: int) -> bool:
        author = self.get_by_id(author_id)
        if author is None:
            return False
        self.session.delete(author)
        self.session.commit()
        return True


class BookRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, book: Book) -> Book:
        self.session.add(book)
        self.session.commit()
        self.session.refresh(book)
        return book

    def get_by_id(self, book_id: int) -> Book | None:
        return self.session.scalar(
            select(Book).options(selectinload(Book.author)).where(Book.id == book_id)
        )

    def get_all(self) -> list[Book]:
        return list(self.session.scalars(select(Book).options(selectinload(Book.author)).order_by(Book.id)))

    def update(
        self,
        book_id: int,
        *,
        title: str | None = None,
        year: int | None = None,
        pages: int | None = None,
        author_id: int | None = None,
        isbn: str | None = None,
    ) -> Book | None:
        book = self.get_by_id(book_id)
        if book is None:
            return None
        if title is not None:
            book.title = title.strip()
        if year is not None:
            book.year = year
        if pages is not None:
            book.pages = pages
        if author_id is not None:
            book.author_id = author_id
        if isbn is not None:
            book.isbn = isbn
        self.session.commit()
        self.session.refresh(book)
        return book

    def delete(self, book_id: int) -> bool:
        book = self.get_by_id(book_id)
        if book is None:
            return False
        self.session.delete(book)
        self.session.commit()
        return True

    def find_by_author(self, author_name: str) -> list[Book]:
        statement = (
            select(Book)
            .join(Book.author)
            .options(selectinload(Book.author))
            .where(Author.name == author_name.strip())
            .order_by(Book.title)
        )
        return list(self.session.scalars(statement))

    def filter_by_year(self, year: int) -> list[Book]:
        return list(self.session.scalars(
            select(Book).options(selectinload(Book.author))
            .where(Book.year == year).order_by(Book.title)
        ))

    def largest_book(self) -> Book | None:
        return self.session.scalar(
            select(Book).options(selectinload(Book.author))
            .order_by(Book.pages.desc(), Book.title).limit(1)
        )

    def average_pages(self) -> float:
        result = self.session.scalar(select(func.avg(Book.pages)))
        return float(result) if result is not None else 0.0

    def count(self) -> int:
        return int(self.session.scalar(select(func.count(Book.id))) or 0)
