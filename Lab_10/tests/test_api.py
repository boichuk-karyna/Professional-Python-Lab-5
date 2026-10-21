def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_get_book(client):
    payload = {
        "title": "Кобзар",
        "author": "Тарас Шевченко",
        "year": 1840,
        "pages": 250
    }
    create_res = client.post("/books", json=payload)
    assert create_res.status_code == 201
    data = create_res.json()
    assert data["title"] == "Кобзар"
    assert "id" in data

    get_res = client.get("/books")
    assert get_res.status_code == 200
    books = get_res.json()
    assert len(books) == 1
    assert books[0]["author"] == "Тарас Шевченко"


def test_authors_and_statistics(client):
    client.post("/books", json={"title": "Book A", "author": "Author 1", "year": 2020, "pages": 100})
    client.post("/books", json={"title": "Book B", "author": "Author 1", "year": 2021, "pages": 300})

    authors_res = client.get("/authors")
    assert authors_res.status_code == 200
    assert len(authors_res.json()) == 1

    stats_res = client.get("/statistics")
    assert stats_res.status_code == 200
    stats = stats_res.json()
    assert stats["total_books"] == 2
    assert stats["average_pages"] == 200.0
    assert stats["largest_book"]["pages"] == 300
