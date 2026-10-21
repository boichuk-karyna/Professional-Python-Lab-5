"""Console entry point for the Book Catalog API."""

import uvicorn

from book_catalog.api import app
from book_catalog.config import get_settings
from book_catalog.database import init_database


def main() -> None:
    """Initialize persistence and start the ASGI server."""
    init_database()
    settings = get_settings()
    uvicorn.run(app, host=settings.host, port=settings.port)


# Initialize the database when launched by `uvicorn book_catalog.main:app`.
init_database()

__all__ = ["app", "main"]

if __name__ == "__main__":
    main()
