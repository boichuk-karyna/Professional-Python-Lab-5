from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_list_search_and_filter_books(client: TestClient) -> None:
    first = client.post(
        "/books",
        json={"title": "The Hobbit", "author": "J. R. R. Tolkien", "year": 1937, "pages": 310},
    )
    second = client.post(
        "/books",
        json={"title": "The Silmarillion", "author": "J. R. R. Tolkien", "year": 1977, "pages": 365},
    )
    assert first.status_code == 201
    assert second.status_code == 201
    assert len(client.get("/books", params={"author": "tolkien"}).json()) == 2
    assert client.get("/books", params={"year": 1937}).json()[0]["title"] == "The Hobbit"
    assert client.get("/books", params={"q": "silmarillion"}).json()[0]["pages"] == 365


def test_authors_and_books_by_author(client: TestClient) -> None:
    client.post("/books", json={"title": "Dune", "author": "Frank Herbert", "year": 1965, "pages": 412})
    authors = client.get("/authors").json()
    assert len(authors) == 1
    books = client.get(f"/authors/{authors[0]['id']}/books")
    assert books.status_code == 200
    assert books.json()[0]["title"] == "Dune"


def test_validation_and_missing_records(client: TestClient) -> None:
    invalid = client.post(
        "/books",
        json={"title": " ", "author": "A", "year": 1200, "pages": 0},
    )
    assert invalid.status_code == 422
    assert client.get("/books/999").status_code == 404
    assert client.get("/authors/999/books").status_code == 404
    assert client.delete("/books/999").status_code == 404


def test_statistics_and_delete(client: TestClient) -> None:
    client.post("/books", json={"title": "Short", "author": "A", "year": 2000, "pages": 100})
    client.post("/books", json={"title": "Long", "author": "B", "year": 2001, "pages": 300})
    statistics = client.get("/books/statistics").json()
    assert statistics["count"] == 2
    assert statistics["average_pages"] == 200
    assert statistics["largest_book"]["title"] == "Long"
    book_id = statistics["largest_book"]["id"]
    assert client.delete(f"/books/{book_id}").status_code == 204
