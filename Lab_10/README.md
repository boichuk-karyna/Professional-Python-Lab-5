# Book Catalog (Варіант 2) — Lab 10

Production-oriented версія проєкту "Система обліку книг" (Лабораторна робота №10).
Студентка: Бойчук Карина

## Опис
Система керування каталогом книг із підтримкою REST API, підключенням до бази даних (SQLAlchemy), конфігурацією через змінні середовища (`pydantic-settings`), перевіркою якості коду (`ruff`, `mypy`), автоматичним тестуванням (`pytest`), контейнеризацією (Docker + Healthcheck) та CI/CD pipeline у GitHub Actions.

## Основні функції та API
- `GET /health` — Healthcheck ендпоінт перевірки стану
- `GET /books` — Отримання всіх книг або фільтрація за автором/роком
- `POST /books` — Додавання нової книги в каталог
- `GET /authors` — Список усіх авторів із кількістю видань
- `GET /authors/{author_id}/books` — Отримання книг автора за ID або автором
- `GET /statistics` — Аналітика каталогу (загальна кількість, середня кількість сторінок, найбільша книга)

## Інструкція із запуску

### 1. Локальне встановлення
```bash
python -m venv .venv
source .venv/bin/activate  # Linux / macOS
# або .venv\Scripts\activate  # Windows

pip install -e ".[dev]"
cp .env.example .env
uvicorn book_catalog.api:app --reload
```

### 2. Запуск перевірок якості та тестів
```bash
ruff check .
ruff format --check .
mypy src
pytest -v
python -m build
```

### 3. Запуск у Docker
```bash
docker build -t book-catalog:latest .
docker run --rm -p 8000:8000 --env-file .env book-catalog:latest
```
Документація Swagger UI: http://localhost:8000/docs
