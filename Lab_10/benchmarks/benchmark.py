"""Small benchmark for the Book Manager API's local SQLite catalog."""
from time import perf_counter

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from book_manager.database import Base
from book_manager.models import Author, Book
from book_manager.repositories import BookRepository


def main() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        author = Author(name="Test Author")
        session.add(author)
        session.flush()
        session.add_all(
            Book(title=f"Book {i:04d}", year=2000 + i % 25, pages=100 + i % 500,
                 author_id=author.id)
            for i in range(1000)
        )
        session.commit()
        repository = BookRepository(session)
        start = perf_counter()
        items, total = repository.get_all(page=1, page_size=100, sort_by="title")
        elapsed = perf_counter() - start
        print(f"Books in catalog: {total}")
        print(f"Books returned: {len(items)}")
        print(f"Query elapsed: {elapsed:.6f} seconds")


if __name__ == "__main__":
    main()
