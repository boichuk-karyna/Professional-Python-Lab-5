from __future__ import annotations

import math
import random
from collections import Counter, defaultdict
from functools import lru_cache
from typing import Iterable, Sequence

import numpy as np

from .analytics_models import Book


def generate_books(count: int = 100_000, seed: int = 42) -> list[Book]:
    """Create a reproducible large catalog for performance experiments."""
    if count < 0:
        raise ValueError("count cannot be negative")
    rng = random.Random(seed)
    authors = [f"Author {i:04d}" for i in range(500)]
    return [
        Book(f"Book {i:07d}", authors[rng.randrange(len(authors))],
             rng.randint(1950, 2025), rng.randint(80, 1200))
        for i in range(count)
    ]


def pages_python(books: Sequence[Book]) -> dict[str, float | int]:
    pages = [book.pages for book in books]
    if not pages:
        return {"count": 0, "average": 0.0, "minimum": 0, "maximum": 0, "std": 0.0}
    average = sum(pages) / len(pages)
    variance = sum((page - average) ** 2 for page in pages) / len(pages)
    return {"count": len(pages), "average": average, "minimum": min(pages),
            "maximum": max(pages), "std": math.sqrt(variance)}


def pages_numpy(books: Sequence[Book]) -> dict[str, float | int]:
    values = np.fromiter((book.pages for book in books), dtype=np.int64, count=len(books))
    if not values.size:
        return {"count": 0, "average": 0.0, "minimum": 0, "maximum": 0, "std": 0.0}
    return {"count": int(values.size), "average": float(values.mean()),
            "minimum": int(values.min()), "maximum": int(values.max()), "std": float(values.std())}


def author_counts(books: Sequence[Book]) -> dict[str, int]:
    return dict(Counter(book.author for book in books))


def books_by_year(books: Sequence[Book]) -> dict[int, int]:
    grouped: dict[int, int] = defaultdict(int)
    for book in books:
        grouped[book.year] += 1
    return dict(sorted(grouped.items()))


def cpu_score(value: int) -> float:
    """Deterministic CPU-bound workload for comparing threads and processes."""
    current = float(value)
    for _ in range(80):
        current = math.sin(current) ** 2 + math.cos(current) ** 2 + math.sqrt(abs(current) + 1)
    return current


@lru_cache(maxsize=512)
def cached_author_summary(author: str, catalog_version: int, snapshot: tuple[tuple[str, str, int, int], ...]) -> tuple[int, float, int]:
    matching = [row for row in snapshot if row[1].casefold() == author.casefold()]
    return (len(matching), sum(row[3] for row in matching) / len(matching) if matching else 0.0,
            max((row[3] for row in matching), default=0))


def cache_summary(books: Sequence[Book], author: str, version: int = 0) -> tuple[int, float, int]:
    snapshot = tuple((b.title, b.author, b.year, b.pages) for b in books)
    return cached_author_summary(author, version, snapshot)


def invalidate_author_cache() -> None:
    cached_author_summary.cache_clear()
