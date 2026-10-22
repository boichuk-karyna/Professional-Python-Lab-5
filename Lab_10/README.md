# Book Catalog Project

Проєкт системи обліку книг (`book-catalog`), виконаний відповідно до вимог Лабораторної роботи №10.

## Структура
- `src/book_catalog`: Основний сирцевий код проєкту (`src-layout`).
- `tests`: Набір автотестів (`pytest`).
- `.github/workflows`: Конфігурація CI/CD pipeline (GitHub Actions).
- `Dockerfile`: Контейнеризація застосунку.

## Запуск
1. Встановлення залежностей: `pip install -e ".[dev]"`
2. Запуск тестів: `pytest`
3. Запуск застосунку: `book-catalog`
4. Збірка пакета: `python -m build`
5. Збірка Docker: `docker build -t book-catalog:1.0 .`
