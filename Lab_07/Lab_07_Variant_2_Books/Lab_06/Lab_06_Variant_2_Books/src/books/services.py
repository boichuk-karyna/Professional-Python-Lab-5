"""Book catalog operations and async external-catalog integration."""
from typing import Protocol
from .config import get_year_range
from .models import Book
from .repositories import BookRepository


class ExternalBookCatalog(Protocol):
    async def fetch_books(self) -> list[dict[str, object]]:
        ...


class BookService:
    def __init__(self, repository: BookRepository, year_range: tuple[int, int] | None = None):
        self.repository = repository
        self.year_range = year_range if year_range is not None else get_year_range()
        low, high = self.year_range
        if low <= 0 or high < low:
            raise ValueError("Invalid year range.")

    def add_book(self, book: Book) -> Book:
        low, high = self.year_range
        if not low <= book.year <= high:
            raise ValueError(f"Book year must be between {low} and {high}.")
        self.repository.add(book)
        return book

    def all_books(self) -> list[Book]:
        return self.repository.all()

    def search_by_author(self, author: str) -> list[Book]:
        needle = author.strip().casefold()
        if not needle:
            return []
        return [b for b in self.all_books() if needle in b.author.casefold()]

    def search_by_title(self, title: str) -> list[Book]:
        needle = title.strip().casefold()
        if not needle:
            return []
        return [b for b in self.all_books() if needle in b.title.casefold()]

    def filter_by_year(self, year: int) -> list[Book]:
        if isinstance(year, bool) or not isinstance(year, int):
            raise ValueError("Year must be an integer.")
        return [b for b in self.all_books() if b.year == year]

    def largest_book(self) -> Book | None:
        books = self.all_books()
        return max(books, key=lambda b: b.pages, default=None)

    def average_pages(self) -> float:
        books = self.all_books()
        return sum(b.pages for b in books) / len(books) if books else 0.0

    async def import_external(self, external: ExternalBookCatalog) -> list[Book]:
        records = await external.fetch_books()
        imported = []
        for record in records:
            book = Book(
                title=str(record["title"]),
                author=str(record["author"]),
                year=int(record["year"]),
                pages=int(record["pages"]),
            )
            self.add_book(book)
            imported.append(book)
        return imported
