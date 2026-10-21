from collections import Counter, defaultdict, deque
from collections.abc import Callable


def get_unique_authors(books: list[dict]) -> set[str]:
    """Set comprehension: unique authors."""
    return {book["author"] for book in books}


def create_book_index(books: list[dict]) -> dict[int, dict]:
    """Dict comprehension: O(n) build, average O(1) lookup."""
    return {book["id"]: book for book in books}


def titles_list(books: list[dict]) -> list[str]:
    """List comprehension example."""
    return [book["title"] for book in books]


def group_books_by_author(books: list[dict]) -> dict[str, list[dict]]:
    grouped = defaultdict(list)
    for book in books:
        grouped[book["author"]].append(book)
    return dict(grouped)


def count_books_by_author(books: list[dict]) -> Counter:
    return Counter(book["author"] for book in books)


def find_book(books: list[dict], query: str | int) -> dict | None:
    """Search by ID or exact title."""
    if isinstance(query, int):
        return create_book_index(books).get(query)

    normalized = query.strip().casefold()
    return next(
        (book for book in books if book["title"].casefold() == normalized),
        None,
    )


def filter_books(books: list[dict], predicate: Callable[[dict], bool]) -> list[dict]:
    """Higher-order universal filter."""
    return [book for book in books if predicate(book)]


def create_year_filter(min_year: int) -> Callable[[dict], bool]:
    """Closure that remembers min_year."""
    def predicate(book: dict) -> bool:
        return int(book["year"]) >= min_year

    return predicate


def filter_by_year(books: list[dict], min_year: int) -> list[dict]:
    return filter_books(books, create_year_filter(min_year))


def operation_history(maxlen: int = 5) -> deque[str]:
    """Use deque from collections for recent operations."""
    return deque(maxlen=maxlen)
