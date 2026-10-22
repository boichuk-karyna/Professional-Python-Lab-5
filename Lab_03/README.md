# Лабораторна робота №3 — Варіант 2

Тема: потокова обробка системи обліку книг.

Реалізовано:
- streaming CSV reading;
- parsing і validation;
- пропуск некоректних записів;
- фільтрація за автором і роком;
- lazy пошук книги заданого автора;
- streaming average кількості сторінок;
- визначення книги з найбільшою кількістю сторінок;
- перші N книг після заданого року через `islice`;
- batch processing;
- generator expression;
- `yield from`;
- `itertools.chain`, `islice`, `accumulate`;
- власний iterator;
- dataset на 100 000 records;
- порівняння eager і lazy processing через `time.perf_counter` і `tracemalloc`;
- оцінка часу до першого результату.

Запуск:

```bash
python -m stream_processor.main
```

Структура:

```text
stream_books_variant2/
├── pyproject.toml
├── README.md
├── data/
└── src/
    └── stream_processor/
        ├── __init__.py
        ├── models.py
        ├── readers.py
        ├── parsers.py
        ├── filters.py
        ├── transformations.py
        ├── batches.py
        ├── analytics.py
        ├── pipeline.py
        ├── experiments.py
        ├── iterators.py
        └── main.py
```
