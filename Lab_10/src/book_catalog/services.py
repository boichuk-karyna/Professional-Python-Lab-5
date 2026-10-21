from sqlalchemy.orm import Session
from book_catalog.repositories import BookRepository
from book_catalog.schemas import AuthorResponse, BookCreate, BookResponse, CatalogStats


class BookService:
    def __init__(self, db: Session):
        self.repo = BookRepository(db)

    def list_books(self, author: str | None = None, year: int | None = None) -> list[BookResponse]:
        return [BookResponse.model_validate(b) for b in self.repo.get_all(author, year)]

    def create_book(self, book_data: BookCreate) -> BookResponse:
        book = self.repo.create(book_data)
        return BookResponse.model_validate(book)

    def get_authors(self) -> list[AuthorResponse]:
        return [AuthorResponse(**a) for a in self.repo.get_authors()]

    def get_books_by_author(self, author_identifier: str) -> list[BookResponse]:
        books = self.repo.get_books_by_author_identifier(author_identifier)
        return [BookResponse.model_validate(b) for b in books]

    def get_stats(self) -> CatalogStats:
        stats = self.repo.get_stats()
        if stats["largest_book"]:
            stats["largest_book"] = BookResponse.model_validate(stats["largest_book"])
        return CatalogStats(**stats)
