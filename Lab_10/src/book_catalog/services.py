from typing import List, Optional
from book_catalog.models import Book
from book_catalog.repositories import BookRepository

class BookService:
    def __init__(self, repository: BookRepository) -> None:
        self.repository = repository

    def add_book(self, id_val: int, title: str, author: str, year: int, pages: int) -> Book:
        book = Book(id=id_val, title=title, author=author, year=year, pages=pages)
        self.repository.add(book)
        return book

    def filter_by_author(self, author: str) -> List[Book]:
        return [b for b in self.repository.get_all() if b.author.lower() == author.lower()]

    def filter_by_year(self, year: int) -> List[Book]:
        return [b for b in self.repository.get_all() if b.year == year]

    def get_largest_book(self) -> Optional[Book]:
        books = self.repository.get_all()
        if not books:
            return None
        return max(books, key=lambda b: b.pages)

    def get_average_pages(self) -> float:
        books = self.repository.get_all()
        if not books:
            return 0.0
        return sum(b.pages for b in books) / len(books)
