"""A direct sqlite3 DB-API query, intentionally separate from SQLAlchemy ORM."""
import sqlite3
from pathlib import Path

def find_books_by_author(database_path: str | Path, author_name: str) -> list[tuple]:
    with sqlite3.connect(str(database_path)) as connection:
        connection.execute("PRAGMA foreign_keys=ON")
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT books.id, books.title, books.year, books.pages, authors.name
            FROM books
            JOIN authors ON books.author_id = authors.id
            WHERE authors.name = ?
            ORDER BY books.title
            """,
            (author_name,),
        )
        return cursor.fetchall()
