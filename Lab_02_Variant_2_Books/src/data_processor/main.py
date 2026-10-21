from data_processor.analytics import (
    average_pages,
    average_values,
    create_record,
    largest_book,
    page_statistics,
    sort_by_year,
)
from data_processor.benchmark import benchmark_search
from data_processor.data import BOOK_FIELDS, BOOKS
from data_processor.processors import (
    count_books_by_author,
    create_book_index,
    filter_by_year,
    find_book,
    get_unique_authors,
    group_books_by_author,
    operation_history,
    titles_list,
)


def print_books(title: str, books: list[dict]) -> None:
    print(f"\n{title}")
    print("-" * 85)
    for book in books:
        print(
            f'{book["id"]:2} | {book["title"][:28]:28} | '
            f'{book["author"][:20]:20} | {book["year"]} | {book["pages"]:4}'
        )


def main() -> None:
    print("Book fields (tuple):", BOOK_FIELDS)
    print_books("All books", BOOKS)

    authors = get_unique_authors(BOOKS)
    print("\nUnique authors (set):", authors)

    print("\nTitles (list comprehension):", titles_list(BOOKS))

    grouped = group_books_by_author(BOOKS)
    print("\nGrouped by author (defaultdict -> dict):")
    for author, books in grouped.items():
        print(author, "->", len(books))

    print("\nCounter by author:", count_books_by_author(BOOKS))

    index = create_book_index(BOOKS)
    print("\nSearch by dict index, id=4:", index.get(4))
    print("Search by title:", find_book(BOOKS, "Clean Code"))

    recent = filter_by_year(BOOKS, 2020)
    print_books("Books from 2020", recent)

    biggest = largest_book(BOOKS)
    print("\nLargest book:", biggest)

    avg = average_pages(BOOKS)
    print(f"Average pages: {avg:.2f}")

    print_books("Sorted by year", sort_by_year(BOOKS))

    stats = page_statistics(BOOKS)
    print("\nPage statistics tuple (min, max, avg):", stats)

    print("Average via *args:", average_values(100, 200, 300, 400))

    new_book = create_record(
        id=7,
        title="Architecture Patterns with Python",
        author="Harry Percival",
        year=2020,
        pages=304,
    )
    print("Created via **kwargs:", new_book)

    history = operation_history()
    history.extend(["load", "group", "search", "filter", "sort", "report"])
    print("Recent operations (deque):", list(history))

    print("\nBenchmark:")
    for row in benchmark_search():
        print(row)


if __name__ == "__main__":
    main()
