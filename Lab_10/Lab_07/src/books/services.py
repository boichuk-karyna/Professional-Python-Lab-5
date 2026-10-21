"""Business operations and transactional workflow."""
from __future__ import annotations

from collections.abc import Sequence
from sqlalchemy.orm import Session

from .models import Author, Book


def add_author_with_books(
    session: Session,
    author_name: str,
    books: Sequence[dict[str, object]],
) -> Author:
    """Insert author and all books atomically; rollback everything on any error."""
    try:
        author = Author(name=author_name.strip())
        session.add(author)
        session.flush()  # obtain author.id before inserting related books

        for item in books:
            book = Book(
                title=str(item["title"]).strip(),
                year=int(item["year"]),
                pages=int(item["pages"]),
                isbn=str(item["isbn"]).strip() if item.get("isbn") else None,
                author_id=author.id,
            )
            session.add(book)

        session.commit()
        session.refresh(author)
        return author
    except Exception:
        session.rollback()
        raise
