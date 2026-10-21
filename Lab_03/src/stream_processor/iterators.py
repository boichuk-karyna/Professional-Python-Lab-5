from collections.abc import Iterator

from stream_processor.models import BookRecord


class BookPageIterator:
    def __init__(
        self,
        books: list[BookRecord],
    ) -> None:
        self.books = books
        self.index = 0

    def __iter__(self) -> Iterator[BookRecord]:
        return self

    def __next__(self) -> BookRecord:
        if self.index >= len(self.books):
            raise StopIteration

        book = self.books[self.index]
        self.index += 1
        return book
