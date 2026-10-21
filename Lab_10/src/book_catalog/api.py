"""FastAPI routes for the book catalog."""
import logging
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI, HTTPException, Query

from book_catalog.config import get_settings
from book_catalog.database import init_db
from book_catalog.models import Author, Book, BookCreate
from book_catalog import repositories

settings = get_settings()
logging.basicConfig(level=settings.log_level.upper(), format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    init_db()
    logger.info("Book Catalog started in %s environment", settings.environment)
    yield


app = FastAPI(title=settings.app_name, version="1.0.0", description="Book catalog API for Lab 10, variant 2", lifespan=lifespan)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "environment": settings.environment}


@app.post("/books", response_model=Book, status_code=201)
def add_book(book: BookCreate) -> dict[str, object]:
    return repositories.create_book(book)


@app.get("/books", response_model=list[Book])
def get_books(author: str | None = None, year: int | None = Query(default=None, gt=0)) -> list[dict[str, object]]:
    """List books; optionally search by author or filter by publication year."""
    return repositories.list_books(author=author, year=year)


@app.get("/books/statistics/largest", response_model=Book | None)
def get_largest_book() -> dict[str, object] | None:
    return repositories.largest_book()


@app.get("/books/statistics/average-pages")
def get_average_pages() -> dict[str, float | int]:
    return {"average_pages": round(repositories.average_pages(), 2), "count": len(repositories.list_books())}


@app.get("/authors", response_model=list[Author])
def get_authors() -> list[dict[str, object]]:
    return repositories.list_authors()


@app.get("/authors/{author_id}/books", response_model=list[Book])
def get_author_books(author_id: int) -> list[dict[str, object]]:
    authors = {author["id"] for author in repositories.list_authors()}
    if author_id not in authors:
        raise HTTPException(status_code=404, detail="Author not found")
    return repositories.author_books(author_id)
