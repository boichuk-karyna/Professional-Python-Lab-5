from collections.abc import Iterable, Iterator

from stream_processor.models import BookRecord


def validate_books(
    rows: Iterable[dict[str, str]],
) -> Iterator[BookRecord]:
    for row in rows:
        try:
            isbn = row["isbn"].strip()
            title = row["title"].strip()
            author = row["author"].strip()
            year = int(row["year"])
            pages = int(row["pages"])
        except (KeyError, TypeError, ValueError):
            continue

        if not isbn or not title or not author:
            continue

        if not (0 <= year <= 2100):
            continue

        if pages <= 0:
            continue

        yield BookRecord(
            isbn=isbn,
            title=title,
            author=author,
            year=year,
            pages=pages,
        )


def filter_by_author(
    books: Iterable[BookRecord],
    author: str,
) -> Iterator[BookRecord]:
    target = author.casefold()

    for book in books:
        if book.author.casefold() == target:
            yield book


def filter_after_year(
    books: Iterable[BookRecord],
    year: int,
) -> Iterator[BookRecord]:
    for book in books:
        if book.year > year:
            yield book


def search_books(
    books: Iterable[BookRecord],
    query: str,
) -> Iterator[BookRecord]:
    target = query.casefold()

    for book in books:
        if (
            target in book.author.casefold()
            or target in book.title.casefold()
            or target == book.isbn.casefold()
        ):
            yield book
