from collections.abc import Iterator
from itertools import chain
from pathlib import Path

from stream_processor.filters import (
    filter_after_year,
    filter_by_author,
    search_books,
    validate_books,
)
from stream_processor.models import BookRecord
from stream_processor.parsers import parse_csv_rows
from stream_processor.readers import read_lines
from stream_processor.transformations import normalize_books


def build_pipeline(
    path: Path,
) -> Iterator[BookRecord]:
    lines = read_lines(path)
    rows = parse_csv_rows(lines)
    valid = validate_books(rows)
    normalized = normalize_books(valid)
    return normalized


def build_author_pipeline(
    path: Path,
    author: str,
) -> Iterator[BookRecord]:
    return filter_by_author(
        build_pipeline(path),
        author,
    )


def build_year_pipeline(
    path: Path,
    year: int,
) -> Iterator[BookRecord]:
    return filter_after_year(
        build_pipeline(path),
        year,
    )


def build_search_pipeline(
    path: Path,
    query: str,
) -> Iterator[BookRecord]:
    return search_books(
        build_pipeline(path),
        query,
    )


def combine_pipelines(
    first: Iterator[BookRecord],
    second: Iterator[BookRecord],
) -> Iterator[BookRecord]:
    return chain(first, second)
