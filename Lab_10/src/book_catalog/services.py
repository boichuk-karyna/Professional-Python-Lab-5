from typing import List, Optional
from book_catalog.models import Book, Author
from book_catalog.repositories import BookRepository, AuthorRepository

class CatalogService:
    def __init__(self, book_repo: Optional[BookRepository] = None, author_repo: Optional[AuthorRepository] = None) -> None:
        self.book_repo = book_repo or BookRepository()
        self.author_repo = author_repo or AuthorRepository()

    def list_books(self) -> List[Book]:
        return self.book_repo.get_all()

    def list_authors(self) -> List[Author]:
        return self.author_repo.get_all()

    def get_author_books(self, author_id: int) -> List[Book]:
        return self.book_repo.get_by_author_id(author_id)
