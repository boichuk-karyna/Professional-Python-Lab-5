# Лабораторна робота №6 — Варіант 2: система обліку книг

Проєкт містить модель книги, каталог, конфігурацію, CSV-імпорт, JSON-експорт,
асинхронний зовнішній каталог і unit/integration tests.

## Встановлення

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
python -m pip install -e ".[test]"
```

Linux/macOS:
```bash
source .venv/bin/activate
python -m pip install -e ".[test]"
```

## Запуск тестів

```bash
python -m pytest -v
```

Звіт statement + branch coverage:
```bash
python -m pytest -v --cov=books --cov-branch --cov-report=term-missing --cov-report=html
```

HTML-звіт буде у `htmlcov/index.html`. Конфігурація задає мінімальний поріг
покриття 80%; фактичне покриття потрібно підтвердити запуском тестів локально.
