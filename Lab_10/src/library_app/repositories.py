from typing import Generic, Protocol, TypeVar

from library_app.models import Book


class HasId(Protocol):

    @property
    def id(self) -> int:
        ...


T = TypeVar(
    "T",
    bound=HasId,
)


class Repository(Generic[T]):

    def __init__(self) -> None:
        self._items: dict[int, T] = {}

    def add(
        self,
        item: T,
    ) -> None:
        self._items[item.id] = item

    def get(
        self,
        item_id: int,
    ) -> T | None:
        return self._items.get(item_id)

    def remove(
        self,
        item_id: int,
    ) -> bool:
        return (
            self._items.pop(
                item_id,
                None,
            )
            is not None
        )

    def all(self) -> list[T]:
        return list(
            self._items.values()
        )

    def count(self) -> int:
        return len(self._items)


class BookRepository(Repository[Book]):

    def find_by_author(
        self,
        author_name: str,
    ) -> list[Book]:

        name = author_name.lower()

        return [
            book
            for book in self.all()
            if name
            in book.author.full_name.lower()
        ]