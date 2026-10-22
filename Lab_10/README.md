# Book Catalog — Lab 10, Variant 2

Production-oriented version of the book catalog project. The application manages books and authors through a FastAPI REST API, persists data using SQLAlchemy, reads configuration from environment variables, and includes packaging, Docker, tests, linting, type checking, and GitHub Actions.

## Features

- Add books with title, author, publication year, and page count.
- Search books by author and filter by publication year.
- List authors and get books by author.
- Calculate average page count and identify the largest book.
- Health endpoint and interactive API documentation.
- SQLite by default; database URL configurable using `DATABASE_URL`.

## Project structure

```text
Lab_10/
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
│   └── test_api.py
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── pyproject.toml
└── README.md
```

## Requirements

Python 3.11+ and, for container execution, Docker.

## Local installation

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
Copy-Item .env.example .env
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Linux/macOS activation:

```bash
source .venv/bin/activate
cp .env.example .env
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Configuration

Supported environment variables:

| Variable | Purpose | Default |
|---|---|---|
| `APP_NAME` | API title | `Book Catalog` |
| `ENVIRONMENT` | Runtime environment | `development` |
| `DATABASE_URL` | SQLAlchemy database URL | `sqlite:///./data/books.db` |
| `LOG_LEVEL` | Logging level | `INFO` |

Copy `.env.example` to `.env` for local development. The real `.env` file is excluded by `.gitignore`. Do not commit passwords, tokens, API keys, or production credentials. In GitHub Actions, store real credentials in repository Actions secrets and pass them through the workflow environment only when needed.

## Run locally

```bash
uvicorn book_catalog.api:app --reload
```

Open:

- API docs: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Health: http://127.0.0.1:8000/health

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Health check |
| `POST` | `/books` | Add a book |
| `GET` | `/books` | List books |
| `GET` | `/books?author=Shevchenko` | Search by author |
| `GET` | `/books?year=1840` | Filter by year |
| `GET` | `/books/statistics` | Count, average pages, largest book |
| `GET` | `/authors` | List authors |
| `POST` | `/authors` | Add an author |
| `GET` | `/authors/{id}/books` | List an author's books |

Example request:

```json
{
  "title": "Кобзар",
  "author": "Тарас Шевченко",
  "year": 1840,
  "pages": 128
}
```

Example command:

```bash
curl -X POST http://127.0.0.1:8000/books \
  -H "Content-Type: application/json" \
  -d '{"title":"Кобзар","author":"Тарас Шевченко","year":1840,"pages":128}'
```

## Tests and quality checks

```bash
pytest -v
ruff check .
ruff format --check .
mypy src
```

Auto-format code with:

```bash
ruff format .
```

## Build wheel and source distribution

```bash
python -m pip install build
python -m build
```

Both artifacts are written to `dist/`: a `.whl` wheel and a `.tar.gz` source distribution.

To test the wheel in a clean environment, create another virtual environment and install the generated wheel:

```bash
python -m venv wheel-test
```

Windows:

```powershell
wheel-test\Scripts\python -m pip install dist\book_catalog-1.0.0-py3-none-any.whl
```

Linux/macOS:

```bash
wheel-test/bin/python -m pip install dist/book_catalog-1.0.0-py3-none-any.whl
```

## Docker

Build image:

```bash
docker build -t book-catalog:1.0 .
```

Run with persistent SQLite data and environment variables:

```bash
docker volume create book-catalog-data
docker run --rm -p 8000:8000 -e ENVIRONMENT=production -e LOG_LEVEL=INFO -e DATABASE_URL=sqlite:////app/data/books.db -v book-catalog-data:/app/data book-catalog:1.0
```

Then check `http://localhost:8000/health` and `http://localhost:8000/docs`.

Do not put secrets in the Dockerfile or bake `.env` into the image.

## CI/CD

`.github/workflows/ci.yml` runs on pushes and pull requests. It installs the project, runs Ruff lint and format checks, runs mypy and pytest, builds wheel/sdist, verifies the artifacts, and builds the Docker image.

## Demonstration checklist

1. Show the package layout and `pyproject.toml`.
2. Install dependencies and run `pytest -v`.
3. Run Ruff and mypy.
4. Build and show wheel/sdist in `dist/`.
5. Build the Docker image and start the container.
6. Demonstrate `/health`, `/docs`, creating a book, searching by author, filtering by year, and `/books/statistics`.
7. Show the GitHub Actions run and explain `.env.example`, `.gitignore`, and secrets handling.
