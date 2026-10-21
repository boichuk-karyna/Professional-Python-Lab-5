# Звіт до лабораторної роботи №10

**Тема:** Production Python: Docker, CI/CD та захист проєкту  
**Варіант:** 2 — система обліку книг  
**Виконав(ла):** Бойчук Карина

## Мета роботи

Підготувати Python-проєкт до production-oriented використання: оформити пакет, налаштувати конфігурацію через змінні середовища, створити Dockerfile, налаштувати CI/CD, автоматичні тести та документацію.

## Короткий опис

Розроблено Book Catalog — REST API для обліку книг. Книга має назву, автора, рік видання та кількість сторінок. Реалізовано додавання, перегляд, редагування й видалення книг, пошук за автором і назвою, фільтрацію за роком, список авторів, статистику каталогу та endpoint перевірки стану `/health`.

## Структура проєкту

Проєкт використовує `src-layout`. Пакет `book_catalog` містить API, налаштування, моделі, схеми, репозиторій і сервісний рівень. Каталог `tests` містить unit та integration тести. Файли Docker і GitHub Actions забезпечують контейнеризацію та автоматичні перевірки.

## Реалізовані production-вимоги

- `pyproject.toml` із метаданими та залежностями.
- Побудова wheel і sdist через `python -m build`.
- Налаштування `DATABASE_URL`, `APP_ENV`, `LOG_LEVEL` через environment variables.
- `.env.example`; `.env` і файли бази виключені через `.gitignore`.
- Dockerfile, `.dockerignore`, persistent volume та health check.
- GitHub Actions: Ruff lint/format, mypy, pytest, package build, Docker build.
- README з інструкціями запуску, API та сценарієм демонстрації.

## Команди перевірки

```text
python -m pip install -e ".[dev]"
pytest -v
ruff check .
ruff format --check .
mypy src
python -m build
docker build -t book-catalog:1.0 .
```

Фактичні результати виконання команд і скриншоти слід додати після запуску проєкту на комп'ютері та в GitHub Actions.

## Висновок

Під час лабораторної роботи було підготовлено систему обліку книг до production-oriented використання. Проєкт має пакетну структуру, конфігурацію через змінні середовища, REST API, тести, Dockerfile та workflow GitHub Actions. Документація описує встановлення, запуск, перевірку й демонстрацію застосунку.
