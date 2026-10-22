from collections.abc import Iterable
from collections import Counter

from stream_processor.models import BookRecord


def streaming_average_pages(
    books: Iterable[BookRecord],
) -> float:
    total = 0
    count = 0

    for book in books:
        total += book.pages
        count += 1

    return total / count if count else 0.0


def find_largest_book(
    books: Iterable[BookRecord],
) -> BookRecord | None:
    largest = None

    for book in books:
        if largest is None or book.pages > largest.pages:
            largest = book

    return largest


def count_by_author(
    books: Iterable[BookRecord],
) -> dict[str, int]:
    counts = Counter()

    for book in books:
        counts[book.author] += 1

    return dict(counts)


def process_batch(batch: list[BookRecord]) -> int:
    return sum(book.pages for book in batch)
