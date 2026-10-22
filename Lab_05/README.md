# Лабораторна робота №5

## Тема
Обробка помилок, файли та серіалізація.

## Варіант
2 — імпорт та експорт системи обліку книг.

## Мета
Розробити надійний модуль імпорту, перевірки,
обробки та експорту даних про книги.

## Поля книги
- isbn
- title
- author
- year
- pages

## Використані технології
- Python
- pathlib
- dataclasses
- exceptions
- logging
- CSV
- JSON
- YAML
- context managers
- streaming I/O
- atomic output

## Запуск

```bash
python -m pip install -e .
python -m reliable_importer.main