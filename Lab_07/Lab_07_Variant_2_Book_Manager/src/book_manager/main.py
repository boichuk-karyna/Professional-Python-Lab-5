from .database import SessionLocal, engine
from .models import Base, Author, Book
from .repositories import AuthorRepository, BookRepository
from .services import add_author_with_books

def main() -> None:
    Base.metadata.create_all(engine)
    with SessionLocal() as session:
        authors = AuthorRepository(session)
        author = authors.get_by_name("Lesya Ukrainka")
        if author is None:
            author = add_author_with_books(session, "Lesya Ukrainka", [
                {"title": "Лісова пісня", "year": 1911, "pages": 96, "isbn": "978-1-00000-000-1"},
                {"title": "Одержима", "year": 1901, "pages": 48, "isbn": "978-1-00000-000-2"},
            ])
        books = BookRepository(session)
        print("Каталог книг:")
        for book in books.get_all():
            print(f"{book.id}: {book.title} ({book.year}), {book.pages} стор., автор ID={book.author_id}")
        print("Книга з найбільшою кількістю сторінок:", books.largest_book())
        print(f"Середня кількість сторінок: {books.average_pages():.2f}")

if __name__ == "__main__":
    main()
