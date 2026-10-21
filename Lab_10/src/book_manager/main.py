"""Application entry point for local and container execution."""

import uvicorn

from book_manager.api import app
from book_manager.database import init_database

# Ensure the schema exists when this module is imported by Uvicorn.
init_database()


def main() -> None:
    """Start the production ASGI server."""
    uvicorn.run(
        "book_manager.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )


__all__ = ["app", "main"]
