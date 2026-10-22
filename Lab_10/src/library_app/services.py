from abc import ABC, abstractmethod
from collections.abc import Sequence

from library_app.models import Book
from library_app.protocols import Exporter, Notifier
from library_app.repositories import BookRepository


class SearchStrategy(ABC):

    @abstractmethod
    def matches(
        self,
        book: Book,
        query: str,
    ) -> bool:
        ...


class TitleSearchStrategy(SearchStrategy):

    def matches(
        self,
        book: Book,
        query: str,
    ) -> bool:

        return (
            query.lower()
            in book.title.lower()
        )


class AuthorSearchStrategy(SearchStrategy):

    def matches(
        self,
        book: Book,
        query: str,
    ) -> bool:

        return (
            query.lower()
            in book.author.full_name.lower()
        )


class BookSearchService:

    def __init__(
        self,
        repository: BookRepository,
        strategy: SearchStrategy,
    ) -> None:

        self._repository = repository
        self._strategy = strategy

    def search(
        self,
        query: str,
    ) -> list[Book]:

        return [
            book
            for book in self._repository.all()
            if self._strategy.matches(
                book,
                query,
            )
        ]


class BookReportingService:

    def __init__(
        self,
        repository: BookRepository,
        exporter: Exporter,
        notifier: Notifier,
    ) -> None:

        self._repository = repository
        self._exporter = exporter
        self._notifier = notifier

    def filter_by_year(
        self,
        year_from: int,
        year_to: int,
    ) -> list[Book]:

        return [
            book
            for book in self._repository.all()
            if year_from
            <= book.publication_info.year
            <= year_to
        ]

    def largest_book(self) -> Book | None:

        books = self._repository.all()

        if not books:
            return None

        return max(
            books,
            key=lambda book: book.pages,
        )

    def average_pages(self) -> float:

        books = self._repository.all()

        if not books:
            return 0.0

        return (
            sum(
                book.pages
                for book in books
            )
            / len(books)
        )

    def export_report(self) -> str:

        books = self._repository.all()

        result = self._exporter.export(
            books
        )

        self._notifier.send(
            "Book report was successfully created."
        )

        return result


def calculate_average_pages(
    books: Sequence[Book],
) -> float:

    if not books:
        return 0.0

    return (
        sum(
            book.pages
            for book in books
        )
        / len(books)
    )