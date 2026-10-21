"""API integration tests."""


def add_author(client, name="Terry Pratchett"):
    response = client.post("/authors", json={"name": name})
    assert response.status_code == 201
    return response.json()


def add_book(client, author_id, title, year, pages):
    return client.post(
        "/books",
        json={
            "title": title,
            "author_id": author_id,
            "year": year,
            "pages": pages,
        },
    )


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
    response = add_book(client, author["id"], "Guards! Guards!", 1989, 400)
    assert response.status_code == 201
    assert response.json()["title"] == "Guards! Guards!"


def test_missing_author_rejected(client):
    response = add_book(client, 999, "Unknown", 2000, 100)
    assert response.status_code == 404


def test_invalid_pages_rejected(client):
    author = add_author(client)
    response = add_book(client, author["id"], "Invalid", 2000, 0)
    assert response.status_code == 422


def test_filter_by_year(client):
    author = add_author(client)
    add_book(client, author["id"], "Book A", 2001, 120)
    add_book(client, author["id"], "Book B", 2002, 120)
    response = client.get("/books?year=2001")
    assert [book["title"] for book in response.json()] == ["Book A"]


def test_search_by_author(client):
    author = add_author(client, "Ursula Le Guin")
    add_book(client, author["id"], "A Wizard of Earthsea", 1968, 205)
    response = client.get("/books?author=ursula")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_books_for_author(client):
    author = add_author(client)
    add_book(client, author["id"], "Small Gods", 1992, 300)
    response = client.get(f"/authors/{author['id']}/books")
    assert response.status_code == 200
    assert response.json()[0]["title"] == "Small Gods"


def test_unknown_author_books_returns_404(client):
    assert client.get("/authors/999/books").status_code == 404


def test_statistics(client):
    author = add_author(client)
    add_book(client, author["id"], "Short", 2000, 100)
    add_book(client, author["id"], "Long", 2000, 300)
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
    add_book(client, author["id"], "Older", 1990, 200)
    add_book(client, author["id"], "Newer", 2000, 250)
    response = client.get("/books?author=terry&year=2000")
    assert [book["title"] for book in response.json()] == ["Newer"]


def test_title_validation(client):
    author = add_author(client)
    response = add_book(client, author["id"], "", 2000, 100)
    assert response.status_code == 422
