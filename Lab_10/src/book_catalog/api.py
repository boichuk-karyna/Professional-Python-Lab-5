import asyncio
from collections.abc import Generator

import logging

from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from book_catalog.config import get_settings
from book_catalog.database import get_session
from book_catalog.external_api import fetch_many_author_books
from book_catalog.models import Author, Book
from book_catalog.repositories import AuthorRepository, BookRepository
from book_catalog.schemas import (
    AuthorCreate, AuthorResponse, BatchAuthorsRequest, BookCreate, BookListResponse,
    BookPatch, BookResponse, BookStatistics,
)
from book_catalog.services import BookService, DuplicateResourceError, ResourceNotFoundError

settings = get_settings()
logging.basicConfig(
    level=settings.log_level.upper(),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("book_catalog")

app = FastAPI(
    title=settings.app_name,
    description="Асинхронний REST API для обліку книг та авторів (Лабораторна робота №8, варіант 2).",
    version="1.0.0",
)


def session_dependency() -> Generator[Session, None, None]:
    yield from get_session()


def book_response(book: Book) -> BookResponse:
    return BookResponse(
        id=book.id, title=book.title, year=book.year, pages=book.pages,
        isbn=book.isbn, author_id=book.author_id, author_name=book.author.name,
    )


@app.get("/", tags=["system"])
async def root() -> dict[str, str]:
    return {"message": "Book Manager API is running", "docs": "/docs"}


@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    return {"status": "ok", "environment": settings.environment}


@app.get("/books", response_model=BookListResponse, tags=["books"])
async def list_books(
    author_name: str | None = Query(default=None, min_length=1),
    year_from: int | None = Query(default=None, ge=1, le=2100),
    year_to: int | None = Query(default=None, ge=1, le=2100),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    sort_by: str = Query(default="title", pattern="^(title|year|pages)$"),
    order: str = Query(default="asc", pattern="^(asc|desc)$"),
    session: Session = Depends(session_dependency),
) -> BookListResponse:
    if year_from is not None and year_to is not None and year_from > year_to:
        raise HTTPException(status_code=422, detail="year_from must not exceed year_to")
    items, total = BookRepository(session).get_all(
        author_name, year_from, year_to, page, page_size, sort_by, order
    )
    return BookListResponse(items=[book_response(book) for book in items], total=total, page=page, page_size=page_size)


@app.get("/books/statistics", response_model=BookStatistics, tags=["books"])
async def book_statistics(session: Session = Depends(session_dependency)) -> BookStatistics:
    total, average, largest = BookRepository(session).statistics()
    return BookStatistics(
        total_books=total,
        average_pages=round(average, 2),
        largest_book=book_response(largest) if largest else None,
    )


@app.get("/books/{book_id}", response_model=BookResponse, tags=["books"])
async def get_book(book_id: int, session: Session = Depends(session_dependency)) -> BookResponse:
    book = BookRepository(session).get_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book_response(book)


@app.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED, tags=["books"])
async def create_book(data: BookCreate, session: Session = Depends(session_dependency)) -> BookResponse:
    try:
        return book_response(BookService(session).create_book(data))
    except DuplicateResourceError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@app.patch("/books/{book_id}", response_model=BookResponse, tags=["books"])
async def update_book(book_id: int, data: BookPatch, session: Session = Depends(session_dependency)) -> BookResponse:
    if not data.model_fields_set:
        raise HTTPException(status_code=422, detail="At least one field must be supplied")
    try:
        return book_response(BookService(session).update_book(book_id, data))
    except ResourceNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except DuplicateResourceError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["books"])
async def delete_book(book_id: int, session: Session = Depends(session_dependency)) -> Response:
    try:
        BookService(session).delete_book(book_id)
    except ResourceNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/authors", response_model=list[AuthorResponse], tags=["authors"])
async def list_authors(session: Session = Depends(session_dependency)) -> list[Author]:
    return AuthorRepository(session).get_all()


@app.post("/authors", response_model=AuthorResponse, status_code=status.HTTP_201_CREATED, tags=["authors"])
async def create_author(data: AuthorCreate, session: Session = Depends(session_dependency)) -> Author:
    try:
        return BookService(session).create_author(data.name, data.biography)
    except DuplicateResourceError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@app.get("/authors/{author_id}/books", response_model=list[BookResponse], tags=["authors"])
async def get_author_books(author_id: int, session: Session = Depends(session_dependency)) -> list[BookResponse]:
    author = AuthorRepository(session).get_by_id(author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return [book_response(book) for book in BookRepository(session).get_by_author(author_id)]


@app.post("/authors/batch-books", tags=["async"])
async def batch_author_books(data: BatchAuthorsRequest) -> dict[str, list[dict]]:
    try:
        results = await fetch_many_author_books(data.author_ids)
    except asyncio.TimeoutError as exc:
        raise HTTPException(status_code=504, detail="Batch request timed out") from exc
    except (httpx_error_types()) as exc:
        raise HTTPException(status_code=502, detail=f"External API request failed: {exc}") from exc
    return {"results": results}


def httpx_error_types() -> tuple[type[BaseException], ...]:
    import httpx
    return (httpx.RequestError, httpx.HTTPStatusError, ValueError, RuntimeError)
