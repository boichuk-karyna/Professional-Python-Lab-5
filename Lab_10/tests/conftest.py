import pytest
from book_catalog.repositories import BookRepository
from book_catalog.services import BookService

@pytest.fixture
def repository():
    return BookRepository()

@pytest.fixture
def service(repository):
    return BookService(repository)
