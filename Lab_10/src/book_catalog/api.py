from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from book_catalog.database import get_db, init_db
from book_catalog.schemas import BookCreate, BookResponse, CatalogStats
from book_catalog.services import BookService


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Book Catalog API", version="1.0.0", lifespan=lifespan)


@app.get("/health", status_code=status.HTTP_200_OK)
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/books", response_model=list[BookResponse])
def get_books(
    author: str | None = None,
    year: int | None = None,
    db: Session = Depends(get_db)
):
    service = BookService(db)
    return service.list_books(author=author, year=year)


@app.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    service = BookService(db)
    return service.create_book(book)


@app.get("/authors")
def get_authors(db: Session = Depends(get_db)):
    service = BookService(db)
    return service.get_authors()


@app.get("/authors/{author_name}/books", response_model=list[BookResponse])
def get_books_by_author(author_name: str, db: Session = Depends(get_db)):
    service = BookService(db)
    books = service.list_books(author=author_name)
    if not books:
        raise HTTPException(status_code=404, detail="No books found for this author")
    return books


@app.get("/statistics", response_model=CatalogStats)
def get_statistics(db: Session = Depends(get_db)):
    service = BookService(db)
    return service.get_stats()
