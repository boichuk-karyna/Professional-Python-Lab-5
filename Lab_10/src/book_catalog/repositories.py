from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from book_catalog.models import Author, Book


class BookRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_books(
        self,
        author: str | None = None,
        year: int | None = None,
        query: str | None = None,
    ) -> list[Book]:
        statement = select(Book).options(joinedload(Book.author)).join(Author)
        if author:
            statement = statement.where(Author.name.ilike(f"%{author.strip()}%"))
        if year is not None:
            statement = statement.where(Book.year == year)
        if query:
            statement = statement.where(Book.title.ilike(f"%{query.strip()}%"))
        return list(self.session.scalars(statement.order_by(Book.id)).unique().all())

    def get_book(self, book_id: int) -> Book | None:
        statement = select(Book).options(joinedload(Book.author)).where(Book.id == book_id)
        return self.session.scalars(statement).unique().first()

    def get_or_create_author(self, name: str) -> Author:
        cleaned = name.strip()
        author = self.session.scalars(
            select(Author).where(func.lower(Author.name) == cleaned.lower())
        ).first()
        if author is None:
            author = Author(name=cleaned)
            self.session.add(author)
            self.session.flush()
        return author

    def create_book(
        self, title: str, author_name: str, year: int, pages: int, description: str | None = None
    ) -> Book:
        author = self.get_or_create_author(author_name)
        book = Book(
            title=title.strip(),
            author=author,
            year=year,
            pages=pages,
            description=description,
        )
        self.session.add(book)
        self.session.commit()
        self.session.refresh(book)
        return self.get_book(book.id) or book

    def delete_book(self, book_id: int) -> bool:
        book = self.session.get(Book, book_id)
        if book is None:
            return False
        self.session.delete(book)
        self.session.commit()
        return True

    def list_authors(self) -> list[Author]:
        return list(self.session.scalars(select(Author).order_by(Author.name)).all())

    def get_author(self, author_id: int) -> Author | None:
        return self.session.get(Author, author_id)

    def books_by_author(self, author_id: int) -> list[Book]:
        statement = (
            select(Book)
            .options(joinedload(Book.author))
            .where(Book.author_id == author_id)
            .order_by(Book.id)
        )
        return list(self.session.scalars(statement).unique().all())

    def statistics(self) -> tuple[int, float | None, Book | None]:
        count = int(self.session.scalar(select(func.count(Book.id))) or 0)
        average = self.session.scalar(select(func.avg(Book.pages)))
        largest_statement = (
            select(Book).options(joinedload(Book.author)).order_by(Book.pages.desc(), Book.id).limit(1)
        )
        largest = self.session.scalars(largest_statement).unique().first()
        return count, float(average) if average is not None else None, largest
