"""SQLAlchemy database models."""

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from book_catalog.database import Base


class Author(Base):
    """Author entity."""

    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    books: Mapped[list["Book"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan",
    )


class Book(Base):
    """Book entity with a required author."""

    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False, index=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    pages: Mapped[int] = mapped_column(Integer, nullable=False)
    author: Mapped[Author] = relationship(back_populates="books")
