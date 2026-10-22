from collections.abc import Iterable, Iterator
from itertools import islice

from stream_processor.models import BookRecord


def batched_books(
    books: Iterable[BookRecord],
    batch_size: int,
) -> Iterator[list[BookRecord]]:
    if batch_size <= 0:
        raise ValueError("batch_size must be positive")

    iterator = iter(books)

    while True:
        batch = list(islice(iterator, batch_size))

        if not batch:
            return

        yield batch
