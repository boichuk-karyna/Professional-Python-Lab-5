"""API and business-function tests."""
def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_search_and_year_filter(client):
    first = client.post("/books", json={"title": "The Hobbit", "author": "J. R. R. Tolkien", "year": 1937, "pages": 310})
    second = client.post("/books", json={"title": "Dune", "author": "Frank Herbert", "year": 1965, "pages": 500})
    assert first.status_code == 201
    assert second.status_code == 201
    assert len(client.get("/books", params={"author": "tolkien"}).json()) == 1
    assert client.get("/books", params={"year": 1965}).json()[0]["title"] == "Dune"


def test_author_and_statistics(client):
    client.post("/books", json={"title": "Short Book", "author": "A. Writer", "year": 2020, "pages": 100})
    client.post("/books", json={"title": "Long Book", "author": "B. Writer", "year": 2021, "pages": 700})
    authors = client.get("/authors").json()
    assert len(authors) == 2
    assert client.get("/books/statistics/largest").json()["title"] == "Long Book"
    assert client.get("/books/statistics/average-pages").json()["average_pages"] == 400
    assert len(client.get(f"/authors/{authors[0]['id']}/books").json()) == 1


def test_invalid_book_rejected(client):
    response = client.post("/books", json={"title": "", "author": "Author", "year": 2020, "pages": 0})
    assert response.status_code == 422
