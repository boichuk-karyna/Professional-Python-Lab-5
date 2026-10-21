"""Business logic for catalog queries."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from book_catalog.models import Author, Book
from book_catalog.schemas import BookCreate


def add_book(session: Session, data: BookCreate) -> Book:
    """Add a book and create its author if needed."""
    author_name = data.author.strip()
    author = session.scalar(select(Author).where(Author.name == author_name))
    if author is None:
        author = Author(name=author_name)
        session.add(author)
        session.flush()
    book = Book(
        title=data.title.strip(),
        author_id=author.id,
        year=data.year,
        pages=data.pages,
    )
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


def list_books(
    session: Session,
    author: str | None = None,
    year: int | None = None,
) -> list[Book]:
    """Return books optionally filtered by author and publication year."""
    statement = select(Book).options(joinedload(Book.author)).join(Author)
    if author:
        statement = statement.where(Author.name.ilike(f"%{author}%"))
    if year is not None:
        statement = statement.where(Book.year == year)
    return list(session.scalars(statement.order_by(Book.title)).unique().all())


def list_authors(session: Session) -> list[dict[str, int | str]]:
    """Return authors with the number of books in the catalog."""
    statement = (
        select(Author.id, Author.name, func.count(Book.id))
        .outerjoin(Book)
        .group_by(Author.id, Author.name)
        .order_by(Author.name)
    )
    return [
        {"id": author_id, "name": name, "book_count": count}
        for author_id, name, count in session.execute(statement).all()
    ]


def books_by_author(session: Session, author_id: int) -> list[Book] | None:
    """Return an author's books, or None when the author does not exist."""
    author = session.get(Author, author_id)
    if author is None:
        return None
    return list(
        session.scalars(
            select(Book)
            .options(joinedload(Book.author))
            .where(Book.author_id == author_id)
            .order_by(Book.title)
        ).unique().all()
    )


def largest_book(session: Session) -> Book | None:
    """Return the book with the greatest page count."""
    return session.scalar(
        select(Book).options(joinedload(Book.author)).order_by(Book.pages.desc(), Book.id).limit(1)
    )


def average_pages(session: Session) -> float:
    """Return average page count, or zero for an empty catalog."""
    average = session.scalar(select(func.avg(Book.pages)))
    return float(average) if average is not None else 0.0
