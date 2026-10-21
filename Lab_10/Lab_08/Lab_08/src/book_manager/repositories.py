from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from book_manager.models import Author, Book


class AuthorRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all(self) -> list[Author]:
        return list(self.session.scalars(select(Author).order_by(Author.name)).all())

    def get_by_id(self, author_id: int) -> Author | None:
        return self.session.get(Author, author_id)

    def get_by_name(self, name: str) -> Author | None:
        # Python casefold handles Unicode names consistently, including Ukrainian characters.
        normalized = name.strip().casefold()
        return next((author for author in self.session.scalars(select(Author)).all()
                     if author.name.strip().casefold() == normalized), None)

    def add(self, author: Author) -> Author:
        self.session.add(author)
        self.session.commit()
        self.session.refresh(author)
        return author


class BookRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all(
        self,
        author_name: str | None = None,
        year_from: int | None = None,
        year_to: int | None = None,
        page: int = 1,
        page_size: int = 10,
        sort_by: str = "title",
        order: str = "asc",
    ) -> tuple[list[Book], int]:
        query = select(Book).options(joinedload(Book.author))
        count_query = select(func.count(Book.id))
        if author_name:
            # SQLite lower() is ASCII-oriented; casefold in Python supports Ukrainian names.
            matching_author_ids = [
                author.id for author in self.session.scalars(select(Author)).all()
                if author_name.casefold() in author.name.casefold()
            ]
            query = query.where(Book.author_id.in_(matching_author_ids))
            count_query = count_query.where(Book.author_id.in_(matching_author_ids))
        if year_from is not None:
            query = query.where(Book.year >= year_from)
            count_query = count_query.where(Book.year >= year_from)
        if year_to is not None:
            query = query.where(Book.year <= year_to)
            count_query = count_query.where(Book.year <= year_to)
        total = int(self.session.scalar(count_query) or 0)
        sort_column = {"title": Book.title, "year": Book.year, "pages": Book.pages}.get(sort_by, Book.title)
        query = query.order_by(sort_column.desc() if order == "desc" else sort_column.asc())
        items = list(self.session.scalars(query.offset((page - 1) * page_size).limit(page_size)).unique().all())
        return items, total

    def get_by_id(self, book_id: int) -> Book | None:
        return self.session.scalar(
            select(Book).options(joinedload(Book.author)).where(Book.id == book_id)
        )

    def get_by_author(self, author_id: int) -> list[Book]:
        return list(
            self.session.scalars(
                select(Book).options(joinedload(Book.author))
                .where(Book.author_id == author_id).order_by(Book.title)
            ).unique().all()
        )

    def add(self, book: Book) -> Book:
        self.session.add(book)
        self.session.commit()
        self.session.refresh(book)
        return self.get_by_id(book.id) or book

    def delete(self, book: Book) -> None:
        self.session.delete(book)
        self.session.commit()

    def statistics(self) -> tuple[int, float, Book | None]:
        total = int(self.session.scalar(select(func.count(Book.id))) or 0)
        average = float(self.session.scalar(select(func.avg(Book.pages))) or 0.0)
        largest = self.session.scalar(
            select(Book).options(joinedload(Book.author)).order_by(Book.pages.desc(), Book.title).limit(1)
        )
        return total, average, largest
