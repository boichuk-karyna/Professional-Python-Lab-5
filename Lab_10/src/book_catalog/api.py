import logging
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from book_catalog.config import get_settings
from book_catalog.database import Base, engine, get_session
from book_catalog.models import Author, Book
from book_catalog.repositories import BookRepository
from book_catalog.schemas import AuthorCreate, AuthorRead, BookCreate, BookRead, BookStatistics

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


app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)


def repository(session: Annotated[Session, Depends(get_session)]) -> BookRepository:
    return BookRepository(session)


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok", "environment": settings.environment}


@app.get("/books", response_model=list[BookRead], tags=["books"])
def list_books(
    repo: Annotated[BookRepository, Depends(repository)],
    author: str | None = None,
    year: Annotated[int | None, Query(ge=1450, le=2100)] = None,
    q: str | None = None,
) -> list[Book]:
    return repo.list_books(author=author, year=year, query=q)


@app.post("/books", response_model=BookRead, status_code=status.HTTP_201_CREATED, tags=["books"])
def create_book(
    payload: BookCreate,
    repo: Annotated[BookRepository, Depends(repository)],
) -> Book:
    try:
        return repo.create_book(
            title=payload.title,
            author_name=payload.author,
            year=payload.year,
            pages=payload.pages,
            description=payload.description,
        )
    except Exception:
        logger.exception("Could not create book")
        raise HTTPException(status_code=500, detail="Could not create book") from None


@app.get("/books/statistics", response_model=BookStatistics, tags=["books"])
def book_statistics(repo: Annotated[BookRepository, Depends(repository)]) -> dict[str, object]:
    count, average, largest = repo.statistics()
    return {"count": count, "average_pages": average, "largest_book": largest}


@app.get("/books/{book_id}", response_model=BookRead, tags=["books"])
def get_book(book_id: int, repo: Annotated[BookRepository, Depends(repository)]) -> Book:
    book = repo.get_book(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["books"])
def delete_book(book_id: int, repo: Annotated[BookRepository, Depends(repository)]) -> Response:
    if not repo.delete_book(book_id):
        raise HTTPException(status_code=404, detail="Book not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/authors", response_model=list[AuthorRead], tags=["authors"])
def list_authors(repo: Annotated[BookRepository, Depends(repository)]) -> list[Author]:
    return repo.list_authors()


@app.post("/authors", response_model=AuthorRead, status_code=status.HTTP_201_CREATED, tags=["authors"])
def create_author(
    payload: AuthorCreate,
    session: Annotated[Session, Depends(get_session)],
) -> Author:
    from sqlalchemy import select

    existing = session.scalars(select(Author).where(Author.name.ilike(payload.name))).first()
    if existing:
        raise HTTPException(status_code=409, detail="Author already exists")
    author = Author(name=payload.name)
    session.add(author)
    session.commit()
    session.refresh(author)
    return author


@app.get("/authors/{author_id}/books", response_model=list[BookRead], tags=["authors"])
def author_books(
    author_id: int,
    repo: Annotated[BookRepository, Depends(repository)],
) -> list[Book]:
    if repo.get_author(author_id) is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return repo.books_by_author(author_id)
