# Звіт до лабораторної роботи №7
## Робота з базами даних у Python

**Виконала:** Бойчук Карина  
**Варіант:** 2 — Система обліку книг

## 1. Мета роботи
Ознайомитися з організацією шару зберігання даних у Python, SQLite, SQL, DB-API, CRUD, транзакціями, ACID, Repository Pattern, SQLAlchemy ORM, Alembic і integration tests.

## 2. Постановка задачі
Реалізувати каталог книг із даними назва, автор, рік видання, кількість сторінок. Створити пов'язані таблиці `authors` і `books`; реалізувати CRUD авторів і книг, пошук за автором, фільтр за роком, найбільшу книгу, середню кількість сторінок, параметризований DB-API запит, атомарне додавання автора з книгами, міграцію ISBN та інтеграційні тести.

## 3. Предметна область і схема БД
Один автор може мати багато книг (one-to-many). `authors.id` та `books.id` — первинні ключі. `books.author_id` — зовнішній ключ на `authors.id` з каскадним видаленням.

- `authors`: `id INTEGER PK`, `name VARCHAR(150) NOT NULL UNIQUE`, `biography TEXT NULL`.
- `books`: `id INTEGER PK`, `title VARCHAR(250) NOT NULL`, `year INTEGER NOT NULL`, `pages INTEGER NOT NULL`, `author_id INTEGER FK NOT NULL`, `isbn VARCHAR(20) NULL UNIQUE` (додано міграцією).
- Обмеження: рік у діапазоні 0–2100, сторінки > 0.

## 4. Структура проєкту
Код розділений на `models.py` (ORM-моделі), `database.py` (engine і сесії), `repositories.py` (CRUD і запити), `services.py` (транзакційна бізнес-операція), `db_api.py` (прямий sqlite3 DB-API), `main.py` (демонстраційний запуск), `migrations/` (Alembic), `tests/` (інтеграційні тести).

## 5. SQL та параметризований запит
У `db_api.py` використано `sqlite3` та запит:
```sql
SELECT books.id, books.title, books.year, books.pages, authors.name
FROM books JOIN authors ON books.author_id = authors.id
WHERE authors.name = ?
ORDER BY books.title
```
Значення передається окремим параметром `(author_name,)`, тому дані не конкатенуються в SQL-рядок.

## 6. CRUD і Repository Pattern
`AuthorRepository` та `BookRepository` забезпечують Create, Read, Update, Delete. Пошук і фільтрація ізольовані в репозиторіях, тому бізнес-логіка не залежить від деталей зберігання.

## 7. Транзакції та ACID
`add_author_with_books()` додає автора й усі книги в одній транзакції. `flush()` отримує ID автора без commit. Успіх завершується `commit()`, будь-яка помилка викликає `rollback()` і повторно передається виклику.
- Atomicity: всі записи зберігаються разом або не зберігається жоден.
- Consistency: обмеження NOT NULL, UNIQUE, CHECK і FOREIGN KEY.
- Isolation: транзакційний механізм SQLite та окремі сесії.
- Durability: зафіксовані `commit()` зміни зберігаються у файлі БД.

## 8. Міграції
`0001_create_authors_books.py` створює таблиці без ISBN. `0002_add_isbn_to_books.py` додає nullable поле `isbn` та UNIQUE constraint. Команди: `alembic upgrade head`, `alembic current`, `alembic downgrade 0001`.

## 9. Integration tests
Тести використовують окрему SQLite in-memory базу, не торкаються робочої `books.db`. Перевіряються CRUD автора/книги, relationship author-books, пошук за автором, фільтр за роком, largest book, average pages, constraints, параметризований DB-API та rollback транзакції.

## 10. Запуск і перевірка
```bash
python -m pip install -e ".[test]"
pytest -v
python -m book_manager.main
alembic upgrade head
```

## 11. Висновок
У результаті реалізовано persistence layer для системи обліку книг на SQLite та SQLAlchemy ORM, два пов'язані об'єкти, Repository Pattern, CRUD, DB-API параметризований запит, транзакцію з commit/rollback, міграцію Alembic і integration tests.
