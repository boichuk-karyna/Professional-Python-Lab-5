# Professional Python — Lab 10, Variant 2: Book Catalog

Production-oriented continuation of the book-catalog project from Labs 7–9. It preserves the SQLAlchemy persistence layer, FastAPI REST endpoints, asynchronous HTTPX workflow, and catalog operations while adding packaging, environment-based configuration, Docker, quality checks, and GitHub Actions CI.

## Requirements

- Python 3.11 or newer
- Docker (for container execution)
- Git (for CI workflow)

## Install locally

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
```

If PowerShell activation is blocked, run `.venv\Scripts\python.exe -m pip install -e ".[dev]"`.

### Git Bash / Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
cp .env.example .env
```

Configuration is read from environment variables. `.env.example` is a template only; `.env` is ignored by Git. The application has safe defaults and does not require secrets for local SQLite use.

## Run the API

```bash
book-manager
```

Or run it directly:

```bash
uvicorn book_manager.api:app --app-dir src --host 127.0.0.1 --port 8000
```

Open Swagger at <http://127.0.0.1:8000/docs>, ReDoc at <http://127.0.0.1:8000/redoc>, and health at <http://127.0.0.1:8000/health>.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/books` | List, filter, sort, and paginate books |
| POST | `/books` | Create a book; create its author when needed |
| GET | `/books/{book_id}` | Get one book |
| PATCH | `/books/{book_id}` | Partially update a book |
| DELETE | `/books/{book_id}` | Delete a book |
| GET | `/authors` | List authors |
| POST | `/authors` | Create an author |
| GET | `/authors/{author_id}/books` | List an author's books |
| GET | `/books/statistics` | Catalog statistics |
| POST | `/authors/batch-books` | Concurrently request books for several authors |

Example `POST /books` JSON:

```json
{
  "title": "Кобзар",
  "author_name": "Тарас Шевченко",
  "year": 1840,
  "pages": 320,
  "isbn": "9786170000001"
}
```

Example filter: `/books?author_name=Шевченко&year_from=1800&year_to=1900&page=1&page_size=10&sort_by=pages&order=desc`.

## Configuration

| Variable | Default | Purpose |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./books.db` | SQLAlchemy connection URL |
| `APP_ENV` | `development` | Environment label |
| `LOG_LEVEL` | `INFO` | Logging level |
| `HTTP_TIMEOUT` | `3.0` | External HTTP timeout in seconds |
| `HTTP_RETRIES` | `3` | Maximum HTTP attempts |
| `HTTP_CONCURRENCY` | `3` | Concurrent external requests |
| `API_BASE_URL` | `http://127.0.0.1:8000` | API URL used by batch requests |

Do not commit `.env`, passwords, tokens, or real API keys. Supply production secrets through the deployment environment or a secret manager.

## Tests and code quality

```bash
pytest -v
ruff check src tests
ruff format src tests
mypy src
pytest --cov=book_manager --cov-branch --cov-report=term-missing
```

Build both distribution formats:

```bash
python -m build
```

The `dist/` directory should contain a `.whl` and a `.tar.gz` source distribution.

## Docker

Build the image:

```bash
docker build -t book-manager:1.0 .
```

Run the API with a persistent named volume:

```bash
docker volume create book-manager-data
docker run --rm -p 8000:8000 -v book-manager-data:/app/data book-manager:1.0
```

The container uses a non-root user, a slim Python image, a health check, and a persistent SQLite location. To override settings:

```bash
docker run --rm -p 8000:8000 \
  -e APP_ENV=production \
  -e LOG_LEVEL=INFO \
  -v book-manager-data:/app/data \
  book-manager:1.0
```

For SQLite persistence, the container defaults to `sqlite:////app/data/books.db`. A mounted volume preserves the database when the container is removed.

## Continuous Integration

`.github/workflows/ci.yml` runs on pushes, pull requests, and manual dispatch. It installs the package, runs Ruff lint and formatting checks, runs mypy, executes tests with branch coverage, builds wheel and sdist, verifies both artifacts, and builds the Docker image.

## Architecture

`FastAPI → Pydantic schemas → service layer → repository layer → SQLAlchemy ORM → SQLite`

This is the Lab 10 production packaging of the Variant 2 book catalog; it is not a replacement with a different business domain.
