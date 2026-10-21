# Book Catalog — Lab 10, Variant 2

Production-oriented Python package and REST API for managing a book catalog. The project is the **second variant: Book Catalog** (`book-catalog` / `book_catalog`). Book fields are title, author, publication year, and page count.

## Features

- Add books and automatically create authors when needed.
- List and search books by author; filter by publication year.
- List authors and their book counts; list books for a selected author.
- Calculate average page count and identify the largest book.
- SQLite persistence, environment-based configuration, structured logging, Docker health check, automated tests, package build, and GitHub Actions CI.

## Requirements

Python 3.11+ for local use. Docker is required only for container execution.

## Installation and local run

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Copy `.env.example` to `.env` and adjust values if needed. Start the API:

```bash
book-catalog
# alternatively:
uvicorn book_catalog.api:app --host 127.0.0.1 --port 8000
```

The default database is `book_catalog.db` in the current directory. Tables are created on application startup.

## Configuration and secrets

| Variable | Default | Purpose |
|---|---|---|
| `APP_NAME` | `Book Catalog` | API title |
| `ENVIRONMENT` | `development` | Runtime environment |
| `DATABASE_URL` | `sqlite:///./book_catalog.db` | SQLAlchemy database URL |
| `LOG_LEVEL` | `INFO` | Logging level |

Configuration is read from environment variables and optional local `.env`. `.env` is ignored by Git. `.env.example` contains placeholders only. Never commit passwords, tokens, API keys, or production database credentials.

PowerShell example:

```powershell
$env:ENVIRONMENT="production"
$env:LOG_LEVEL="INFO"
$env:DATABASE_URL="sqlite:///./book_catalog.db"
```

## REST API

Interactive Swagger documentation: <http://localhost:8000/docs>. ReDoc: <http://localhost:8000/redoc>. OpenAPI JSON: <http://localhost:8000/openapi.json>.

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health status and current environment |
| `POST` | `/books` | Add a book |
| `GET` | `/books` | List books; optional `author` and `year` query filters |
| `GET` | `/books/statistics` | Largest book and average page count |
| `GET` | `/authors` | List authors and their book counts |
| `GET` | `/authors/{author_id}/books` | List books by author ID |

Example request body for `POST /books`:

```json
{
  "title": "Kobzar",
  "author": "Taras Shevchenko",
  "year": 1840,
  "pages": 320
}
```

## Tests and code quality

```bash
pytest -v --cov=book_catalog --cov-report=term-missing
ruff check .
ruff format --check .
mypy src
```

## Packaging

```bash
python -m pip install build
python -m build
```

The `dist/` directory contains a wheel (`.whl`) and source distribution (`.tar.gz`). To check wheel installation in a clean environment, create a new virtual environment and install the generated wheel with `python -m pip install dist/book_catalog-1.0.0-py3-none-any.whl` (the exact filename may use normalized project-name separators).

## Docker

Build the image:

```bash
docker build -t book-catalog:1.0 .
```

Run it with persistent SQLite storage:

```bash
docker volume create book_catalog_data
docker run --rm -p 8000:8000 -e ENVIRONMENT=production -e LOG_LEVEL=INFO -v book_catalog_data:/app/data book-catalog:1.0
```

The container uses a non-root user and includes a Docker `HEALTHCHECK`. Visit <http://localhost:8000/health> and <http://localhost:8000/docs>. You can pass additional configuration with `-e NAME=value` or `--env-file .env`; do not bake secrets into the image.

## CI/CD

`.github/workflows/ci.yml` runs on pushes to `main`/`develop` and on pull requests. It installs the package, runs Ruff lint and formatting checks, runs mypy and pytest with coverage, builds wheel and sdist, checks that both artifacts exist, and builds the Docker image.

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

1. Run `pytest -v`, `ruff check .`, `ruff format --check .`, and `mypy src`.
2. Run `python -m build` and show wheel and sdist in `dist/`.
3. Build and start the Docker container.
4. Demonstrate `/health`, `/docs`, adding a book, filtering by author/year, author listing, and statistics.
5. Show the latest successful GitHub Actions run and explain environment variables and secret handling.

## License

MIT. See `LICENSE`.
