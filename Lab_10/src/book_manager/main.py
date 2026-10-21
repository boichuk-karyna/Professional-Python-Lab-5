"""Console entry point for the Book Manager API."""

import uvicorn

from book_manager.api import app
from book_manager.config import get_settings
from book_manager.database import init_database


def main() -> None:
    """Initialize persistence and start the ASGI server."""
    init_database()
    settings = get_settings()
    uvicorn.run(app, host=settings.host, port=settings.port)


# Initialize the database when launched by `uvicorn book_manager.main:app`.
init_database()

__all__ = ["app", "main"]

if __name__ == "__main__":
    main()
