"""In-memory repository for book records."""
from .models import Book


class BookRepository:
    def __init__(self) -> None:
        self._books: list[Book] = []

    def add(self, book: Book) -> None:
        if not isinstance(book, Book):
            raise TypeError("Expected a Book instance.")
        self._books.append(book)

    def all(self) -> list[Book]:
        return list(self._books)
