# Лабораторна робота №7 — варіант 2: Система обліку книг

Проєкт демонструє persistence layer для каталогу книг: SQLite, SQLAlchemy ORM 2.x,
Repository Pattern, параметризований DB-API запит, транзакцію з `commit()`/`rollback()`,
Alembic-міграцію та integration tests з окремою in-memory тестовою базою.

## Структура

```text
Lab_07_Variant_2_Books/
├── alembic.ini
├── migrations/
│   ├── env.py
│   └── versions/
│       ├── 0001_create_authors_books.py
│       └── 0002_add_isbn_to_books.py
├── src/books/
│   ├── __init__.py
│   ├── database.py
│   ├── models.py
│   ├── repositories.py
│   ├── services.py
│   ├── db_api.py
│   └── main.py
├── tests/
│   ├── conftest.py
│   └── test_persistence.py
└── pyproject.toml
```

## Встановлення та запуск (Windows / PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[test]"
python -m pytest -v
python -m books.main
```

Якщо використовуєш Git Bash для активації середовища:
```bash
source .venv/Scripts/activate
```

## Міграції

Міграції створюють базову структуру, а наступна додає `isbn` до `books`:

```bash
alembic upgrade head
alembic current
alembic downgrade -1
alembic upgrade head
```

За замовчуванням локальна БД зберігається у `books.db` у корені проєкту.
Тестова БД окрема й існує лише в пам'яті (`sqlite:///:memory:`).

## Що реалізовано

- Таблиці `authors` та `books`, `PRIMARY KEY`, `FOREIGN KEY`, `UNIQUE` для ISBN.
- `AuthorRepository` і `BookRepository`: Create, Read, Update, Delete.
- One-to-many relationship: один автор має багато книг.
- Фільтр за роком, найбільша книга, середня кількість сторінок.
- DB-API пошук книг за автором з `?` placeholder.
- Транзакційне додавання автора та кількох книг: будь-яка помилка відкочує всю операцію.
- Alembic migration для поля `isbn`, із `upgrade()` та `downgrade()`.
- Integration tests для CRUD, зв'язку, фільтра, агрегатів, constraint і rollback.

## ACID коротко

- **Atomicity:** транзакція додає автора та всі книги або нічого; у разі помилки виконується rollback.
- **Consistency:** обмеження `NOT NULL`, `CHECK`, `UNIQUE` та зовнішній ключ підтримують коректність даних.
- **Isolation:** транзакційні зміни виконуються в межах окремої SQLAlchemy Session; SQLite керує блокуванням і видимістю транзакцій.
- **Durability:** після успішного `commit()` SQLite зберігає підтверджені зміни у файлі БД.

## SQL-еквівалент параметризованого пошуку

```sql
SELECT books.id, books.title, authors.name, books.year, books.pages, books.isbn
FROM books
JOIN authors ON authors.id = books.author_id
WHERE authors.name = ?;
```

Значення передається окремим параметром, а не вставляється у SQL-рядок, що допомагає уникнути SQL injection.
