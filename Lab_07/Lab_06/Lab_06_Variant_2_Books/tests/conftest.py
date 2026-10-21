import pytest
from books.models import Book
from books.repositories import BookRepository
from books.services import BookService


@pytest.fixture
def book() -> Book:
    return Book("The Hobbit", "J. R. R. Tolkien", 1937, 310)


@pytest.fixture
def books() -> list[Book]:
    return [
        Book("The Hobbit", "J. R. R. Tolkien", 1937, 310),
        Book("The Lord of the Rings", "J. R. R. Tolkien", 1954, 1178),
        Book("Pride and Prejudice", "Jane Austen", 1813, 432),
    ]


@pytest.fixture
def repository() -> BookRepository:
    return BookRepository()


@pytest.fixture
def service(repository: BookRepository) -> BookService:
    return BookService(repository, year_range=(1, 2100))
