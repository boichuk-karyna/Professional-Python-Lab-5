from book_catalog.api import app
from book_catalog.database import init_database

init_database()

__all__ = ["app"]
