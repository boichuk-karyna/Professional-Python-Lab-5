"""FastAPI routes for the Book Catalog service."""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.orm import Session

from book_catalog.config import get_settings
from book_catalog.database import Base, engine, get_session
from book_catalog.models import Author, Book
from book_catalog.repositories import AuthorRepository, BookRepository
from book_catalog.schemas import (
    AuthorCreate,
    AuthorRead,
    BookCreate,
    BookRead,
    BookStatistics,
)

settings = get_settings()
logging.basicConfig(
    level=settings.log_level.upper(),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Initialize database tables when the application starts."""
    Base.metadata.create_all(bind=engine)
    logger.info("Book Catalog API started in %s environment", settings.app_env)
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="REST API for managing books and authors.",
    lifespan=lifespan,
)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    """Return basic application health status."""
    return {"status": "ok", "environment": settings.app_env}


@app.post("/authors", response_model=AuthorRead, status_code=status.HTTP_201_CREATED)
def create_author(
    payload: AuthorCreate,
    session: Session = Depends(get_session),
) -> Author:
    """Create an author."""
    return AuthorRepository(session).create(payload.name)


@app.get("/authors", response_model=list[AuthorRead])
def list_authors(session: Session = Depends(get_session)) -> list[Author]:
    """List all authors."""
    return AuthorRepository(session).list()


@app.post("/books", response_model=BookRead, status_code=status.HTTP_201_CREATED)
def create_book(
    payload: BookCreate,
    session: Session = Depends(get_session),
) -> Book:
    """Create a book after validating that its author exists."""
    if AuthorRepository(session).get(payload.author_id) is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return BookRepository(session).create(
        payload.title, payload.author_id, payload.year, payload.pages
    )


@app.get("/books", response_model=list[BookRead])
def list_books(
    year: int | None = Query(default=None, ge=1, le=2100),
    author: str | None = Query(default=None, min_length=1, max_length=200),
    session: Session = Depends(get_session),
) -> list[Book]:
    """List books, optionally filtered by publication year or author name."""
    repository = BookRepository(session)
    if author:
        books = repository.find_by_author(author)
        if year is not None:
            books = [book for book in books if book.year == year]
        return books
    return repository.list(year=year)


@app.get("/authors/{author_id}/books", response_model=list[BookRead])
def list_author_books(
    author_id: int,
    session: Session = Depends(get_session),
) -> list[Book]:
    """List books belonging to one author."""
    author = AuthorRepository(session).get(author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return BookRepository(session).by_author_id(author_id)


@app.get("/statistics/books", response_model=BookStatistics)
def book_statistics(session: Session = Depends(get_session)) -> dict[str, object]:
    """Return total count, average pages and the largest book."""
    return BookRepository(session).statistics()
