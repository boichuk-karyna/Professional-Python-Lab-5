# Book Catalog — Lab 10, Variant 2

Production-oriented REST API for a book catalog, prepared for Laboratory Work No. 10: Packaging, environment configuration, Docker, automated tests and CI/CD.

## Features

- Add, list, update and delete books.
- Search by author and title; filter by publication year.
- List unique authors and books by author ID.
- Calculate total books, average page count and the largest book.
- SQLite persistence, configurable with `DATABASE_URL`.
- FastAPI interactive docs at `/docs` and `/redoc`.
- Health endpoint at `/health`.
- `wheel` and `sdist` package builds, Docker image and GitHub Actions CI.

Book fields: `title`, `author`, `year`, `pages`. Input is validated; page count must be positive and year must be between 0 and 2100.

## Requirements

- Python 3.11 or newer
- Docker Desktop for container commands
- Git for version control

## Install and run locally

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
uvicorn book_catalog.api:app --reload
```

Open `http://127.0.0.1:8000/docs`. The default SQLite database is stored in `data/book_catalog.db`.

On Linux/macOS, activate the environment with `source .venv/bin/activate` and copy the sample configuration with `cp .env.example .env`.

## Configuration and secrets

Configuration is read from environment variables. Supported variables:

| Variable | Default | Purpose |
|---|---|---|
| `APP_NAME` | `Book Catalog API` | API title |
| `APP_ENV` or `ENVIRONMENT` | `development` | Environment label |
| `DATABASE_URL` | `sqlite:///./data/book_catalog.db` | SQLAlchemy database URL |
| `LOG_LEVEL` | `INFO` | Logging level |

For PowerShell, set values before starting the server:

```powershell
$env:APP_ENV = "development"
$env:LOG_LEVEL = "DEBUG"
$env:DATABASE_URL = "sqlite:///./data/book_catalog.db"
uvicorn book_catalog.api:app
```

For production, pass environment values through the hosting platform or `docker run -e`. Never commit `.env` or place real passwords, API keys, tokens, or database credentials in source code, Dockerfile, README or Git history. `.env.example` contains placeholders only. If a future deployment needs secrets in GitHub Actions, store them in repository Settings → Secrets and variables → Actions and reference them as `${{ secrets.SECRET_NAME }}`.

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health status and environment |
| `POST` | `/books` | Add a book |
| `GET` | `/books` | List books; optional `author`, `year`, `search` query parameters |
| `GET` | `/books/{book_id}` | Get one book |
| `PATCH` | `/books/{book_id}` | Update selected fields |
| `DELETE` | `/books/{book_id}` | Delete a book |
| `GET` | `/books/statistics` | Total, average pages and largest book |
| `GET` | `/authors` | Distinct authors |
| `GET` | `/authors/{author_id}/books` | Books for author ID |

Author IDs are stable only for the current sorted list of distinct authors (one-based positions). This keeps the required `/authors/{id}/books` route without introducing a separate author table.

Example request:

```json
{
  "title": "Кобзар",
  "author": "Тарас Шевченко",
  "year": 1840,
  "pages": 320
}
```

Quick health check:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

## Tests and quality checks

```powershell
pytest -v
ruff check .
ruff format --check .
mypy src
```

Tests cover schema validation, CRUD endpoints, author search, year filtering, statistics, error responses and health status. Tests use an isolated in-memory SQLite database.

## Build wheel and source distribution

```powershell
python -m build
Get-ChildItem dist
```

Expected artifacts include `book_catalog-1.0.0-py3-none-any.whl` and `book_catalog-1.0.0.tar.gz`.

To check the wheel in a clean environment:

```powershell
py -m venv wheel-test
.\wheel-test\Scripts\Activate.ps1
python -m pip install dist\book_catalog-1.0.0-py3-none-any.whl
book-catalog
```

The console command starts the API server. Use a separate terminal to call `/health`.

## Docker

Build the image:

```powershell
docker build -t book-catalog:1.0 .
```

Run with persistent storage and environment configuration:

```powershell
docker run --rm -p 8000:8000 `
  -e APP_ENV=production `
  -e LOG_LEVEL=INFO `
  -e DATABASE_URL=sqlite:////app/data/book_catalog.db `
  -v book_catalog_data:/app/data `
  book-catalog:1.0
```

Verify `http://localhost:8000/health` and `http://localhost:8000/docs`. The Docker image runs as a non-root user and includes a Docker `HEALTHCHECK`. The volume preserves the SQLite database across container recreation.

## CI/CD

`.github/workflows/ci.yml` runs on pushes to `main`/`develop`, pull requests and manual dispatch. It installs the package and runs Ruff lint, Ruff format check, mypy, pytest, wheel/sdist build, artifact checks and Docker image build.

## Project structure

```text
book-catalog/
├── .github/workflows/ci.yml
├── src/book_catalog/
│   ├── __init__.py
│   ├── api.py
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── repositories.py
│   ├── schemas.py
│   └── services.py
├── tests/
│   ├── conftest.py
│   ├── test_api.py
│   └── test_services.py
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── LICENSE
├── pyproject.toml
└── README.md
```

## Demonstration checklist

1. Show the Git repository and `src` layout.
2. Run `pytest -v`, `ruff check .`, `ruff format --check .` and `mypy src`.
3. Run `python -m build` and show both files in `dist`.
4. Install the wheel in a clean virtual environment.
5. Build and run the Docker image with a persistent volume.
6. Open `/health` and `/docs`, create a book and demonstrate filtering/statistics.
7. Show the latest successful GitHub Actions run.
8. Explain environment variables and why secrets are not committed.

## Git workflow suggestion

Use meaningful commits such as `Add production configuration`, `Add Python packaging`, `Add Docker support`, `Add CI pipeline`, and `Document release workflow`. Before final release, check that `.env` and database files are not tracked.
