# Professional Python — Lab 10, Variant 2: Book Catalog

Production-oriented version of the book catalogue developed in earlier labs. The project retains the Variant 2 domain (books and authors) and extends the REST API from Lab 8 with packaging, environment-based configuration, Docker, CI/CD, and quality checks.

## Features

- CRUD operations for books and authors.
- Search by author, year-range filtering, pagination, and sorting.
- Book statistics: total number, average pages, and the largest book.
- Persistent SQLite storage by default; the database URL can be supplied through `DATABASE_URL`.
- Asynchronous batch author-book requests with timeout/retry/concurrency control.
- Health check at `GET /health`.
- Automated tests, linting, formatting, type checking, wheel/sdist build, and Docker image build.

## Requirements

Python 3.11 or newer. Docker is optional for container execution.

## Install locally (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
```

If PowerShell blocks virtual-environment activation, use `.\.venv\Scripts\python.exe -m pip install -e ".[dev]"` and run commands with that interpreter.

## Configuration

The application reads configuration from environment variables. `.env.example` contains safe local defaults; copy it to `.env` if desired.

| Variable | Purpose | Default |
|---|---|---|
| `DATABASE_URL` | SQLAlchemy connection URL | `sqlite:///./books.db` |
| `ENVIRONMENT` | Environment label | `development` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `HOST` / `PORT` | Server bind address and port | `0.0.0.0` / `8000` |
| `API_BASE_URL` | External API base URL used by async integration | `https://openlibrary.org` |

Do not commit `.env` or put passwords, tokens, API keys, or credentials in source code, README, Dockerfile, or Git history.

## Run the API

```powershell
python -m book_manager.cli
```

Or run from the source tree without installing the package:

```powershell
$env:PYTHONPATH = "src"
python -m book_manager.cli
```

Open Swagger UI at <http://127.0.0.1:8000/docs>, ReDoc at <http://127.0.0.1:8000/redoc>, and health check at <http://127.0.0.1:8000/health>.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Health status |
| `GET` | `/books` | List/search/filter books, pagination and sorting |
| `POST` | `/books` | Create a book (can create author by `author_name`) |
| `GET` | `/books/{book_id}` | Retrieve a book |
| `PATCH` | `/books/{book_id}` | Update a book |
| `DELETE` | `/books/{book_id}` | Delete a book |
| `GET` | `/books/statistics` | Catalog statistics |
| `GET` | `/authors` | List authors |
| `POST` | `/authors` | Create author |
| `GET` | `/authors/{author_id}/books` | List books by author |
| `POST` | `/authors/batch-books` | Asynchronously fetch books for multiple authors |

Example request for `POST /books`:

```json
{
  "title": "Кобзар",
  "author_name": "Тарас Шевченко",
  "year": 1840,
  "pages": 320,
  "isbn": "9786170000001"
}
```

Example query: `GET /books?author_name=Шевченко&year_from=1800&year_to=1900&page=1&page_size=10&sort_by=pages&order=desc`.

## Tests and code quality

```powershell
python -m pytest -v
ruff check src tests
ruff format --check src tests
mypy src
pytest --cov=book_manager --cov-branch --cov-report=term-missing
```

## Build distributable packages

```powershell
python -m build
```

The `dist/` directory contains the wheel and source distribution. To verify the wheel in a clean virtual environment:

```powershell
py -m venv .wheel-check
.\.wheel-check\Scripts\python.exe -m pip install dist\book_manager_production-1.0.0-py3-none-any.whl
.\.wheel-check\Scripts\python.exe -c "import book_manager; print('wheel import OK')"
```

## Docker

Build the image:

```powershell
docker build -t book-manager:1.0 .
```

Run with persistent database storage:

```powershell
docker volume create book_manager_data
docker run --rm -p 8000:8000 -v book_manager_data:/app/data book-manager:1.0
```

The image runs as a non-root user. The SQLite database is stored in `/app/data/books.db`, which is backed by the named volume. For custom settings, pass `-e DATABASE_URL=... -e ENVIRONMENT=production -e LOG_LEVEL=INFO`.

## CI/CD

`.github/workflows/ci.yml` runs on pushes and pull requests. It installs the package, checks Ruff lint and formatting, runs Mypy and pytest with branch coverage, builds wheel/sdist, and builds the Docker image.

## Demonstration checklist

1. Install the package and copy `.env.example` to `.env`.
2. Run the application and open `/docs`.
3. Create an author or create a book using `author_name`.
4. List books, test year filtering and sorting, and inspect `/books/statistics`.
5. Call `/health` and run the full test suite.
6. Build the package and Docker image; verify data persistence by restarting a container with the same volume.
