from book_manager.api import app
from book_manager.database import init_database

init_database()

__all__ = ["app"]
