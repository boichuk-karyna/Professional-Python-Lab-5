"""Application-level book catalog operations."""

from book_catalog.models import Book
from book_catalog.repositories import BookRepository
from book_catalog.schemas import BookCreate, BookUpdate, CatalogStatistics


class BookService:
    """Provide business operations independent of HTTP handling."""

    def __init__(self, repository: BookRepository) -> None:
        self.repository = repository

    def create_book(self, data: BookCreate) -> Book:
        """Add a book after normalizing its text fields."""
        normalized = data.model_copy(
            update={"title": data.title.strip(), "author": data.author.strip()}
        )
        if not normalized.title or not normalized.author:
            raise ValueError("Назва та автор не можуть бути порожніми.")
        return self.repository.add(normalized)

    def statistics(self) -> CatalogStatistics:
        """Return calculated catalog statistics."""
        total, average, largest = self.repository.statistics()
        return CatalogStatistics(
            total_books=total,
            average_pages=round(average, 2),
            largest_book=largest,
        )

    def update_book(self, book: Book, data: BookUpdate) -> Book:
        """Validate and update a book."""
        updates = data.model_dump(exclude_unset=True)
        for field in ("title", "author"):
            if field in updates and updates[field] is not None:
                updates[field] = updates[field].strip()
                if not updates[field]:
                    raise ValueError(f"Поле {field} не може бути порожнім.")
        return self.repository.update(book, BookUpdate(**updates))
