import sqlite3
from book_manager.db_api import find_books_by_author

def test_parameterized_db_api_search(tmp_path):
    db = tmp_path / "test.db"
    with sqlite3.connect(db) as conn:
        conn.execute("PRAGMA foreign_keys=ON")
        conn.execute("CREATE TABLE authors (id INTEGER PRIMARY KEY, name TEXT NOT NULL)")
        conn.execute("""CREATE TABLE books (
            id INTEGER PRIMARY KEY, title TEXT, year INTEGER, pages INTEGER,
            author_id INTEGER REFERENCES authors(id))""")
        conn.execute("INSERT INTO authors(name) VALUES (?)", ("A Author",))
        conn.execute("INSERT INTO books(title,year,pages,author_id) VALUES (?,?,?,?)",
                     ("DB Book", 2020, 222, 1))
    result = find_books_by_author(db, "A Author")
    assert len(result) == 1 and result[0][1] == "DB Book"
    assert find_books_by_author(db, "' OR 1=1 --") == []
