"""Command-line entry point for the Book Catalog API."""

import uvicorn

from book_catalog.database import init_database


def main() -> None:
    """Initialize persistence and start the API server."""
    init_database()
    uvicorn.run("book_catalog.api:app", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
