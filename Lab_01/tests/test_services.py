from book_manager.models import Book
from book_manager.services import (
    add_book,
    calculate_average_pages,
    filter_by_year,
    find_by_author,
    find_largest_book,
    sort_books_by_pages,
)


def create_test_books() -> list[Book]:
    return [
        Book(
            title="Book One",
            author="Author One",
            year=2000,
            pages=200,
        ),
        Book(
            title="Book Two",
            author="Author Two",
            year=2010,
            pages=350,
        ),
        Book(
            title="Book Three",
            author="Author One",
            year=2000,
            pages=150,
        ),
    ]


def test_add_book() -> None:
    books: list[Book] = []

    book = add_book(
        books,
        "New Book",
        "New Author",
        2024,
        300,
    )

    assert len(books) == 1
    assert book.title == "New Book"
    assert book.author == "New Author"
    assert book.year == 2024
    assert book.pages == 300


def test_find_by_author() -> None:
    books = create_test_books()

    result = find_by_author(
        books,
        "Author One",
    )

    assert len(result) == 2
    assert all(
        book.author == "Author One"
        for book in result
    )


def test_filter_by_year() -> None:
    books = create_test_books()

    result = filter_by_year(
        books,
        2000,
    )

    assert len(result) == 2
    assert all(
        book.year == 2000
        for book in result
    )


def test_find_largest_book() -> None:
    books = create_test_books()

    result = find_largest_book(books)

    assert result is not None
    assert result.title == "Book Two"
    assert result.pages == 350


def test_calculate_average_pages() -> None:
    books = create_test_books()

    result = calculate_average_pages(books)

    assert result == 700 / 3


def test_sort_books_by_pages() -> None:
    books = create_test_books()

    result = sort_books_by_pages(books)

    assert result[0].pages == 350
    assert result[1].pages == 200
    assert result[2].pages == 150