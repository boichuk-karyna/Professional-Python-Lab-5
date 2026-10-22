from typing import Generic, Protocol, TypeVar

class HasCode(Protocol):
    code: str

T = TypeVar("T", bound=HasCode)

class InMemoryRepository(Generic[T]):
    def __init__(self) -> None:
        self._items: dict[str, T] = {}

    def add(self, item: T) -> None:
        self._items[item.code] = item

    def get(self, code: str) -> T | None:
        return self._items.get(code)

    def all(self) -> list[T]:
        return list(self._items.values())

    def remove(self, code: str) -> bool:
        return self._items.pop(code, None) is not None