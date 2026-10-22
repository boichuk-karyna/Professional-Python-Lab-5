# Book Manager — Лабораторна робота №10, варіант 2

Production-oriented REST API для каталогу книг та авторів. Проєкт використовує FastAPI, SQLAlchemy, Pydantic і SQLite, має змінні середовища, тести, Dockerfile та GitHub Actions.

## Функціональність
- Створення, перегляд, редагування та видалення книг.
- Облік авторів і зв’язку «автор — книги».
- Валідація назви, автора, року видання, кількості сторінок та ISBN.
- Пошук/фільтрація за автором і діапазоном років, сортування та пагінація.
- Статистика каталогу: кількість книг, середня кількість сторінок і найбільша книга.
- Імпорт книг із CSV та експорт каталогу у JSON.
- Асинхронне отримання даних зовнішнього API з timeout, retry та обмеженням конкурентності.
- Перевірка стану сервісу через `GET /health`.

## Встановлення
Потрібен Python 3.11+.

```bash
python -m venv .venv
```

Windows PowerShell:
```powershell
.venv\\Scripts\\Activate.ps1
```

Linux/macOS:
```bash
source .venv/bin/activate
```

```bash
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

## Конфігурація
Скопіюйте `.env.example` у `.env` і за потреби змініть параметри. Застосунок читає змінні середовища:

- `DATABASE_URL` — URL бази даних; типове значення `sqlite:///./books.db`.
- `APP_ENV` або `ENVIRONMENT` — середовище запуску.
- `LOG_LEVEL` — рівень логування (`DEBUG`, `INFO`, `WARNING`, `ERROR`).
- `HTTP_TIMEOUT`, `HTTP_RETRIES`, `HTTP_CONCURRENCY`, `API_BASE_URL` — параметри запитів до зовнішнього API.

Не зберігайте паролі, токени або ключі доступу в коді чи Git.

## Запуск локально
```bash
uvicorn book_manager.api:app --app-dir src --reload
```
Документація API: http://127.0.0.1:8000/docs

## API
- `GET /health` — health check.
- `GET /` — інформація про сервіс.
- `GET /books` — список книг; підтримує `author_name`, `year_from`, `year_to`, `page`, `page_size`, `sort_by`, `order`.
- `POST /books` — створення книги.
- `GET /books/{book_id}` — отримання книги за ID.
- `PATCH /books/{book_id}` — оновлення полів книги.
- `DELETE /books/{book_id}` — видалення книги.
- `GET /books/statistics` — статистика каталогу.
- `POST /books/import.csv` — імпорт CSV із заголовками `title,author_name,year,pages,isbn` (тіло запиту з `Content-Type: text/csv`).
- `GET /books/export.json` — експорт каталогу в JSON.
- Доступні також маршрути для авторів; повний перелік показаний у `/docs`.

Приклад створення книги:
```json
{
  "title": "Приклад книги",
  "author_name": "Іван Франко",
  "year": 1900,
  "pages": 240,
  "isbn": null
}
```

## Тести та перевірки
```bash
pytest -v
ruff check src tests
ruff format --check src tests
mypy src
python -m build
```

## Docker
```bash
docker build -t book-manager:1.0 .
docker run --rm -p 8000:8000 -v book_data:/app/data book-manager:1.0
```
SQLite-файл зберігається у `/app/data/books.db`, який підключено до persistent volume `book_data`.

## CI/CD
GitHub Actions запускає перевірки стилю, форматування, статичної типізації, pytest, збірку Python-пакетів та Docker image під час push і pull request.

## Сценарій демонстрації
1. Відкрити `/docs`.
2. Перевірити `GET /health`.
3. Створити кілька книг через `POST /books`.
4. Перевірити список, фільтрацію за роком та автором.
5. Переглянути `GET /books/statistics`.
6. Спробувати некоректні значення, щоб побачити валідацію.

## Продовження попередніх лабораторних робіт

ЛР №10 розвиває той самий предметний проєкт — каталог книг та авторів. Напрацювання попередніх етапів зібрані в одній актуальній реалізації, а не запускаються як окремі непов'язані програми:

| Етап | Як представлений у проєкті |
|---|---|
| ЛР №1 | Пакет `src/book_manager`, точка входу та конфігурація проєкту |
| ЛР №2–4 | Моделі, сервіси, репозиторії, схеми Pydantic і розділення відповідальностей |
| ЛР №5 | Імпорт CSV (`POST /books/import.csv`) та JSON-серіалізація (`GET /books/export.json`) |
| ЛР №6 | Pytest-тести для API, валідації, помилок і файлового імпорту/експорту |
| ЛР №7 | SQLAlchemy-моделі та репозиторії для книг і авторів |
| ЛР №8 | REST API на FastAPI та автоматична документація `/docs` |
| ЛР №9 | Бенчмарк `benchmarks/benchmark.py` для вимірювання часу запиту |
| ЛР №10 | `pyproject.toml` для пакування, `Dockerfile` і GitHub Actions CI |

Цей архів містить інтегровану поточну версію застосунку, а не копії всіх попередніх каталогів лабораторних робіт.
