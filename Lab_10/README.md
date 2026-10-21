# Book Catalog (Варіант 2)

 Production-oriented версія проєкту "Система обліку книг" (Lab 10).

##  Опис
Система керування каталогом книг із підтримкою REST API, БД, лінтингу, автоматичного тестування, контейнеризації через Docker та CI/CD у GitHub Actions.

##  Основний функціонал
- Додавання та перегляд книг
- Пошук за автором (`/authors`, `/authors/{id}/books`)
- Фільтрація за роком видання
- Аналітика (найбільша книга, середня кількість сторінок)
- Перевірка стану системи (`GET /health`)

##  Налаштування та запуск

### Локальний запуск
1. Створіть та активуйте віртуальне середовище:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # або .venv\Scripts\activate  # Windows
   ```
2. Встановіть пакет у режимі розробки:
   ```bash
   pip install -e ".[dev]"
   ```
3. Скопіюйте файл налаштувань:
   ```bash
   cp .env.example .env
   ```
4. Запустіть сервер:
   ```bash
   uvicorn book_catalog.api:app --reload
   ```

### Перевірка якості коду та тестування
```bash
ruff check .
ruff format --check .
mypy src
pytest -v
```

### Запуск у Docker
1. Збірка образу:
   ```bash
   docker build -t book-catalog:latest .
   ```
2. Запуск контейнера:
   ```bash
   docker run --rm -p 8000:8000 --env-file .env book-catalog:latest
   ```

##  API Документація
Після запуску документація доступна за адресами:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Healthcheck: `http://localhost:8000/health`
