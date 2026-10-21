"""Integration tests for the REST API."""

from fastapi.testclient import TestClient


def add_book(client: TestClient, title: str, author: str, year: int, pages: int):
    response = client.post(
        "/books",
        json={"title": title, "author": author, "year": year, "pages": pages},
    )
    assert response.status_code == 201
    return response.json()


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_and_read_book(client: TestClient) -> None:
    book = add_book(client, "Кобзар", "Тарас Шевченко", 1840, 320)
    response = client.get(f"/books/{book['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Кобзар"


def test_list_books(client: TestClient) -> None:
    add_book(client, "Кобзар", "Тарас Шевченко", 1840, 320)
    assert len(client.get("/books").json()) == 1


def test_search_by_author(client: TestClient) -> None:
    add_book(client, "Кобзар", "Тарас Шевченко", 1840, 320)
    response = client.get("/books", params={"author": "Шевченко"})
    assert len(response.json()) == 1


def test_filter_by_year(client: TestClient) -> None:
    add_book(client, "Кобзар", "Тарас Шевченко", 1840, 320)
    add_book(client, "Лісова пісня", "Леся Українка", 1911, 100)
    response = client.get("/books", params={"year": 1911})
    assert [book["title"] for book in response.json()] == ["Лісова пісня"]


def test_search_by_title(client: TestClient) -> None:
    add_book(client, "Кобзар", "Тарас Шевченко", 1840, 320)
    assert len(client.get("/books", params={"search": "Коб"}).json()) == 1


def test_update_book(client: TestClient) -> None:
    book = add_book(client, "Кобзар", "Тарас Шевченко", 1840, 320)
    response = client.patch(f"/books/{book['id']}", json={"pages": 350})
    assert response.status_code == 200
    assert response.json()["pages"] == 350


def test_delete_book(client: TestClient) -> None:
    book = add_book(client, "Кобзар", "Тарас Шевченко", 1840, 320)
    assert client.delete(f"/books/{book['id']}").status_code == 204
    assert client.get(f"/books/{book['id']}").status_code == 404


def test_missing_book_returns_404(client: TestClient) -> None:
    assert client.get("/books/999").status_code == 404


def test_invalid_book_returns_422(client: TestClient) -> None:
    response = client.post(
        "/books", json={"title": "", "author": "A", "year": 2020, "pages": 10}
    )
    assert response.status_code == 422


def test_authors_endpoint(client: TestClient) -> None:
    add_book(client, "Книга Б", "Автор Б", 2000, 100)
    add_book(client, "Книга А", "Автор А", 2001, 120)
    assert client.get("/authors").json() == ["Автор А", "Автор Б"]


def test_books_for_author(client: TestClient) -> None:
    add_book(client, "Книга", "Автор", 2000, 100)
    response = client.get("/authors/1/books")
    assert response.status_code == 200
    assert response.json()[0]["author"] == "Автор"


def test_unknown_author_returns_404(client: TestClient) -> None:
    assert client.get("/authors/100/books").status_code == 404


def test_statistics(client: TestClient) -> None:
    add_book(client, "Книга А", "Автор А", 2000, 100)
    add_book(client, "Книга Б", "Автор Б", 2001, 300)
    result = client.get("/books/statistics").json()
    assert result["total_books"] == 2
    assert result["average_pages"] == 200.0
    assert result["largest_book"]["title"] == "Книга Б"


def test_empty_statistics(client: TestClient) -> None:
    result = client.get("/books/statistics").json()
    assert result == {"total_books": 0, "average_pages": 0.0, "largest_book": None}


def test_trim_text_fields(client: TestClient) -> None:
    book = add_book(client, "  Книга  ", "  Автор  ", 2000, 100)
    assert book["title"] == "Книга"
    assert book["author"] == "Автор"
