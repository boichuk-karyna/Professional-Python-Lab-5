"""SQLAlchemy models for books and authors."""

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from book_catalog.database import Base


class Author(Base):
    """An author and their catalogued books."""

    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    books: Mapped[list["Book"]] = relationship(back_populates="author")


class Book(Base):
    """A book with its title, author, publication year and page count."""

    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(250), index=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), index=True)
    year: Mapped[int] = mapped_column(Integer, index=True)
    pages: Mapped[int] = mapped_column(Integer)
    author: Mapped[Author] = relationship(back_populates="books")
