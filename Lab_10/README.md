# Book Catalog

Production-oriented REST API for a book catalog (individual variant 2). The project keeps the book domain and adds packaging, environment-based configuration, Docker, automated quality checks, tests, and documentation.

## Features

- Add, list, retrieve, and delete books.
- Search by author and title.
- Filter by publication year.
- List authors and retrieve an author's books.
- Statistics: largest book and average page count.
- CSV import and JSON export service functions.
- SQLAlchemy persistence, configurable database URL, health endpoint.
- OpenAPI documentation, Docker image, GitHub Actions CI.

## Requirements

Python 3.11+ for local use. Docker is required only for container execution.

## Installation

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Linux/macOS:

```bash
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Configuration

Copy `.env.example` to `.env` and edit the values if needed. The `.env` file is ignored by Git.

| Variable | Purpose | Default |
|---|---|---|
| `APP_NAME` | API title | `Book Catalog` |
| `APP_ENV` or `ENVIRONMENT` | Runtime environment | `development` |
| `DATABASE_URL` | SQLAlchemy database URL | `sqlite:///./book_catalog.db` |
| `LOG_LEVEL` | Logging level | `INFO` |

No real credentials or secrets are included in the repository. For Docker, pass settings using `-e` or `--env-file`.

## Run locally

```bash
uvicorn book_catalog.api:app --reload
```

- API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health: http://localhost:8000/health

## API

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Health status and environment |
| GET | `/books` | List books; optional `author`, `year`, `q` filters |
| POST | `/books` | Add a book |
| GET | `/books/{book_id}` | Get a book |
| DELETE | `/books/{book_id}` | Delete a book |
| GET | `/books/statistics` | Count, average pages, largest book |
| GET | `/authors` | List authors |
| POST | `/authors` | Add an author |
| GET | `/authors/{author_id}/books` | List books by author |

Example request body:

```json
{
  "title": "The Hobbit",
  "author": "J. R. R. Tolkien",
  "year": 1937,
  "pages": 310,
  "description": "A fantasy novel"
}
```

## Docker

Build:

```bash
docker build -t book-catalog:1.0 .
```

Run with persistent SQLite storage and environment configuration:

```bash
docker volume create book-catalog-data
docker run --rm -p 8000:8000 \
  -e APP_ENV=production \
  -e LOG_LEVEL=INFO \
  -e DATABASE_URL=sqlite:////app/data/book_catalog.db \
  -v book-catalog-data:/app/data \
  book-catalog:1.0
```

Open http://localhost:8000/health. The Docker image defines a health check and runs as a non-root user.

## Tests and quality checks

```bash
pytest -v
ruff check .
ruff format --check .
mypy src
python -m build
```

The tests cover API health, CRUD behavior, author/title search, year filtering, statistics, validation errors, CSV import, and JSON export.

## Wheel installation check

```bash
python -m build
python -m venv wheel-test
```

Activate `wheel-test`, then run:

```bash
python -m pip install dist/book_catalog-1.0.0-py3-none-any.whl
python -c "import book_catalog; print(book_catalog.__version__)"
```

## CI/CD

`.github/workflows/ci.yml` runs on pushes to `main`/`develop` and pull requests. It executes Ruff lint and formatting checks, mypy, pytest, package build/artifact verification, and Docker image build.

## Project structure

```text
book-catalog/
├── .github/workflows/ci.yml
├── src/book_catalog/
│   ├── api.py
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── repositories.py
│   ├── schemas.py
│   └── services.py
├── tests/
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── pyproject.toml
└── README.md
```

## Demonstration checklist

1. Install the project and run the tests.
2. Start the API and open `/docs`.
3. Add two books with `POST /books`.
4. Demonstrate author search and year filtering.
5. Open `/books/statistics` and `/health`.
6. Build and run the Docker image.
7. Show the GitHub Actions workflow and its checks.
