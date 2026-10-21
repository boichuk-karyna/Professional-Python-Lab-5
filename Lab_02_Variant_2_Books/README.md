# Лабораторна робота №2 — Варіант 2

**Тема:** Структури даних та функціональна декомпозиція  
**Варіант 2:** Аналіз системи обліку книг.

## Структура

- `src/data_processor/data.py` — вхідні дані та tuple полів;
- `processors.py` — set/dict/list comprehensions, пошук, групування, Counter, defaultdict, closure;
- `analytics.py` — агрегації, lambda, `*args`, `**kwargs`;
- `decorators.py` — decorator вимірювання часу;
- `benchmark.py` — порівняння list search та dict search;
- `main.py` — демонстрація роботи.

## Запуск

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt
python -m data_processor.main
```

Якщо запускати з кореня проєкту:

```bash
set PYTHONPATH=src
python -m data_processor.main
```

Linux/macOS:

```bash
PYTHONPATH=src python -m data_processor.main
```
