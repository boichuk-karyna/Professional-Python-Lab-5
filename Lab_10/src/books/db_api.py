"""A DB-API operation implemented directly with sqlite3 (without ORM)."""
import sqlite3
from pathlib import Path


def find_books_by_author(database_path: str | Path, author_name: str) -> list[tuple]:
    """Parameterized SQL search using the DB-API '?' placeholder."""
    with sqlite3.connect(str(database_path)) as connection:
        connection.execute("PRAGMA foreign_keys=ON")
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT books.id, books.title, authors.name, books.year, books.pages, books.isbn
            FROM books
            JOIN authors ON authors.id = books.author_id
            WHERE authors.name = ?
            ORDER BY books.title
            """,
            (author_name.strip(),),
        )
        return cursor.fetchall()
