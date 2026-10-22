from typing import List
from book_catalog.models import Book

class BookRepository:
    def __init__(self) -> None:
        self._books: List[Book] = []

    def add(self, book: Book) -> None:
        self._books.append(book)

    def get_all(self) -> List[Book]:
        return self._books
