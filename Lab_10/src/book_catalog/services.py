from book_catalog.repositories import BookRepository
from book_catalog.schemas import BookRead


def to_book_read(book) -> BookRead:
    return BookRead(
        id=book.id,
        title=book.title,
        author_id=book.author_id,
        author=book.author.name,
        year=book.year,
        pages=book.pages,
    )


class BookService:
    def __init__(self, repository: BookRepository):
        self.repository = repository

    def list_books(
        self,
        author: str | None = None,
        year: int | None = None,
    ) -> list[BookRead]:
        return [
            to_book_read(book)
            for book in self.repository.list_books(author=author, year=year)
        ]

    def add_book(self, title: str, author: str, year: int, pages: int) -> BookRead:
        book = self.repository.add_book(title, author, year, pages)
        return to_book_read(book)

    def books_by_author(self, author_id: int) -> list[BookRead] | None:
        if self.repository.get_author(author_id) is None:
            return None
        return [
            to_book_read(book)
            for book in self.repository.books_by_author(author_id)
        ]
