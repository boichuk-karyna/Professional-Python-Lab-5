# Book Catalog System

Production-oriented Python application for managing book catalog data (Lab 10, Variant 2).

## Description
This project provides a robust API and domain layer for book accounting, including authors, books, year filtering, page statistics, and persistence.

## Project Structure
- `src/book_catalog`: Source code of the application.
- `tests/`: Automated tests suite.
- `.github/workflows/ci.yml`: Continuous Integration configuration for GitHub Actions.
- `Dockerfile`: Containerization setup.

## Quick Start (Local)
1. Install dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
2. Copy environment file:
   ```bash
   cp .env.example .env
   ```
3. Run the API:
   ```bash
   uvicorn book_catalog.api:app --reload
   ```

## Running with Docker
1. Build the Docker image:
   ```bash
   docker build -t book-catalog:1.0 .
   ```
2. Run the container:
   ```bash
   docker run --rm -p 8000:8000 --env-file .env book-catalog:1.0
   ```

## API Documentation
- Health Check: `GET /health`
- Interactive Swagger UI: `http://localhost:8000/docs`
- ReDoc UI: `http://localhost:8000/redoc`

## Running Quality Checks
- **Linting:** `ruff check .`
- **Formatting:** `ruff format --check .`
- **Type Checking:** `mypy src`
- **Testing:** `pytest -v`
