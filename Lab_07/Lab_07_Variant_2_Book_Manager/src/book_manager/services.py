from __future__ import annotations
from sqlalchemy.orm import Session
from .models import Author, Book

def add_author_with_books(session: Session, author_name: str,
                          books: list[dict[str, object]],
                          biography: str | None = None) -> Author:
    """Create author and all books atomically; rollback every change on failure."""
    try:
        author = Author(name=author_name, biography=biography)
        session.add(author)
        session.flush()  # obtain author.id without committing
        for item in books:
            session.add(Book(
                title=str(item["title"]),
                year=int(item["year"]),
                pages=int(item["pages"]),
                isbn=str(item["isbn"]) if item.get("isbn") is not None else None,
                author_id=author.id,
            ))
        session.commit()
        session.refresh(author)
        return author
    except Exception:
        session.rollback()
        raise
