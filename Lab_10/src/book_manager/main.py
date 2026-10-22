"""Application entry point."""
import uvicorn

from book_manager.api import app
from book_manager.database import init_database


def main() -> None:
    init_database()
    uvicorn.run(app, host="127.0.0.1", port=8000)


__all__ = ["app", "main"]
