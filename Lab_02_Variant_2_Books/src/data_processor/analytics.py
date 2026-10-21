from data_processor.decorators import measure_time


@measure_time
def average_pages(books: list[dict]) -> float:
    if not books:
        return 0.0
    return sum(book["pages"] for book in books) / len(books)


def largest_book(books: list[dict]) -> dict | None:
    if not books:
        return None
    return max(books, key=lambda book: book["pages"])


def sort_by_year(books: list[dict], reverse: bool = False) -> list[dict]:
    return sorted(
        books,
        key=lambda book: (book["year"], book["title"]),
        reverse=reverse,
    )


def average_values(*values: float) -> float:
    """Demonstrates *args."""
    return sum(values) / len(values) if values else 0.0


def create_record(**fields) -> dict:
    """Demonstrates **kwargs."""
    return dict(fields)


def page_statistics(books: list[dict]) -> tuple[int, int, float]:
    """Tuple with min pages, max pages and average pages."""
    if not books:
        return (0, 0, 0.0)
    pages = [book["pages"] for book in books]
    return (min(pages), max(pages), sum(pages) / len(pages))
