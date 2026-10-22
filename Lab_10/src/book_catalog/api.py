import logging
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.orm import Session

from book_catalog.config import get_settings
from book_catalog.database import Base, engine, get_db
from book_catalog.models import Author
from book_catalog.repositories import BookRepository
from book_catalog.schemas import (
    AuthorCreate,
    AuthorRead,
    BookCreate,
    BookRead,
    BookStatistics,
)
from book_catalog.services import BookService, to_book_read

settings = get_settings()
logging.basicConfig(
    level=settings.log_level.upper(),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    logger.info("Book Catalog started in %s environment", settings.environment)
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="REST API for managing a book catalog.",
    lifespan=lifespan,
)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok", "environment": settings.environment}


@app.post("/books", response_model=BookRead, status_code=status.HTTP_201_CREATED,
          tags=["books"])
def create_book(payload: BookCreate, db: Session = Depends(get_db)) -> BookRead:
    service = BookService(BookRepository(db))
    return service.add_book(
        payload.title, payload.author, payload.year, payload.pages
    )


@app.get("/books", response_model=list[BookRead], tags=["books"])
def list_books(
    author: str | None = Query(default=None, min_length=1),
    year: int | None = Query(default=None, ge=0, le=2100),
    db: Session = Depends(get_db),
) -> list[BookRead]:
    return BookService(BookRepository(db)).list_books(author=author, year=year)


@app.get("/books/statistics", response_model=BookStatistics, tags=["books"])
def book_statistics(db: Session = Depends(get_db)) -> BookStatistics:
    count, average, largest = BookRepository(db).statistics()
    return BookStatistics(
        count=count,
        average_pages=round(average, 2) if average is not None else None,
        largest_book=to_book_read(largest) if largest else None,
    )


@app.get("/authors", response_model=list[AuthorRead], tags=["authors"])
def list_authors(db: Session = Depends(get_db)) -> list[AuthorRead]:
    return [AuthorRead.model_validate(a) for a in BookRepository(db).list_authors()]


@app.post("/authors", response_model=AuthorRead, status_code=201, tags=["authors"])
def create_author(payload: AuthorCreate, db: Session = Depends(get_db)) -> AuthorRead:
    repository = BookRepository(db)
    author = repository.get_or_create_author(payload.name)
    db.commit()
    db.refresh(author)
    return AuthorRead.model_validate(author)


@app.get("/authors/{author_id}/books", response_model=list[BookRead], tags=["authors"])
def books_by_author(author_id: int, db: Session = Depends(get_db)) -> list[BookRead]:
    books = BookService(BookRepository(db)).books_by_author(author_id)
    if books is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return books
