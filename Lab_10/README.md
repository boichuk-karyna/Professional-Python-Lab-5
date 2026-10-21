# Professional Python — Lab 10, Variant 2
## Book Manager: production packaging, Docker and CI/CD

This is the production-oriented continuation of the **Book Catalog / Book Manager** project from Labs 1–9. It retains the Lab 8 FastAPI + SQLAlchemy + SQLite REST API and carries forward Lab 9 performance work (NumPy statistics, thread/process experiments, caching and profiling) as separate modules so that the REST API's database models do not conflict with the performance experiment data model.

## Included requirements

- Installable package using `pyproject.toml`, version `1.0.0`, console script `book-manager`.
- Build configuration for both wheel and source distribution (`python -m build`).
- Environment-based configuration via Pydantic Settings; `.env.example` is safe to commit and `.env` is ignored.
- REST API, database persistence, validation, error handling, `/health`, Swagger docs.
- Unit/API tests plus Lab 9 optimization and parallelism tests.
- Ruff lint, mypy type checking, pytest coverage and package build in GitHub Actions.
- Multi-stage Dockerfile, non-root runtime user, SQLite data volume and Docker healthcheck.

## Requirements

Python 3.11+ for local development. Docker Desktop is required only for container build/run. The CI workflow checks Python 3.11 and 3.12.

## Setup on Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
```

If PowerShell blocks activation, run `.\.venv\Scripts\python.exe -m pip install -e ".[dev]"` and use that same interpreter for the commands below.

## Run the API

```powershell
uvicorn book_manager.main:app --reload
```

- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>
- Health: <http://127.0.0.1:8000/health>

The default SQLite database is `data/books.db`. Override it with `DATABASE_URL` in `.env` or the process environment. In Docker, use a volume mounted at `/app/data` so the database survives container replacement.

## REST endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API status and docs path |
| GET | `/health` | Container/monitoring health check |
| GET | `/books` | Filter, sort and paginate books |
| GET | `/books/{book_id}` | Get one book |
| POST | `/books` | Create book; create author when needed |
| PATCH | `/books/{book_id}` | Update a book |
| DELETE | `/books/{book_id}` | Delete a book |
| GET | `/books/statistics` | Total books, average pages and largest book |
| GET | `/authors` | List authors |
| POST | `/authors` | Create author |
| GET | `/authors/{author_id}/books` | List an author's books |
| POST | `/authors/batch-books` | Async external requests with concurrency limit, timeout and retry |

Example request to `POST /books`:

```json
{
  "title": "Кобзар",
  "author_name": "Тарас Шевченко",
  "year": 1840,
  "pages": 320,
  "isbn": "9786170000001"
}
```

## Tests and quality checks

```powershell
pytest -v
pytest --cov=book_manager --cov-report=term-missing
ruff check src tests benchmarks
mypy src/book_manager --ignore-missing-imports
```

## Build Python distributions

```powershell
python -m build
Get-ChildItem dist
```

Expected outputs: one `.whl` and one `.tar.gz` source distribution in `dist/`.

## Docker

Build the image:

```powershell
docker build -t book-manager:1.0 .
```

Run it with persistent SQLite storage:

```powershell
docker volume create book-manager-data
docker run --rm --name book-manager -p 8000:8000 -v book-manager-data:/app/data book-manager:1.0
```

Or pass configuration explicitly (do not pass real secrets in source code or commit them):

```powershell
docker run --rm -p 8000:8000 -v book-manager-data:/app/data -e APP_ENV=production -e LOG_LEVEL=INFO book-manager:1.0
```

## Lab 9 performance experiments

The performance module stays available independently of the REST API models:

```powershell
python benchmarks/benchmark.py 10000
```

It compares Python and NumPy statistics and sequential/thread/process CPU workloads, writes `results/benchmark_results.csv`, and records a `cProfile` snapshot. Timing values depend on the machine and are not hard-coded as measured results.

## GitHub Actions

The workflow at `.github/workflows/ci.yml` runs on every push and pull request. It installs the package, checks lint and types, runs tests with coverage, builds wheel/sdist, verifies wheel installation and builds the Docker image on Python 3.11 and 3.12.

## Security and release checklist

- [ ] Keep `.env` and real credentials out of Git.
- [ ] Keep `.env.example` free of real keys/passwords.
- [ ] `pytest` passes locally.
- [ ] Ruff and mypy complete without errors.
- [ ] `python -m build` creates wheel and sdist.
- [ ] `docker build` succeeds and `/health` returns `{"status":"ok"}`.
- [ ] GitHub Actions is green after pushing the project.
- [ ] Create a release tag only after the checks pass, for example `v1.0.0`.

## Architecture

`HTTP client → FastAPI → service layer → repository layer → SQLAlchemy → SQLite`

The API and database layers come from Lab 8; the performance and profiling experiments from Lab 9 remain under `analytics.py`, `parallel.py`, `profiling.py`, `performance_models.py` and `performance_catalog.py`.
