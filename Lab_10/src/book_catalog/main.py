"""Command-line entry point for the Book Catalog API."""

import uvicorn


def main() -> None:
    """Start the local API server."""
    uvicorn.run("book_catalog.api:app", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
