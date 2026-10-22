def make_book(title="Кобзар", author="Тарас Шевченко", year=1840, pages=320, isbn="9786170000001"):
    return {"title": title, "author_name": author, "year": year, "pages": pages, "isbn": isbn}


def test_root_and_health(client):
    assert client.get("/").status_code == 200
    assert client.get("/health").json()["status"] == "ok"


def test_create_book_returns_201_and_author(client):
    response = client.post("/books", json=make_book())
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Кобзар"
    assert data["author_name"] == "Тарас Шевченко"
    assert data["author_id"] > 0


def test_get_book(client):
    created = client.post("/books", json=make_book()).json()
    response = client.get(f"/books/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_missing_book_returns_404(client):
    assert client.get("/books/999").status_code == 404


def test_patch_book(client):
    created = client.post("/books", json=make_book()).json()
    response = client.patch(f"/books/{created['id']}", json={"pages": 400})
    assert response.status_code == 200
    assert response.json()["pages"] == 400


def test_patch_empty_payload_is_rejected(client):
    created = client.post("/books", json=make_book()).json()
    response = client.patch(f"/books/{created['id']}", json={})
    assert response.status_code == 422


def test_delete_book(client):
    created = client.post("/books", json=make_book()).json()
    response = client.delete(f"/books/{created['id']}")
    assert response.status_code == 204
    assert client.get(f"/books/{created['id']}").status_code == 404


def test_invalid_year_validation(client):
    response = client.post("/books", json=make_book(year=0))
    assert response.status_code == 422


def test_invalid_pages_validation(client):
    response = client.post("/books", json=make_book(pages=0))
    assert response.status_code == 422


def test_duplicate_isbn_returns_409(client):
    client.post("/books", json=make_book())
    response = client.post("/books", json=make_book(title="Інша книга"))
    assert response.status_code == 409


def test_filter_by_author_and_year(client):
    client.post("/books", json=make_book())
    client.post("/books", json=make_book("Лісова пісня", "Леся Українка", 1911, 150, "9786170000002"))
    response = client.get("/books", params={"author_name": "Шевченко", "year_from": 1800, "year_to": 1900})
    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["items"][0]["title"] == "Кобзар"


def test_pagination_and_sorting(client):
    client.post("/books", json=make_book())
    client.post("/books", json=make_book("А", "Автор А", 2000, 100, "9786170000003"))
    response = client.get("/books", params={"page": 1, "page_size": 1, "sort_by": "pages", "order": "desc"})
    assert response.status_code == 200
    assert len(response.json()["items"]) == 1
    assert response.json()["items"][0]["pages"] == 320
    assert response.json()["total"] == 2


def test_invalid_year_range(client):
    response = client.get("/books", params={"year_from": 2000, "year_to": 1900})
    assert response.status_code == 422


def test_author_endpoints(client):
    response = client.post("/authors", json={"name": "Леся Українка", "biography": "Українська письменниця"})
    assert response.status_code == 201
    author_id = response.json()["id"]
    assert client.get("/authors").status_code == 200
    assert client.get(f"/authors/{author_id}/books").json() == []


def test_duplicate_author_returns_409(client):
    client.post("/authors", json={"name": "Леся Українка"})
    response = client.post("/authors", json={"name": "Леся Українка"})
    assert response.status_code == 409


def test_statistics(client):
    client.post("/books", json=make_book())
    client.post("/books", json=make_book("Лісова пісня", "Леся Українка", 1911, 160, "9786170000002"))
    response = client.get("/books/statistics")
    assert response.status_code == 200
    assert response.json()["total_books"] == 2
    assert response.json()["average_pages"] == 240
    assert response.json()["largest_book"]["title"] == "Кобзар"


def test_batch_validation(client):
    assert client.post("/authors/batch-books", json={"author_ids": []}).status_code == 422
    assert client.post("/authors/batch-books", json={"author_ids": [1, 1]}).status_code == 422


def test_csv_import_endpoint(client):
    csv_data = "title,author_name,year,pages,isbn\nКобзар,Тарас Шевченко,1840,320,9786170000001\n"
    response = client.post("/books/import.csv", content=csv_data, headers={"Content-Type": "text/csv"})
    assert response.status_code == 200
    assert response.json() == {"imported": 1}
    assert client.get("/books").json()["items"][0]["title"] == "Кобзар"


def test_csv_import_rejects_invalid_header(client):
    response = client.post(
        "/books/import.csv", content="name,year\nExample,2000\n", headers={"Content-Type": "text/csv"}
    )
    assert response.status_code == 422


def test_json_export_endpoint(client):
    client.post("/books", json=make_book())
    response = client.get("/books/export.json")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    assert response.json()[0]["title"] == "Кобзар"
