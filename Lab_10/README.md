# Book Catalog — Lab 10, Variant 2

Production-oriented version of the book catalog developed in Labs 1–9. The application uses FastAPI, Pydantic, SQLAlchemy and SQLite, with package distribution, environment-based configuration, Docker, automated tests and GitHub Actions.

## Features

- Create, list, update and delete books.
- Search books by author and filter by publication year.
- List authors and view books by author.
- Calculate total books, average page count and the largest book.
- Health check at `GET /health`.
- SQL pagination and sorting; indexed title/year/author fields; aggregate statistics are calculated in SQL.
- Async batch author lookup retained from Lab 8.
- Configuration through environment variables; secrets are not stored in source code.

## Requirements

- Python 3.11+ (CI and Docker use Python 3.12)
- Docker Desktop, for container execution

## Install locally (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
```

Edit `.env` only for local settings. Never commit `.env`; it is excluded by `.gitignore`.

## Configuration

| Variable | Default | Purpose |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./data/books.db` | SQLAlchemy database URL |
| `APP_ENV` | `development` | Application environment, also accepts `ENVIRONMENT` |
| `LOG_LEVEL` | `INFO` | Logging level |
| `API_BASE_URL` | Provided by external API module | Base URL used by the async author lookup |

For example, in PowerShell:

```powershell
$env:APP_ENV = "development"
$env:LOG_LEVEL = "INFO"
$env:DATABASE_URL = "sqlite:///./data/books.db"
```

Database passwords, tokens and API keys must be supplied through environment variables or GitHub Actions Secrets. Do not put real secrets in `.env.example`, Python files, the Dockerfile or README.

## Run locally

```powershell
python -m book_catalog.main
```

The API starts at `http://127.0.0.1:8000`.

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Health: http://127.0.0.1:8000/health

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/books` | List/search/filter books; pagination and sorting |
| POST | `/books` | Add a book |
| GET | `/books/{book_id}` | Get a book |
| PATCH | `/books/{book_id}` | Update a book |
| DELETE | `/books/{book_id}` | Delete a book |
| GET | `/books/statistics` | Total, average pages and largest book |
| GET | `/authors` | List authors |
| POST | `/authors` | Add an author |
| GET | `/authors/{author_id}/books` | List books by author |
| POST | `/authors/batch-books` | Async lookup for several author IDs |
| GET | `/health` | Health check |

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

Example filtering: `GET /books?author_name=Шевченко&year_from=1800&year_to=1900&page=1&page_size=10&sort_by=pages&order=desc`.

## Tests and quality checks

```powershell
pytest --cov=book_catalog --cov-branch --cov-report=term-missing
ruff check .
ruff format --check .
mypy src
```

## Build package distributions

```powershell
python -m pip install build
python -m build
Get-ChildItem dist
```

The `dist` directory should contain a `.whl` wheel and a `.tar.gz` source distribution. To verify the wheel in a clean environment:

```powershell
py -m venv .venv-wheel-check
.\.venv-wheel-check\Scripts\python.exe -m pip install dist\book_catalog-1.0.0-py3-none-any.whl
.\.venv-wheel-check\Scripts\python.exe -c "import book_catalog; print(book_catalog.__file__)"
```

## Docker

Build the image:

```powershell
docker build -t book-catalog:1.0 .
```

Run with persistent SQLite storage and environment variables:

```powershell
docker run --rm -p 8000:8000 `
  -e APP_ENV=production `
  -e LOG_LEVEL=INFO `
  -e DATABASE_URL=sqlite:////app/data/books.db `
  -v book_catalog_data:/app/data `
  book-catalog:1.0
```

Check `http://localhost:8000/health`. The container has a Docker `HEALTHCHECK`; the database file is stored in the named volume so it can survive container removal.

## CI/CD

`.github/workflows/ci.yml` runs on pushes to `main`/`develop` and on pull requests. It installs the project, runs Ruff lint and format checks, mypy, tests with branch coverage, builds wheel/sdist, verifies distribution artifacts and builds the Docker image.

## Project structure

```text
Lab_10/
├── .github/workflows/ci.yml
├── src/book_catalog/
│   ├── api.py
│   ├── database.py
│   ├── external_api.py
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
├── LICENSE
├── pyproject.toml
└── README.md
```

## Demo scenario

1. Start the application and open `/docs`.
2. Call `GET /health` and confirm `status` is `ok`.
3. Create an author or create a book using `POST /books`.
4. Call `GET /books`, try author/year filters, and inspect `GET /books/statistics`.
5. Run pytest, build the wheel/sdist and Docker image.
6. Push the project to GitHub and show the successful CI workflow.
