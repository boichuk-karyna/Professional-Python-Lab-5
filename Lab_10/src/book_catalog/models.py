"""SQLAlchemy persistence models."""

from sqlalchemy import CheckConstraint, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from book_catalog.database import Base


class Book(Base):
    """Book record stored in the catalog."""

    __tablename__ = "books"
    __table_args__ = (
        CheckConstraint("year >= 0", name="ck_book_year_nonnegative"),
        CheckConstraint("pages > 0", name="ck_book_pages_positive"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(250), index=True, nullable=False)
    author: Mapped[str] = mapped_column(String(200), index=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    pages: Mapped[int] = mapped_column(Integer, nullable=False)
