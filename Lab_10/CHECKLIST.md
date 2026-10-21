# Чекліст демонстрації Lab 10 — варіант 2

- [ ] Встановити пакет командою `python -m pip install -e ".[dev]"`.
- [ ] Запустити `pytest -v --cov=book_catalog`.
- [ ] Запустити `ruff check .` та `ruff format --check .`.
- [ ] Запустити `mypy src`.
- [ ] Зібрати wheel і sdist командою `python -m build`.
- [ ] Запустити API та відкрити `/docs`.
- [ ] Продемонструвати `/health`, `POST /books`, фільтрацію, `/authors` та `/books/statistics`.
- [ ] Побудувати Docker image і запустити контейнер з портом 8000.
- [ ] Показати workflow GitHub Actions і пояснити `.env.example` та відсутність секретів у Git.
