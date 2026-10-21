"""Optimized catalog analytics carried forward from Lab 9."""

from __future__ import annotations

from functools import lru_cache
from typing import Sequence

import numpy as np

from book_manager.models import Book


def page_statistics_python(books: Sequence[Book]) -> dict[str, float | int]:
    """Calculate page statistics using standard Python."""
    values = [book.pages for book in books]
    if not values:
        return {"count": 0, "average": 0.0, "minimum": 0, "maximum": 0, "std": 0.0}
    average = sum(values) / len(values)
    variance = sum((value - average) ** 2 for value in values) / len(values)
    return {
        "count": len(values),
        "average": average,
        "minimum": min(values),
        "maximum": max(values),
        "std": variance**0.5,
    }


def page_statistics_numpy(books: Sequence[Book]) -> dict[str, float | int]:
    """Calculate the same statistics using NumPy vectorized operations."""
    values = np.fromiter((book.pages for book in books), dtype=np.int64, count=len(books))
    if values.size == 0:
        return {"count": 0, "average": 0.0, "minimum": 0, "maximum": 0, "std": 0.0}
    return {
        "count": int(values.size),
        "average": float(values.mean()),
        "minimum": int(values.min()),
        "maximum": int(values.max()),
        "std": float(values.std()),
    }


@lru_cache(maxsize=512)
def _cached_author_summary(
    author_name: str,
    snapshot: tuple[tuple[str, str, int, int], ...],
) -> tuple[int, float, int]:
    """Cache summary by immutable catalog snapshot to avoid stale results."""
    matching = [item for item in snapshot if item[1].casefold() == author_name.casefold()]
    count = len(matching)
    average = sum(item[3] for item in matching) / count if count else 0.0
    largest = max((item[3] for item in matching), default=0)
    return count, average, largest


def cached_author_summary(
    books: Sequence[Book], author_name: str
) -> tuple[int, float, int]:
    """Return count, average pages, and maximum pages for an author."""
    snapshot = tuple((book.title, book.author.name, book.year, book.pages) for book in books)
    return _cached_author_summary(author_name, snapshot)


def clear_analytics_cache() -> None:
    """Clear cached summaries when needed by a caller."""
    _cached_author_summary.cache_clear()
