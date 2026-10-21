"""Database operations for books and authors."""
from typing import Any

from book_catalog.database import connect
from book_catalog.models import BookCreate


def list_books(author: str | None = None, year: int | None = None) -> list[dict[str, Any]]:
    sql = "SELECT b.id, b.title, a.name AS author, b.year, b.pages FROM books b JOIN authors a ON a.id=b.author_id WHERE 1=1"
    params: list[object] = []
    if author:
        sql += " AND lower(a.name) LIKE lower(?)"
        params.append(f"%{author}%")
    if year is not None:
        sql += " AND b.year = ?"
        params.append(year)
    sql += " ORDER BY b.id"
    with connect() as db:
        return [dict(row) for row in db.execute(sql, params).fetchall()]


def create_book(book: BookCreate) -> dict[str, Any]:
    with connect() as db:
        db.execute("INSERT OR IGNORE INTO authors(name) VALUES (?)", (book.author.strip(),))
        author_row = db.execute("SELECT id FROM authors WHERE name = ?", (book.author.strip(),)).fetchone()
        if author_row is None:
            raise RuntimeError("Unable to create or find author.")
        cursor = db.execute(
            "INSERT INTO books(title, author_id, year, pages) VALUES (?, ?, ?, ?)",
            (book.title.strip(), author_row["id"], book.year, book.pages),
        )
        book_id = cursor.lastrowid
    result = get_book(book_id)
    if result is None:
        raise RuntimeError("Book was created but could not be retrieved.")
    return result


def get_book(book_id: int) -> dict[str, Any] | None:
    with connect() as db:
        row = db.execute("SELECT b.id, b.title, a.name AS author, b.year, b.pages FROM books b JOIN authors a ON a.id=b.author_id WHERE b.id=?", (book_id,)).fetchone()
        return dict(row) if row else None


def list_authors() -> list[dict[str, Any]]:
    with connect() as db:
        return [dict(row) for row in db.execute("SELECT id, name FROM authors ORDER BY name").fetchall()]


def author_books(author_id: int) -> list[dict[str, Any]]:
    with connect() as db:
        return [dict(row) for row in db.execute("SELECT b.id, b.title, a.name AS author, b.year, b.pages FROM books b JOIN authors a ON a.id=b.author_id WHERE a.id=? ORDER BY b.id", (author_id,)).fetchall()]


def largest_book() -> dict[str, Any] | None:
    with connect() as db:
        row = db.execute("SELECT b.id, b.title, a.name AS author, b.year, b.pages FROM books b JOIN authors a ON a.id=b.author_id ORDER BY b.pages DESC, b.id LIMIT 1").fetchone()
        return dict(row) if row else None


def average_pages() -> float:
    with connect() as db:
        row = db.execute("SELECT AVG(pages) AS average FROM books").fetchone()
        return float(row["average"]) if row and row["average"] is not None else 0.0
