"""Command-line entry point for the Book Catalog API."""

import uvicorn

from book_catalog.api import app
from book_catalog.database import init_database


def main() -> None:
    """Initialize the database and start the API server."""
    init_database()
    uvicorn.run(
        "book_catalog.api:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )


if __name__ == "__main__":
    main()
