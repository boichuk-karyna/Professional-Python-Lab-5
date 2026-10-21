"""Test configuration using an isolated SQLite database."""
import os
import tempfile
from pathlib import Path

_temp_dir = tempfile.TemporaryDirectory()
os.environ["DATABASE_URL"] = f"sqlite:///{Path(_temp_dir.name) / 'test.db'}"
os.environ["ENVIRONMENT"] = "test"

import pytest
from fastapi.testclient import TestClient

from book_catalog.config import get_settings
from book_catalog.api import app
from book_catalog.database import init_db


@pytest.fixture()
def client() -> TestClient:
    get_settings.cache_clear()
    init_db()
    with TestClient(app) as test_client:
        yield test_client
