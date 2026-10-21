from __future__ import annotations
from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Author(Base):
    __tablename__ = "authors"
    __table_args__ = ()
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    biography: Mapped[str | None] = mapped_column(Text, nullable=True)
    books: Mapped[list["Book"]] = relationship(
        back_populates="author", cascade="all, delete-orphan", passive_deletes=True
    )

    def __repr__(self) -> str:
        return f"Author(id={self.id!r}, name={self.name!r})"

class Book(Base):
    __tablename__ = "books"
    __table_args__ = (
        CheckConstraint("year >= 0 AND year <= 2100", name="ck_books_year"),
        CheckConstraint("pages > 0", name="ck_books_pages"),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    pages: Mapped[int] = mapped_column(Integer, nullable=False)
    isbn: Mapped[str | None] = mapped_column(String(20), nullable=True, unique=True)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.id", ondelete="CASCADE"), nullable=False, index=True
    )
    author: Mapped[Author] = relationship(back_populates="books")

    def __repr__(self) -> str:
        return f"Book(id={self.id!r}, title={self.title!r}, year={self.year!r})"
