# Book Catalog — Лабораторна робота №10, варіант 2

Production-oriented версія системи обліку книг, що продовжує предметну область попередніх лабораторних робіт. Основний пакет — `book_catalog` (distribution name: `book-catalog`). Збережено окремі вихідні дерева попередніх лабораторних у `src/previous_labs/`, щоб не втратити їхні файли та не перезаписати модулі з однаковими назвами.

## Можливості

- додавання та перегляд книг;
- пошук книг за автором;
- фільтрація за роком, сортування та посторінковий перегляд;
- облік авторів та отримання книг автора;
- статистика книг, включно з найбільшою книгою та середньою кількістю сторінок;
- REST API на FastAPI та документація OpenAPI;
- SQLAlchemy persistence layer і SQLite за замовчуванням;
- health endpoint `GET /health`;
- збережені модулі обробки даних, streaming, OOP, імпорту/експорту, тестування, persistence, REST API та profiling з попередніх робіт у `src/previous_labs/`.

## Вимоги

Python 3.11 або новіший. Для Docker-запуску потрібен Docker Engine/Desktop.

## Встановлення

```bash
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# Git Bash/Linux/macOS: source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

## Конфігурація

Скопіюйте `.env.example` у `.env` і змініть параметри за потреби. Файл `.env` ігнорується Git. Основні змінні:

- `DATABASE_URL` — URL бази даних; типове значення `sqlite:///./books.db`;
- `APP_ENV` або `ENVIRONMENT` — середовище виконання;
- `LOG_LEVEL` — рівень журналювання.

Не додавайте паролі, токени або інші секрети до source code, README, Dockerfile чи Git.

## Запуск локально

```bash
book-catalog
```

Альтернативно:

```bash
uvicorn book_catalog.api:app --reload
```

API: `http://127.0.0.1:8000`  
Swagger UI: `http://127.0.0.1:8000/docs`  
ReDoc: `http://127.0.0.1:8000/redoc`  
Health: `http://127.0.0.1:8000/health`

## API endpoints

- `GET /books` — список книг, фільтрація, сортування та пагінація;
- `POST /books` — додати книгу;
- `GET /authors` — список авторів;
- `GET /authors/{id}/books` — книги автора;
- `GET /health` — стан застосунку.

Точні параметри та моделі запитів задокументовані у Swagger UI.

## Тестування та перевірки якості

```bash
pytest -v
ruff check .
ruff format --check src/book_catalog tests
mypy src/book_catalog
python -m build
```

CI у `.github/workflows/ci.yml` автоматично запускає lint, format check, type checking, tests, package build та Docker build на push і pull request.

## Packaging

```bash
python -m build
```

У каталозі `dist/` мають з'явитися wheel (`.whl`) та source distribution (`.tar.gz`). Для перевірки wheel у чистому середовищі створіть окремий venv і встановіть wheel з `dist/`.

## Docker

```bash
docker build -t book-catalog:1.0 .
docker run --rm -p 8000:8000 \\
  -e APP_ENV=production \\
  -e LOG_LEVEL=INFO \\
  -e DATABASE_URL=sqlite:////app/data/books.db \\
  -v book_catalog_data:/app/data \\
  book-catalog:1.0
```

Після запуску перевірте `http://localhost:8000/health`. Volume `book_catalog_data` зберігає SQLite-файл між перезапусками контейнера.

## Структура проєкту

```text
Lab_10/
├── .github/workflows/ci.yml
├── benchmarks/
├── src/
│   ├── book_catalog/       # production package (Lab 10)
│   └── previous_labs/      # збережені src дерев ЛР 01–09
├── tests/
├── Dockerfile
├── .dockerignore
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

## Сценарій демонстрації

1. Встановити проєкт у virtual environment.
2. Запустити `book-catalog` і відкрити `/docs`.
3. Перевірити `GET /health`, додати автора та книгу, отримати список книг і книги автора.
4. Запустити `pytest`, Ruff, Mypy та `python -m build`.
5. Побудувати Docker image, запустити контейнер із volume та перевірити health endpoint.
6. Відкрити вкладку Actions у GitHub і продемонструвати результати CI pipeline.
