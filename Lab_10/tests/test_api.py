"""API integration tests for the book catalog."""


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_add_and_list_books(client):
    response = client.post(
        "/books",
        json={"title": "Kobzar", "author": "Taras Shevchenko", "year": 1840, "pages": 320},
    )
    assert response.status_code == 201
    assert response.json()["author"] == "Taras Shevchenko"
    books = client.get("/books")
    assert books.status_code == 200
    assert len(books.json()) == 1


def test_filter_books_by_year_and_author(client):
    client.post("/books", json={"title": "Book A", "author": "Author A", "year": 2000, "pages": 100})
    client.post("/books", json={"title": "Book B", "author": "Author B", "year": 2020, "pages": 200})
    assert len(client.get("/books", params={"year": 2000}).json()) == 1
    assert len(client.get("/books", params={"author": "Author B"}).json()) == 1


def test_authors_and_author_books(client):
    client.post("/books", json={"title": "Book A", "author": "Author A", "year": 2000, "pages": 100})
    authors = client.get("/authors").json()
    assert authors == [{"id": 1, "name": "Author A", "book_count": 1}]
    assert client.get("/authors/1/books").json()[0]["title"] == "Book A"
    assert client.get("/authors/999/books").status_code == 404


def test_statistics(client):
    client.post("/books", json={"title": "Short", "author": "A", "year": 2000, "pages": 100})
    client.post("/books", json={"title": "Long", "author": "B", "year": 2001, "pages": 300})
    result = client.get("/books/statistics").json()
    assert result["largest_book"]["title"] == "Long"
    assert result["average_pages"] == 200.0


def test_invalid_book_is_rejected(client):
    response = client.post(
        "/books",
        json={"title": "", "author": "Author", "year": 2020, "pages": 0},
    )
    assert response.status_code == 422


def test_empty_statistics(client):
    result = client.get("/books/statistics")
    assert result.status_code == 200
    assert result.json() == {"largest_book": None, "average_pages": 0.0}


def test_same_author_is_reused(client):
    first = client.post(
        "/books",
        json={"title": "First", "author": "Shared Author", "year": 2001, "pages": 120},
    )
    second = client.post(
        "/books",
        json={"title": "Second", "author": "Shared Author", "year": 2002, "pages": 220},
    )
    assert first.status_code == second.status_code == 201
    authors = client.get("/authors").json()
    assert len(authors) == 1
    assert authors[0]["book_count"] == 2


def test_filter_combines_author_and_year(client):
    client.post(
        "/books",
        json={"title": "Target", "author": "Ada Lovelace", "year": 1843, "pages": 90},
    )
    client.post(
        "/books",
        json={"title": "Other year", "author": "Ada Lovelace", "year": 1844, "pages": 100},
    )
    client.post(
        "/books",
        json={"title": "Other author", "author": "Grace Hopper", "year": 1843, "pages": 110},
    )
    response = client.get("/books", params={"author": "Ada", "year": 1843})
    assert response.status_code == 200
    assert [book["title"] for book in response.json()] == ["Target"]


def test_invalid_year_and_page_count_are_rejected(client):
    bad_year = client.post(
        "/books",
        json={"title": "Book", "author": "Author", "year": 9999, "pages": 100},
    )
    bad_pages = client.post(
        "/books",
        json={"title": "Book", "author": "Author", "year": 2020, "pages": -1},
    )
    assert bad_year.status_code == 422
    assert bad_pages.status_code == 422


def test_unknown_author_id_returns_not_found(client):
    response = client.get("/authors/12345/books")
    assert response.status_code == 404
    assert response.json()["detail"] == "Author not found"
