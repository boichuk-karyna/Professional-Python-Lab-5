from library_app.dto import (
    BookPayload,
    book_from_payload,
)
from library_app.models import (
    Author,
    Book,
    BookCatalog,
)
from library_app.protocols import (
    ConsoleExporter,
    ConsoleNotifier,
)
from library_app.repositories import BookRepository
from library_app.services import (
    AuthorSearchStrategy,
    BookReportingService,
    BookSearchService,
    TitleSearchStrategy,
)
from library_app.value_objects import PublicationInfo


def main() -> None:

    author1 = Author(
        id=1,
        first_name="George",
        last_name="Orwell",
    )

    author2 = Author(
        id=2,
        first_name="J. K.",
        last_name="Rowling",
    )

    book1 = Book(
        book_id=1,
        title="1984",
        author=author1,
        pages=328,
        publication_info=PublicationInfo(
            year=1949,
            publisher="Secker & Warburg",
        ),
    )

    book2 = Book(
        book_id=2,
        title="Animal Farm",
        author=author1,
        pages=112,
        publication_info=PublicationInfo(
            year=1945,
            publisher="Secker & Warburg",
        ),
    )

    book3 = Book(
        book_id=3,
        title="Harry Potter and the Philosopher's Stone",
        author=author2,
        pages=320,
        publication_info=PublicationInfo(
            year=1997,
            publisher="Bloomsbury",
        ),
    )

    catalog = BookCatalog()

    catalog.add(book1)
    catalog.add(book2)
    catalog.add(book3)

    print("=== CUSTOM COLLECTION ===")

    print(
        f"Catalog size: {len(catalog)}"
    )

    print(
        f"Book ID 1 exists: "
        f"{1 in catalog}"
    )

    print(
        f"First book: {catalog[0]}"
    )

    print("\nAll books:")

    for book in catalog:
        print(f"- {book}")

    repository = BookRepository()

    for book in catalog:
        repository.add(book)

    print("\n=== LIBRARY ===")

    print(
        f"Number of books: "
        f"{repository.count()}"
    )

    print("\n=== BOOK INFORMATION ===")

    print(book1)
    print(repr(book1))

    print(
        f"Number of pages: "
        f"{len(book1)}"
    )

    print("\n=== PROPERTY ===")

    print(
        f"Current pages: "
        f"{book1.pages}"
    )

    book1.pages = 330

    print(
        f"Updated pages: "
        f"{book1.pages}"
    )

    print("\n=== SEARCH BY TITLE ===")

    title_search = BookSearchService(
        repository=repository,
        strategy=TitleSearchStrategy(),
    )

    title_results = title_search.search(
        "Harry"
    )

    for book in title_results:
        print(book)

    print("\n=== SEARCH BY AUTHOR ===")

    author_search = BookSearchService(
        repository=repository,
        strategy=AuthorSearchStrategy(),
    )

    author_results = author_search.search(
        "Orwell"
    )

    for book in author_results:
        print(book)

    print("\n=== YEAR FILTER ===")

    reporting_service = BookReportingService(
        repository=repository,
        exporter=ConsoleExporter(),
        notifier=ConsoleNotifier(),
    )

    books_1940_1950 = (
        reporting_service.filter_by_year(
            1940,
            1950,
        )
    )

    for book in books_1940_1950:
        print(book)

    print("\n=== LARGEST BOOK ===")

    largest = reporting_service.largest_book()

    if largest is not None:
        print(largest)
        print(
            f"Pages: {largest.pages}"
        )

    print("\n=== AVERAGE PAGES ===")

    average = reporting_service.average_pages()

    print(
        f"Average pages: {average:.2f}"
    )

    print("\n=== EXPORT ===")

    report = reporting_service.export_report()

    print(report)

    print("\n=== TYPEDDICT ===")

    payload: BookPayload = {
        "id": 4,
        "title": "Animal Farm",
        "author_first_name": "George",
        "author_last_name": "Orwell",
        "pages": 120,
        "year": 1945,
        "publisher": "Secker & Warburg",
    }

    payload_book = book_from_payload(
        payload
    )

    print(payload_book)


if __name__ == "__main__":
    main()