from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from book_catalog.models import Author, Book


class BookRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_books(
        self,
        author: str | None = None,
        year: int | None = None,
    ) -> list[Book]:
        query = select(Book).options(joinedload(Book.author))
        if author:
            query = query.join(Book.author)
        if year is not None:
            query = query.where(Book.year == year)
        books = list(self.db.scalars(query.order_by(Book.title)).unique().all())
        if author:
            needle = author.casefold()
            books = [book for book in books if needle in book.author.name.casefold()]
        return books

    def get_book(self, book_id: int) -> Book | None:
        return self.db.scalar(
            select(Book)
            .options(joinedload(Book.author))
            .where(Book.id == book_id)
        )

    def get_or_create_author(self, name: str) -> Author:
        normalized = name.strip()
        author = self.db.scalar(
            select(Author).where(func.lower(Author.name) == normalized.lower())
        )
        if author is None:
            author = Author(name=normalized)
            self.db.add(author)
            self.db.flush()
        return author

    def add_book(self, title: str, author_name: str, year: int, pages: int) -> Book:
        author = self.get_or_create_author(author_name)
        book = Book(
            title=title.strip(),
            author=author,
            year=year,
            pages=pages,
        )
        self.db.add(book)
        self.db.commit()
        return self.get_book_after_commit(book)

    def get_book_after_commit(self, book: Book) -> Book:
        self.db.refresh(book)
        return self.get_book(book.id) or book

    def list_authors(self) -> list[Author]:
        return list(self.db.scalars(select(Author).order_by(Author.name)).all())

    def get_author(self, author_id: int) -> Author | None:
        return self.db.get(Author, author_id)

    def books_by_author(self, author_id: int) -> list[Book]:
        query = (
            select(Book)
            .options(joinedload(Book.author))
            .where(Book.author_id == author_id)
            .order_by(Book.title)
        )
        return list(self.db.scalars(query).unique().all())

    def statistics(self) -> tuple[int, float | None, Book | None]:
        count, average = self.db.execute(
            select(func.count(Book.id), func.avg(Book.pages))
        ).one()
        largest = self.db.scalar(
            select(Book).options(joinedload(Book.author))
            .order_by(Book.pages.desc(), Book.title)
            .limit(1)
        )
        return count, float(average) if average is not None else None, largest
