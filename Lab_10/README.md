# Book Catalog — Lab 10, Variant 2

Production-oriented REST API for a book catalog. The application uses a `src` layout, FastAPI, SQLite persistence, environment-based configuration, packaging, Docker, tests and GitHub Actions.

## Variant 2 features
- Add books with title, author, publication year and page count.
- List books and search by author (`GET /books?author=tolkien`).
- Filter by year (`GET /books?year=1965`).
- List authors and retrieve books by author ID.
- Find the book with the largest page count.
- Calculate average page count.
- Health endpoint (`GET /health`).

## Requirements
Python 3.11+; Docker is optional for container execution.

## Install and run locally
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
Copy-Item .env.example .env
uvicorn book_catalog.api:app --reload
```
Open `http://localhost:8000/docs` for interactive Swagger documentation and `http://localhost:8000/health` for health status.

## Configuration
Settings are read from environment variables and optionally `.env`: `APP_NAME`, `ENVIRONMENT`, `DATABASE_URL`, `LOG_LEVEL`, `API_KEY`. `.env` is ignored by Git. Never put real passwords, tokens or credentials in source code or commit them. `API_KEY` is reserved for future integrations and is not used as an authentication mechanism in this version.

Default database: `sqlite:///./data/books.db`. For Docker, the database is stored at `/app/data/books.db`.

PowerShell example:
```powershell
$env:ENVIRONMENT="production"
$env:LOG_LEVEL="INFO"
uvicorn book_catalog.api:app --host 0.0.0.0 --port 8000
```

## API
| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Health status and environment |
| POST | `/books` | Add a book |
| GET | `/books` | List books; optional `author` and `year` filters |
| GET | `/books/statistics/largest` | Book with the most pages |
| GET | `/books/statistics/average-pages` | Average pages and book count |
| GET | `/authors` | List authors |
| GET | `/authors/{id}/books` | Books by author ID |

Example request body for `POST /books`:
```json
{"title":"The Hobbit","author":"J. R. R. Tolkien","year":1937,"pages":310}
```

## Tests and quality checks
```powershell
pytest -v
ruff check .
ruff format --check .
mypy src
python -m build
```

To verify wheel installation in a clean environment after building:
```powershell
python -m venv wheel_env
.\wheel_env\Scripts\python -m pip install dist\book_catalog-1.0.0-py3-none-any.whl
.\wheel_env\Scripts\python -c "import book_catalog; print(book_catalog.__version__)"
```

## Docker
```powershell
docker build -t book-catalog:1.0 .
docker volume create book_catalog_data
docker run --rm -p 8000:8000 -e ENVIRONMENT=production -e LOG_LEVEL=INFO -v book_catalog_data:/app/data book-catalog:1.0
```
Then check `http://localhost:8000/health`. The volume keeps SQLite data when the container is removed. Do not pass secrets in the Dockerfile; use environment variables or a secure secret manager.

## CI/CD
`.github/workflows/ci.yml` runs on push to `main`/`develop` and pull requests. It executes Ruff lint and format checks, mypy, pytest, wheel/sdist build and Docker image build.

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
│   └── repositories.py
├── tests/
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── LICENSE
├── README.md
└── pyproject.toml
```

## Demonstration scenario
1. Start the API and open `/docs`.
2. Add two books with `POST /books`.
3. Search by author and filter by year with `GET /books`.
4. Open `/authors`, then `/authors/{id}/books`.
5. Demonstrate largest-book and average-pages endpoints.
6. Show `/health`, run tests, build the package and build/run the Docker image.
