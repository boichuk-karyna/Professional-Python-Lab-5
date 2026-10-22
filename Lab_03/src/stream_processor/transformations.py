from collections.abc import Iterable, Iterator

from stream_processor.models import BookRecord


def normalize_books(
    books: Iterable[BookRecord],
) -> Iterator[BookRecord]:
    for book in books:
        yield BookRecord(
            isbn=book.isbn.strip(),
            title=book.title.strip().title(),
            author=book.author.strip().title(),
            year=book.year,
            pages=book.pages,
        )
