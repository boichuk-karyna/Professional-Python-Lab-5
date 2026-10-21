# Professional Python — Lab 8, Variant 2: Book Catalog REST API

Асинхронний REST API для обліку книг та авторів. Проєкт використовує FastAPI, Pydantic, SQLAlchemy і SQLite, HTTPX та asyncio. Дані зберігаються у `books.db` у корені проєкту (можна змінити через `DATABASE_URL`).

## Встановлення (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[test]"
```

Якщо PowerShell забороняє активацію, можна запускати `.\.venv\Scripts\python.exe -m pip install -e ".[test]"` і надалі використовувати той самий інтерпретатор.

## Запуск

```powershell
uvicorn book_manager.main:app --app-dir src --reload
```

Документація Swagger: http://127.0.0.1:8000/docs  
ReDoc: http://127.0.0.1:8000/redoc  
Перевірка стану: http://127.0.0.1:8000/health

## Тестування

```powershell
python -m pytest
```

## REST endpoints

| Метод | Endpoint | Призначення |
|---|---|---|
| GET | `/books` | Список книг; пошук автора, фільтр за роком, пагінація і сортування |
| GET | `/books/{book_id}` | Одна книга |
| POST | `/books` | Створити книгу; автора можна створити через `author_name` |
| PATCH | `/books/{book_id}` | Частково оновити книгу |
| DELETE | `/books/{book_id}` | Видалити книгу |
| GET | `/authors` | Список авторів |
| POST | `/authors` | Створити автора |
| GET | `/authors/{author_id}/books` | Книги автора |
| GET | `/books/statistics` | Кількість книг, середня кількість сторінок і книга з найбільшою кількістю сторінок |
| POST | `/authors/batch-books` | Паралельно отримати книги для кількох авторів із Task, gather, Semaphore, timeout і retry |
| GET | `/health` | Стан API |

### Приклад JSON для POST `/books`

```json
{
  "title": "Кобзар",
  "author_name": "Тарас Шевченко",
  "year": 1840,
  "pages": 320,
  "isbn": "9786170000001"
}
```

### Приклад query parameters

`GET /books?author_name=Шевченко&year_from=1800&year_to=1900&page=1&page_size=10&sort_by=pages&order=desc`

### Асинхронна агрегація

`POST /authors/batch-books` із тілом `{"author_ids":[1,2,3]}` викликає API для кожного автора паралельно. Кількість одночасних запитів обмежено `asyncio.Semaphore`; кожен HTTP-запит має timeout і retry з експоненційною затримкою. Базову URL-адресу можна змінити змінною `API_BASE_URL`.

## Архітектура

`HTTP client → FastAPI → Pydantic schemas → Service layer → Repository layer → SQLite`

- `models.py` — SQLAlchemy-моделі Author і Book.
- `schemas.py` — Pydantic-схеми та перевірка даних.
- `database.py` — налаштування SQLite та сесій.
- `repositories.py` — доступ до даних.
- `services.py` — бізнес-логіка.
- `api.py` — REST endpoints.
- `external_api.py` — асинхронні HTTPX-запити, Task, gather, timeout, retry, Semaphore.
- `tests/` — API та асинхронні тести.

## Примітка щодо скриншотів

Для звіту потрібно зробити власні скриншоти після запуску сервера: сторінки `/docs`, успішного `POST /books`, `GET /books` і результату `python -m pytest`. Зображення не підмінено макетами, щоб звіт відображав фактичне виконання на вашому комп'ютері.
