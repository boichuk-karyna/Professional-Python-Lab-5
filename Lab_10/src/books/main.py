"""Small command-line demonstration."""
from .database import SessionLocal, engine
from .models import Base
from .repositories import AuthorRepository, BookRepository


def main() -> None:
    Base.metadata.create_all(engine)
    with SessionLocal() as session:
        authors = AuthorRepository(session)
        books = BookRepository(session)
        author = authors.get_by_name("Тарас Шевченко")
        if author is None:
            author = authors.add("Тарас Шевченко")
        if not books.find_by_author(author.name):
            books.add(Book(title="Кобзар", year=1840, pages=240, author_id=author.id))
        print("Каталог книг:")
        for book in books.get_all():
            print(f"{book.id}. {book.title} — {book.author.name} ({book.year}), {book.pages} стор.")
        print(f"Середня кількість сторінок: {books.average_pages():.2f}")
        largest = books.largest_book()
        if largest:
            print(f"Найбільша книга: {largest.title} ({largest.pages} стор.)")


from .models import Book

if __name__ == "__main__":
    main()
