# Lab 07 — Варіант 2: Система обліку книг

Проєкт реалізує persistence layer каталогу книг на SQLite + SQLAlchemy 2.x.

## Можливості
- таблиці `authors` і `books`, зв'язок one-to-many, PK/FK, UNIQUE/CHECK constraints;
- повний CRUD для авторів і книг через `AuthorRepository` та `BookRepository`;
- пошук за автором через SQLAlchemy та окремо DB-API (`sqlite3`) з параметризованим запитом;
- фільтр за роком, книга з найбільшою кількістю сторінок, середня кількість сторінок;
- транзакційне додавання автора разом із набором книг: `commit()` при успіху, `rollback()` при помилці;
- Alembic migration, що додає `isbn` до `books`;
- integration tests з окремою in-memory SQLite базою.

## Запуск (Windows / PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -e ".[test]"
py -m pytest -v
py -m book_manager.main
```
Якщо запускаєте через Git Bash:
```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install -e ".[test]"
pytest -v
python -m book_manager.main
```

## Міграції
У корені проєкту:
```bash
alembic upgrade head
alembic current
alembic downgrade 0001
alembic upgrade head
```
`alembic upgrade head` створює схему з міграцій: перша створює `authors` і `books` без `isbn`, друга додає `isbn`. Прикладова БД `books.db` створюється у корені проєкту.

## Структура
```text
src/book_manager/
  __init__.py
  database.py
  models.py
  repositories.py
  services.py
  db_api.py
  main.py
migrations/
  env.py
  script.py.mako
  versions/
    0001_create_authors_books.py
    0002_add_isbn_to_books.py
tests/
  conftest.py
  test_repositories.py
  test_services.py
  test_db_api.py
alembic.ini
```

## ACID
- **Atomicity:** `add_author_with_books()` або додає автора й усі книги, або відкочує всі зміни.
- **Consistency:** NOT NULL, UNIQUE та CHECK обмеження підтримують коректність даних; зовнішній ключ перевіряється SQLite.
- **Isolation:** SQLite керує паралельним доступом до транзакцій; окремі сесії не повинні ділити незавершені зміни.
- **Durability:** після успішного `commit()` зміни збережені в БД.

## Схема
`authors(id PK, name UNIQUE, biography)` 1 ─── * `books(id PK, title, year, pages, isbn, author_id FK -> authors.id)`

## Примітка
Цей архів містить завершений автономний проєкт варіанта 2 на основі вимог методички. Якщо викладач вимагає буквально продовжити ваш конкретний репозиторій Lab_01, перенесіть його попередню бізнес-логіку до цього persistence layer.
