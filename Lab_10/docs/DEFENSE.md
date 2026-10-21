# Lab 10 — preparation for defense (Variant 2)

## Demonstration order

1. Show `pyproject.toml`: package metadata, runtime/dev dependencies and console script.
2. Explain `.env.example`, `config.py` and why `.env` is excluded from Git.
3. Run `pytest -v` and show the test summary.
4. Run `ruff check src tests benchmarks` and `mypy src/book_catalog --ignore-missing-imports`.
5. Run `python -m build` and show the wheel and sdist in `dist/`.
6. Build and run the Docker image; show `docker ps` and `http://127.0.0.1:8000/health`.
7. Open `/docs` and demonstrate creating/listing a book.
8. Show `.github/workflows/ci.yml` and a successful Actions run after pushing the repository.
9. Explain persistent storage with the `/app/data` Docker volume and the non-root runtime user.
10. Show the Lab 5–6 `reliable_importer` package and the Lab 7 Alembic migration.
11. Show Lab 9 benchmark/profile code as the performance extension.

## Commands

```powershell
python -m pip install -e ".[dev]"
pytest -v
ruff check .
ruff format --check .
mypy src
python -m build
docker build -t book-catalog:1.0 .
docker volume create book-catalog-data
docker run --rm -p 8000:8000 -v book-catalog-data:/app/data book-catalog:1.0
```

Do not claim GitHub Actions or Docker passed until the workflow has actually run in your GitHub repository and the image has been built locally.
