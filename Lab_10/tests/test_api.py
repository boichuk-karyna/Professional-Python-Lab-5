def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_and_list_book(client):
    created = client.post(
        "/books",
        json={"title": "Кобзар", "author": "Тарас Шевченко", "year": 1840, "pages": 128},
    )
    assert created.status_code == 201
    assert created.json()["title"] == "Кобзар"

    listed = client.get("/books")
    assert listed.status_code == 200
    assert len(listed.json()) == 1
    assert listed.json()[0]["author"] == "Тарас Шевченко"


def test_filter_books_by_author_and_year(client):
    client.post("/books", json={
        "title": "Кобзар", "author": "Тарас Шевченко", "year": 1840, "pages": 128
    })
    client.post("/books", json={
        "title": "Лісова пісня", "author": "Леся Українка", "year": 1911, "pages": 96
    })
    assert len(client.get("/books", params={"author": "шевченко"}).json()) == 1
    assert len(client.get("/books", params={"year": 1911}).json()) == 1


def test_authors_and_books_endpoint(client):
    client.post("/books", json={
        "title": "Кобзар", "author": "Тарас Шевченко", "year": 1840, "pages": 128
    })
    authors = client.get("/authors").json()
    assert len(authors) == 1
    response = client.get(f"/authors/{authors[0]['id']}/books")
    assert response.status_code == 200
    assert response.json()[0]["title"] == "Кобзар"


def test_statistics(client):
    client.post("/books", json={
        "title": "Book A", "author": "Author A", "year": 2000, "pages": 100
    })
    client.post("/books", json={
        "title": "Book B", "author": "Author B", "year": 2001, "pages": 300
    })
    result = client.get("/books/statistics").json()
    assert result["count"] == 2
    assert result["average_pages"] == 200
    assert result["largest_book"]["title"] == "Book B"


def test_invalid_book_is_rejected(client):
    response = client.post("/books", json={
        "title": "", "author": "Author", "year": 2020, "pages": 0
    })
    assert response.status_code == 422


def test_unknown_author_returns_404(client):
    assert client.get("/authors/999/books").status_code == 404
