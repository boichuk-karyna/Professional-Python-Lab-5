# Lab 10 — Variant 2: Book Management

This project is based on the provided Lab_10 example structure and carries forward the user's previous book-management work from Lab_05 (reliable CSV import/export), Lab_07 (SQLite persistence/repositories), Lab_08 (REST API), and Lab_09 (analytics/profiling).

## Project layout
- `src/book_manager/` — REST API and book-management logic from Lab 08, with distinct analytics/profiling modules from Lab 09.
- `src/books/` — persistence implementation carried forward from Lab 07.
- `src/reliable_warehouse/` — reliable import/export/configuration modules carried forward from Lab 05.
- `tests/` — tests from the provided Lab 10 example.
- `benchmarks/` — benchmark entry point from the example.

## Run
Use the commands and dependency versions in `pyproject.toml`. Run tests from this directory with `python -m pytest`.

Note: the example archive contains several parallel warehouse implementations. They are retained to preserve the example's structure; the book-management code is added alongside them so previous coursework is not discarded.
