from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from library_app.exceptions import InvalidBookDataError
from library_app.value_objects import PublicationInfo


class Publication(ABC):

    @property
    @abstractmethod
    def id(self) -> int:
        ...


@dataclass(slots=True)
class Author:
    id: int
    first_name: str
    last_name: str

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return self.full_name


class PrintedPublication(Publication):

    def __init__(self, publication_id: int) -> None:
        self._id = publication_id

    @property
    def id(self) -> int:
        return self._id


class Book(PrintedPublication):

    def __init__(
        self,
        book_id: int,
        title: str,
        author: Author,
        pages: int,
        publication_info: PublicationInfo,
    ) -> None:
        super().__init__(book_id)

        if not title.strip():
            raise InvalidBookDataError(
                "Book title cannot be empty"
            )

        if pages <= 0:
            raise InvalidBookDataError(
                "Number of pages must be positive"
            )

        self.title = title
        self.author = author
        self._pages = pages
        self.publication_info = publication_info

    @property
    def pages(self) -> int:
        return self._pages

    @pages.setter
    def pages(self, value: int) -> None:
        if value <= 0:
            raise InvalidBookDataError(
                "Number of pages must be positive"
            )

        self._pages = value

    def __repr__(self) -> str:
        return (
            f"Book("
            f"id={self.id!r}, "
            f"title={self.title!r}, "
            f"pages={self.pages!r})"
        )

    def __str__(self) -> str:
        return (
            f"{self.title} — "
            f"{self.author.full_name} "
            f"({self.publication_info.year})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Book):
            return NotImplemented

        return self.id == other.id

    def __len__(self) -> int:
        return self.pages


@dataclass
class BookCatalog:

    books: list[Book] = field(
        default_factory=list
    )

    def add(self, book: Book) -> None:
        self.books.append(book)

    def remove(self, book_id: int) -> bool:
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                return True

        return False

    def __len__(self) -> int:
        return len(self.books)

    def __iter__(self):
        return iter(self.books)

    def __contains__(self, book_id: int) -> bool:
        return any(
            book.id == book_id
            for book in self.books
        )

    def __getitem__(self, index: int) -> Book:
        return self.books[index]


@dataclass
class LibraryRegistry:

    catalog: BookCatalog = field(
        default_factory=BookCatalog
    )

    def register(self, book: Book) -> None:
        self.catalog.add(book)

    def unregister(self, book_id: int) -> bool:
        return self.catalog.remove(book_id)

    def find_by_id(self, book_id: int) -> Book | None:
        for book in self.catalog:
            if book.id == book_id:
                return book

        return None