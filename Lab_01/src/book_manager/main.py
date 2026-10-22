from book_manager.models import Book
from book_manager.services import (
    add_book,
    calculate_average_pages,
    filter_by_year,
    find_by_author,
    find_largest_book,
    sort_books_by_pages,
)


def create_demo_books() -> list[Book]:
    books: list[Book] = []

    add_book(
        books,
        "Kobzar",
        "Taras Shevchenko",
        1840,
        256,
    )

    add_book(
        books,
        "Harry Potter",
        "J. K. Rowling",
        1997,
        320,
    )

    add_book(
        books,
        "The Hobbit",
        "J. R. R. Tolkien",
        1937,
        310,
    )

    add_book(
        books,
        "1984",
        "George Orwell",
        1949,
        328,
    )

    return books


def print_books(books: list[Book]) -> None:
    if not books:
        print("\nBooks not found.")
        return

    print("\nBooks:")

    for book in books:
        print(
            f"{book.title:20}"
            f"{book.author:25}"
            f"{book.year:8}"
            f"{book.pages:6}"
        )


def input_year() -> int:
    while True:
        try:
            year = int(input("Enter publication year: "))

            if year < 0:
                print("Year cannot be negative.")
                continue

            return year

        except ValueError:
            print("Please enter a number.")


def input_pages() -> int:
    while True:
        try:
            pages = int(input("Enter number of pages: "))

            if pages <= 0:
                print("Number of pages must be positive.")
                continue

            return pages

        except ValueError:
            print("Please enter a number.")


def add_book_from_input(
    books: list[Book],
) -> None:
    title = input("Enter book title: ").strip()
    author = input("Enter author: ").strip()
    year = input_year()
    pages = input_pages()

    if not title or not author:
        print("Title and author cannot be empty.")
        return

    add_book(
        books,
        title,
        author,
        year,
        pages,
    )

    print("Book added successfully.")


def print_menu() -> None:
    print("\n" + "=" * 45)
    print("BOOK MANAGER")
    print("=" * 45)
    print("1. Show all books")
    print("2. Add book")
    print("3. Find books by author")
    print("4. Filter books by year")
    print("5. Find the largest book")
    print("6. Calculate average number of pages")
    print("7. Sort books by pages")
    print("8. Exit")
    print("=" * 45)


def run_menu(books: list[Book]) -> None:
    while True:
        print_menu()

        command = input("Select command: ").strip()

        if command == "1":
            print_books(books)

        elif command == "2":
            add_book_from_input(books)

        elif command == "3":
            author = input("Enter author: ").strip()

            result = find_by_author(
                books,
                author,
            )

            print_books(result)

        elif command == "4":
            year = input_year()

            result = filter_by_year(
                books,
                year,
            )

            print_books(result)

        elif command == "5":
            largest = find_largest_book(books)

            if largest is not None:
                print("\nLargest book:")
                print(
                    f"Title: {largest.title}"
                )
                print(
                    f"Author: {largest.author}"
                )
                print(
                    f"Year: {largest.year}"
                )
                print(
                    f"Pages: {largest.pages}"
                )
            else:
                print("\nNo books available.")

        elif command == "6":
            average = calculate_average_pages(books)

            print(
                f"\nAverage number of pages: "
                f"{average:.2f}"
            )

        elif command == "7":
            sorted_books = sort_books_by_pages(books)

            print("\nBooks sorted by number of pages:")
            print_books(sorted_books)

        elif command == "8":
            print("\nGoodbye!")
            break

        else:
            print("\nUnknown command.")


def main() -> None:
    books = create_demo_books()

    print("Welcome to Book Manager!")
    run_menu(books)


if __name__ == "__main__":
    main()