from __future__ import annotations

import argparse

from .analytics import generate_books, pages_numpy, pages_python, books_by_year, author_counts
from .repositories import BookCatalog


def main() -> None:
    parser = argparse.ArgumentParser(description="Book catalog — Lab 9, variant 2")
    parser.add_argument("--count", type=int, default=100_000, help="number of generated books")
    args = parser.parse_args()
    books = generate_books(args.count)
    catalog = BookCatalog(books)
    print(f"Catalog created: {len(books):,} books")
    print("Largest book:", catalog.largest_book())
    print(f"Average pages: {catalog.average_pages():.2f}")
    print("Python page statistics:", pages_python(books))
    print("NumPy page statistics:", pages_numpy(books))
    print("Distinct authors:", len(author_counts(books)))
    print("Publication years represented:", len(books_by_year(books)))
    print("Example author statistics:", catalog.author_statistics(books[0].author))


if __name__ == "__main__":
    main()
