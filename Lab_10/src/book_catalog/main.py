"""Command-line entry point."""
import uvicorn


def main() -> None:
    uvicorn.run("book_catalog.api:app", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
