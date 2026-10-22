"""Command-line entry point for the Book Manager API."""
import os

import uvicorn


def main() -> None:
    """Start the ASGI application."""
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("book_manager.main:app", host=host, port=port, log_level=os.getenv("LOG_LEVEL", "info").lower())


if __name__ == "__main__":
    main()
