from book_manager.models import Book

def add_book(
    books: list[Book],
    title: str,
    author: str,
    year: int,
    pages: int,
) -> Book:
    book = Book(
        title=title,
        author=author,
        year=year,
        pages=pages,
    )
    books.append(book)
    return book

def find_by_author(
    books: list[Book],
    author: str,
) -> list[Book]:
    return [
        book
        for book in books
        if book.author.lower() == author.lower()
    ]

def filter_by_year(
    books: list[Book],
    year: int,
) -> list[Book]:
    return [
        book
        for book in books
        if book.year == year
    ]


def find_largest_book(
    books: list[Book],
) -> Book | None:
    if not books:
        return None

    return max(
        books,
        key=lambda book: book.pages,
    )


def calculate_average_pages(
    books: list[Book],
) -> float:
    if not books:
        return 0.0

    total_pages = sum(
        book.pages
        for book in books
    )

    return total_pages / len(books)


def sort_books_by_pages(
    books: list[Book],
) -> list[Book]:
    return sorted(
        books,
        key=lambda book: book.pages,
        reverse=True,
    )