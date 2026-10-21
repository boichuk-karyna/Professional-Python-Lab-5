"""FastAPI routes for the book catalog."""

import logging
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from book_catalog.config import get_settings
from book_catalog.database import create_db_and_tables, get_session
from book_catalog.models import Book
from book_catalog.repositories import BookRepository
from book_catalog.schemas import BookCreate, BookRead, BookUpdate, CatalogStatistics
from book_catalog.services import BookService

settings = get_settings()
logging.basicConfig(
    level=settings.log_level.upper(),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Initialize persistent storage when the application starts."""
    create_db_and_tables()
    logger.info("Book Catalog API started in %s environment", settings.environment)
    yield


app = FastAPI(
    title=settings.app_name,
    description="API для додавання, пошуку та аналізу каталогу книг.",
    version="1.0.0",
    lifespan=lifespan,
)


def get_book_or_404(book_id: int, session: Session) -> Book:
    """Return a book or raise a standard 404 response."""
    book = BookRepository(session).get(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Книгу не знайдено.")
    return book


@app.get("/health", tags=["System"])
def health() -> dict[str, str]:
    """Return application health and environment."""
    return {"status": "ok", "environment": settings.environment}


@app.post("/books", response_model=BookRead, status_code=status.HTTP_201_CREATED, tags=["Books"])
def create_book(
    data: BookCreate, session: Session = Depends(get_session)
) -> Book:
    """Create a book record."""
    try:
        return BookService(BookRepository(session)).create_book(data)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@app.get("/books", response_model=list[BookRead], tags=["Books"])
def list_books(
    author: str | None = Query(default=None, description="Фільтр за автором"),
    year: int | None = Query(default=None, ge=0, description="Фільтр за роком"),
    search: str | None = Query(default=None, description="Пошук у назві"),
    session: Session = Depends(get_session),
) -> list[Book]:
    """List books and apply optional filters."""
    return BookRepository(session).list_books(author=author, year=year, search=search)


@app.get("/books/statistics", response_model=CatalogStatistics, tags=["Books"])
def statistics(session: Session = Depends(get_session)) -> CatalogStatistics:
    """Return total books, average pages and the largest book."""
    return BookService(BookRepository(session)).statistics()


@app.get("/books/{book_id}", response_model=BookRead, tags=["Books"])
def read_book(book_id: int, session: Session = Depends(get_session)) -> Book:
    """Get one book by identifier."""
    return get_book_or_404(book_id, session)


@app.patch("/books/{book_id}", response_model=BookRead, tags=["Books"])
def update_book(
    book_id: int,
    data: BookUpdate,
    session: Session = Depends(get_session),
) -> Book:
    """Update a book."""
    book = get_book_or_404(book_id, session)
    try:
        return BookService(BookRepository(session)).update_book(book, data)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Books"])
def delete_book(book_id: int, session: Session = Depends(get_session)) -> Response:
    """Delete a book."""
    repository = BookRepository(session)
    repository.delete(get_book_or_404(book_id, session))
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/authors", response_model=list[str], tags=["Authors"])
def list_authors(session: Session = Depends(get_session)) -> list[str]:
    """List distinct authors alphabetically."""
    return BookRepository(session).authors()


@app.get("/authors/{author_id}/books", response_model=list[BookRead], tags=["Authors"])
def list_author_books(
    author_id: int, session: Session = Depends(get_session)
) -> list[Book]:
    """List books for an author using their one-based ID in the sorted author list."""
    books = BookRepository(session).author_books(author_id)
    if books is None:
        raise HTTPException(status_code=404, detail="Автора не знайдено.")
    return books
