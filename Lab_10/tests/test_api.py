"""API integration tests."""

def add_author(client, name="Terry Pratchett"):
    response = client.post("/authors", json={"name": name})
    assert response.status_code == 201
    return response.json()


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_and_list_author(client):
    add_author(client)
    response = client.get("/authors")
    assert response.status_code == 200
    assert response.json()[0]["name"] == "Terry Pratchett"


def test_create_book(client):
    author = add_author(client)
    response = client.post(
        "/books",
        json={"title": "Guards! Guards!", "author_id": author["id"], "year": 1989, "pages": 400},
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Guards! Guards!"


def test_missing_author_rejected(client):
    response = client.post(
        "/books",
        json={"title": "Unknown", "author_id": 999, "year": 2000, "pages": 100},
    )
    assert response.status_code == 404


def test_invalid_pages_rejected(client):
    author = add_author(client)
    response = client.post(
        "/books",
        json={"title": "Invalid", "author_id": author["id"], "year": 2000, "pages": 0},
    )
    assert response.status_code == 422


def test_filter_by_year(client):
    author = add_author(client)
    for title, year in [("Book A", 2001), ("Book B", 2002)]:
        client.post(
            "/books",
            json={"title": title, "author_id": author["id"], "year": year, "pages": 120},
        )
    response = client.get("/books?year=2001")
    assert [book["title"] for book in response.json()] == ["Book A"]


def test_search_by_author(client):
    author = add_author(client, "Ursula Le Guin")
    client.post(
        "/books",
        json={"title": "A Wizard of Earthsea", "author_id": author["id"], "year": 1968, "pages": 205},
    )
    response = client.get("/books?author=ursula")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_books_for_author(client):
    author = add_author(client)
    client.post(
        "/books",
        json={"title": "Small Gods", "author_id": author["id"], "year": 1992, "pages": 300},
    )
    response = client.get(f"/authors/{author['id']}/books")
    assert response.status_code == 200
    assert response.json()[0]["title"] == "Small Gods"


def test_unknown_author_books_returns_404(client):
    assert client.get("/authors/999/books").status_code == 404


def test_statistics(client):
    author = add_author(client)
    for title, pages in [("Short", 100), ("Long", 300)]:
        client.post(
            "/books",
            json={"title": title, "author_id": author["id"], "year": 2000, "pages": pages},
        )
    data = client.get("/statistics/books").json()
    assert data["count"] == 2
    assert data["average_pages"] == 200.0
    assert data["largest_book"]["title"] == "Long"


def test_empty_statistics(client):
    data = client.get("/statistics/books").json()
    assert data == {"count": 0, "average_pages": None, "largest_book": None}


def test_list_books_empty(client):
    response = client.get("/books")
    assert response.status_code == 200
    assert response.json() == []


def test_filter_author_and_year(client):
    author = add_author(client)
    client.post(
        "/books",
        json={"title": "Older", "author_id": author["id"], "year": 1990, "pages": 200},
    )
    client.post(
        "/books",
        json={"title": "Newer", "author_id": author["id"], "year": 2000, "pages": 250},
    )
    response = client.get("/books?author=terry&year=2000")
    assert [book["title"] for book in response.json()] == ["Newer"]


def test_title_validation(client):
    author = add_author(client)
    response = client.post(
        "/books",
        json={"title": "", "author_id": author["id"], "year": 2000, "pages": 100},
    )
    assert response.status_code == 422
