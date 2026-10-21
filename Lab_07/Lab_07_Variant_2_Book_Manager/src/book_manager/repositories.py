from __future__ import annotations
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from .models import Author, Book

class AuthorRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, author: Author) -> Author:
        self.session.add(author)
        self.session.commit()
        self.session.refresh(author)
        return author

    def get_by_id(self, author_id: int) -> Author | None:
        return self.session.get(Author, author_id)

    def get_all(self) -> list[Author]:
        return list(self.session.scalars(select(Author).order_by(Author.name)))

    def get_by_name(self, name: str) -> Author | None:
        return self.session.scalar(select(Author).where(Author.name == name))

    def update(self, author_id: int, *, name: str | None = None,
               biography: str | None = None) -> Author | None:
        author = self.get_by_id(author_id)
        if author is None:
            return None
        if name is not None:
            author.name = name
        if biography is not None:
            author.biography = biography
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
        return list(self.session.scalars(
            select(Book).options(selectinload(Book.author)).order_by(Book.title)
        ))

    def update(self, book_id: int, *, title: str | None = None,
               year: int | None = None, pages: int | None = None,
               author_id: int | None = None, isbn: str | None = None) -> Book | None:
        book = self.session.get(Book, book_id)
        if book is None:
            return None
        if title is not None: book.title = title
        if year is not None: book.year = year
        if pages is not None: book.pages = pages
        if author_id is not None: book.author_id = author_id
        if isbn is not None: book.isbn = isbn
        self.session.commit()
        self.session.refresh(book)
        return book

    def delete(self, book_id: int) -> bool:
        book = self.session.get(Book, book_id)
        if book is None:
            return False
        self.session.delete(book)
        self.session.commit()
        return True

    def find_by_author(self, author_name: str) -> list[Book]:
        statement = (
            select(Book).join(Book.author)
            .where(Author.name == author_name)
            .order_by(Book.title)
        )
        return list(self.session.scalars(statement))

    def filter_by_year(self, year: int) -> list[Book]:
        return list(self.session.scalars(
            select(Book).where(Book.year == year).order_by(Book.title)
        ))

    def largest_book(self) -> Book | None:
        return self.session.scalar(
            select(Book).order_by(Book.pages.desc(), Book.title).limit(1)
        )

    def average_pages(self) -> float:
        from sqlalchemy import func
        value = self.session.scalar(select(func.avg(Book.pages)))
        return float(value) if value is not None else 0.0
