# Book Catalog — Lab 10, Variant 2

Production-oriented Book Catalog REST API, packaged as `book-catalog` / `book_catalog`.

## Features

- Create and list authors and books.
- Search books by author name.
- Filter books by publication year.
- List books belonging to an author.
- Calculate total books, average page count and the largest book.
- Validate request data and reject references to missing authors.
- SQLite persistence, environment-based configuration, structured logging.
- Wheel and source distribution builds, Docker image, GitHub Actions CI.

## Requirements

Python 3.12+ and (for container commands) Docker.

## Install and run locally

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
uvicorn book_catalog.api:app --reload
```

Open `http://127.0.0.1:8000/docs` for Swagger UI, `http://127.0.0.1:8000/redoc` for ReDoc, or `http://127.0.0.1:8000/health` for health status.

## Configuration

Copy `.env.example` to `.env`. Values are examples, not credentials.

| Variable | Purpose | Default |
|---|---|---|
| `APP_NAME` | API title | `Book Catalog API` |
| `APP_ENV` | Environment name | `development` |
| `DATABASE_URL` | SQLAlchemy database URL | `sqlite:///./data/books.db` |
| `LOG_LEVEL` | Logging level | `INFO` |

`.env` is excluded from Git and Docker build context. Do not store passwords, tokens or other real secrets in source files, README, Dockerfile, or commits. Use repository/organization Actions Secrets for CI credentials if needed.

## API

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Health status |
| `POST` | `/authors` | Create an author |
| `GET` | `/authors` | List authors |
| `POST` | `/books` | Create a book |
| `GET` | `/books` | List books; optional `year` and `author` query parameters |
| `GET` | `/authors/{author_id}/books` | List books for one author |
| `GET` | `/statistics/books` | Count, average pages, largest book |

Example request body for `POST /authors`:

```json
{"name": "Ursula Le Guin"}
```

Example request body for `POST /books`:

```json
{"title": "A Wizard of Earthsea", "author_id": 1, "year": 1968, "pages": 205}
```

## Tests and quality checks

```powershell
pytest -v
pytest -v --cov=book_catalog --cov-report=term-missing
ruff check .
ruff format --check .
mypy src
```

## Build Python distributions

```powershell
python -m pip install build
python -m build
```

The `dist/` directory should contain a `.whl` file and a `.tar.gz` source distribution. To verify wheel installation in a clean environment:

```powershell
py -3.12 -m venv .wheel-test
.\.wheel-test\Scripts\python.exe -m pip install dist\book_catalog-1.0.0-py3-none-any.whl
.\.wheel-test\Scripts\python.exe -c "import book_catalog; print(book_catalog.__version__)"
```

## Docker

Start Docker Desktop first.

```powershell
docker build -t book-catalog:1.0 .
docker run --rm -p 8000:8000 -e APP_ENV=production -e LOG_LEVEL=INFO -v book_catalog_data:/app/data book-catalog:1.0
```

The named volume keeps the SQLite database after the container stops. Visit `http://localhost:8000/health` and `http://localhost:8000/docs`.

Check container status and health:

```powershell
docker ps
docker inspect --format='{{json .State.Health}}' <container_id>
```

## CI/CD

`.github/workflows/ci.yml` runs on pushes to `main`, `master`, `develop`, pull requests, and manual dispatch. It installs the package, runs Ruff lint and formatting checks, mypy, pytest with coverage, builds wheel/sdist, checks the artifacts, and builds the Docker image.

## Project structure

```text
.
├── .github/workflows/ci.yml
├── src/book_catalog/
│   ├── __init__.py
│   ├── api.py
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── repositories.py
│   └── schemas.py
├── tests/
│   ├── conftest.py
│   └── test_api.py
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── LICENSE
├── README.md
└── pyproject.toml
```

## Demonstration checklist

1. Show the package metadata in `pyproject.toml`.
2. Run `pytest -v`, `ruff check .`, `ruff format --check .`, and `mypy src`.
3. Run `python -m build` and show both distribution files in `dist/`.
4. Build and start the Docker container with the named data volume.
5. Demonstrate `/health`, `/docs`, author/book creation, filtering, and statistics.
6. Show the latest successful run under the repository's GitHub Actions tab.

## Author

Karyna Boichuk — Software Engineering, variant 2 (Book Catalog).
