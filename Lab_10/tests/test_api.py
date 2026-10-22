def test_health_endpoint(api_client):
    response = api_client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_get_books(api_client):
    response = api_client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_authors(api_client):
    response = api_client.get("/authors")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_author_books(api_client):
    response = api_client.get("/authors/1/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
