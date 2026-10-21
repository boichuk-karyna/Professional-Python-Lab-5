"""FastAPI endpoints for the Book Catalog."""

import logging
from contextlib import asynccontextmanager
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

from book_catalog.config import get_settings
from book_catalog.database import Base, engine, get_db
from book_catalog.models import Book
from book_catalog.schemas import AuthorRead, BookCreate, BookRead
from book_catalog.services import (
    add_book,
    average_pages,
    books_by_author,
    largest_book,
    list_authors,
    list_books,
)

settings = get_settings()
logging.basicConfig(
    level=settings.log_level.upper(),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Initialize database tables when the application starts."""
    Base.metadata.create_all(bind=engine)
    logger.info("Book Catalog started in %s mode", settings.environment)
    yield


app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)


def serialize_book(book: Book) -> dict[str, Any]:
    """Convert a database book to the public API representation."""
    return {
        "id": book.id,
        "title": book.title,
        "author": book.author.name,
        "year": book.year,
        "pages": book.pages,
    }


@app.get("/health")
def health() -> dict[str, str]:
    """Return application health and environment."""
    return {"status": "ok", "environment": settings.environment}


@app.post("/books", response_model=BookRead, status_code=201)
def create_book(data: BookCreate, session: Session = Depends(get_db)) -> dict[str, Any]:
    """Add a book to the catalog."""
    return serialize_book(add_book(session, data))


@app.get("/books", response_model=list[BookRead])
def get_books(
    author: str | None = Query(default=None, description="Filter by author name"),
    year: int | None = Query(default=None, ge=0, le=2100),
    session: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    """List books with optional author and year filters."""
    return [serialize_book(book) for book in list_books(session, author, year)]


@app.get("/books/statistics")
def book_statistics(session: Session = Depends(get_db)) -> dict[str, Any]:
    """Return largest book and average page count."""
    largest = largest_book(session)
    return {
        "largest_book": serialize_book(largest) if largest else None,
        "average_pages": average_pages(session),
    }


@app.get("/authors", response_model=list[AuthorRead])
def get_authors(session: Session = Depends(get_db)) -> list[dict[str, int | str]]:
    """List authors and the number of books written by each."""
    return list_authors(session)


@app.get("/authors/{author_id}/books", response_model=list[BookRead])
def get_author_books(author_id: int, session: Session = Depends(get_db)) -> list[dict[str, Any]]:
    """List books written by the specified author."""
    books = books_by_author(session, author_id)
    if books is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return [serialize_book(book) for book in books]
