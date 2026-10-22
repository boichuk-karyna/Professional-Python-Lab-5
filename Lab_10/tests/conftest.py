import pytest
from fastapi.testclient import TestClient
from book_catalog.api import app

@pytest.fixture
def api_client():
    return TestClient(app)
