from typing import List, Optional
from book_catalog.models import Book, Author

class BookRepository:
    def __init__(self) -> None:
        self._books: List[Book] = [
            Book(id=1, title="The Pragmatic Programmer", author_id=1, year=1999, genre="Technology", price=45.0),
            Book(id=2, title="Clean Code", author_id=2, year=2008, genre="Technology", price=40.0),
        ]

    def get_all(self) -> List[Book]:
        return self._books

    def get_by_id(self, book_id: int) -> Optional[Book]:
        return next((b for b in self._books if b.id == book_id), None)

    def get_by_author_id(self, author_id: int) -> List[Book]:
        return [b for b in self._books if b.author_id == author_id]

class AuthorRepository:
    def __init__(self) -> None:
        self._authors: List[Author] = [
            Author(id=1, name="Andrew Hunt", country="USA"),
            Author(id=2, name="Robert C. Martin", country="USA"),
        ]

    def get_all(self) -> List[Author]:
        return self._authors

    def get_by_id(self, author_id: int) -> Optional[Author]:
        return next((a for a in self._authors if a.id == author_id), None)
