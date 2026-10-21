# Book Manager — Лабораторна робота №10, варіант 2

Production-oriented продовження навчального проєкту обліку книг із попередніх лабораторних робіт. Пакет зберігає модуль `book_manager` та архітектуру REST API + SQLAlchemy repository/service, а також додає packaging, Docker, CI, конфігурацію через environment variables і документацію.

## Функціональність варіанта 2

- додавання, перегляд, редагування та видалення книг;
- пошук за автором і фільтрація за роком видання;
- сортування та пагінація;
- список авторів і книги конкретного автора;
- статистика: кількість книг, середня кількість сторінок і найбільша книга;
- перевірка стану сервісу через `/health`;
- асинхронний пакетний запит книг за авторами з обмеженням конкурентності та повторними спробами;
- SQLAlchemy + SQLite за замовчуванням, URL БД задається через `DATABASE_URL`.

## Структура

```text
.
├── .github/workflows/ci.yml
├── docs/
├── src/book_manager/
│   ├── api.py
│   ├── database.py
│   ├── external_api.py
│   ├── models.py
│   ├── repositories.py
│   ├── schemas.py
│   ├── services.py
│   ├── analytics.py
│   ├── profiling.py
│   └── parallel.py
├── tests/
├── Dockerfile
├── pyproject.toml
└── README.md
```

## Локальний запуск (Windows)

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
uvicorn book_manager.api:app --reload
```

Відкрити Swagger: <http://127.0.0.1:8000/docs>. Перевірка стану: <http://127.0.0.1:8000/health>.

## Конфігурація

Скопіювати `.env.example` у `.env` і змінити значення за потреби. `DATABASE_URL` читається модулем БД; `API_BASE_URL`, `HTTP_TIMEOUT`, `HTTP_RETRIES`, `HTTP_CONCURRENCY` керують пакетним HTTP-запитом. Файл `.env` і файли бази виключені з Git. Для локального запуску змінні можна також встановлювати у PowerShell:

```powershell
$env:DATABASE_URL = "sqlite:///./books.db"
$env:HTTP_TIMEOUT = "3.0"
```

## Основні API маршрути

| Метод | Маршрут | Призначення |
|---|---|---|
| GET | `/health` | Перевірка працездатності |
| GET | `/books` | Список, пошук і фільтрація книг |
| POST | `/books` | Додати книгу; автора буде знайдено або створено |
| GET | `/books/{book_id}` | Отримати книгу за ID |
| PATCH | `/books/{book_id}` | Частково змінити книгу |
| DELETE | `/books/{book_id}` | Видалити книгу |
| GET | `/books/statistics` | Середня кількість сторінок і найбільша книга |
| GET | `/authors` | Список авторів |
| POST | `/authors` | Додати автора |
| GET | `/authors/{author_id}/books` | Книги автора |
| POST | `/authors/batch-books` | Асинхронний пакетний запит для авторів |

Приклад тіла для `POST /books`:

```json
{
  "title": "Кобзар",
  "author_name": "Тарас Шевченко",
  "year": 1840,
  "pages": 320,
  "isbn": "9786170000001"
}
```

Фільтри `GET /books`: `author_name`, `year_from`, `year_to`, `page`, `page_size`, `sort_by` (`title`, `year`, `pages`) і `order` (`asc`, `desc`).

## Тести та якість

```powershell
pytest -v
pytest --cov=book_manager --cov-branch --cov-report=term-missing
ruff check src tests
ruff format --check src tests
mypy src
```

## Packaging

```powershell
python -m build
```

У `dist/` буде створено wheel та source distribution (`.tar.gz`). Встановлення wheel перевіряється командою `python -m pip install --no-deps dist/*.whl`.

## Docker

```powershell
docker build -t book-manager-lab10 .
docker run --rm -p 8000:8000 -v book_manager_data:/data book-manager-lab10
```

Дані SQLite зберігаються у Docker volume `/data`. Swagger доступний на <http://localhost:8000/docs>.

## CI/CD

GitHub Actions запускає Ruff lint, перевірку форматування, mypy, pytest із coverage, збірку wheel/sdist і Docker image на `push`, `pull_request` та вручну. Реальні secrets і `.env` у репозиторій додавати не можна.

## Сценарій демонстрації

1. Запустити API та показати `/health` і `/docs`.
2. Додати дві книги різних авторів через `POST /books`.
3. Продемонструвати фільтр за автором і роком у `GET /books`.
4. Показати `/books/statistics` та `/authors/{id}/books`.
5. Запустити тести, збірку пакета та Docker build.
6. Показати успішний GitHub Actions workflow.
