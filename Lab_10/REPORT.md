# Звіт до лабораторної роботи №10

**Заклад освіти:** ______________________________  
**Дисципліна:** Professional Python  
**Виконала:** Бойчук Карина  
**Група:** ФЕП-33, підгрупа 2  
**Варіант:** 2  
**Тема:** Production Python: Docker, CI/CD та захист проєкту  

## 1. Мета роботи

Підготувати проєкт системи обліку книг до production-oriented використання: оформити Python package, забезпечити конфігурацію через змінні середовища, додати REST API, контейнеризацію, автоматизовані перевірки, тести та документацію.

## 2. Короткий опис проєкту

Book Catalog — REST API для каталогу книг. Книга містить назву, автора, рік видання, кількість сторінок та необов'язковий опис. Дані зберігаються через SQLAlchemy у базі даних, URL якої задається змінною `DATABASE_URL`.

Реалізовано додавання, перегляд, пошук за автором і назвою, фільтрацію за роком, видалення книги, перелік авторів, книги автора, статистику кількості книг, середньої кількості сторінок і найбільшої книги. Додатково передбачено сервісні функції імпорту CSV та експорту JSON.

## 3. Структура проєкту

```text
book-catalog/
├── .github/workflows/ci.yml
├── src/book_catalog/
│   ├── __init__.py
│   ├── api.py
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── repositories.py
│   ├── schemas.py
│   └── services.py
├── tests/
│   ├── conftest.py
│   ├── test_api.py
│   └── test_services.py
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── LICENSE
├── pyproject.toml
├── README.md
└── REPORT.md
```

## 4. Package metadata

У `pyproject.toml` визначено назву пакета `book-catalog`, версію `1.0.0`, Python `>=3.11`, основні залежності FastAPI, Uvicorn, SQLAlchemy, Pydantic та Pydantic Settings, а також dev-залежності pytest, pytest-cov, httpx, Ruff, mypy і build. Для збірки використовується `setuptools.build_meta`.

## 5. Збірка package

Команда для стандартної збірки:

```bash
python -m pip install build
python -m build
```

У каталозі `dist/` мають бути wheel та source distribution. У наданому архіві включено створені артефакти:

- `book_catalog-1.0.0-py3-none-any.whl`
- `book_catalog-1.0.0.tar.gz`

Wheel додатково встановлено в окреме чисте virtual environment з параметром `--no-deps`; імпорт `book_catalog` успішний, версія `1.0.0`.

## 6. Environment variables і secrets

Приклад конфігурації наведений у `.env.example`:

```dotenv
APP_NAME=Book Catalog
APP_ENV=development
DATABASE_URL=sqlite:///./book_catalog.db
LOG_LEVEL=INFO
```

`config.py` читає конфігурацію з environment variables та локального `.env`. Файл `.env`, бази даних, virtual environments і build artifacts виключені у `.gitignore`. У репозиторії не повинно бути справжніх паролів, токенів чи ключів. Для CI секрети за потреби додаються у GitHub Settings → Secrets and variables → Actions, а не записуються у YAML чи source code.

## 7. REST API та документація

Основні endpoints:

| Метод | Endpoint | Призначення |
|---|---|---|
| GET | `/health` | Перевірка стану сервісу |
| GET | `/books` | Перелік книг; параметри `author`, `year`, `q` |
| POST | `/books` | Додавання книги |
| GET | `/books/{book_id}` | Отримання книги за ID |
| DELETE | `/books/{book_id}` | Видалення книги |
| GET | `/books/statistics` | Кількість, середня кількість сторінок, найбільша книга |
| GET | `/authors` | Перелік авторів |
| POST | `/authors` | Додавання автора |
| GET | `/authors/{author_id}/books` | Книги конкретного автора |

FastAPI формує документацію за адресами `/docs`, `/redoc` та схему OpenAPI за `/openapi.json`.

## 8. Docker

`Dockerfile` використовує `python:3.12-slim`, встановлює пакет, створює непривілейованого користувача `appuser`, задає health check та запускає Uvicorn. `.dockerignore` виключає Git, `.env`, тести, кеші та артефакти збірки. Для збереження SQLite даних передбачено volume.

Команди для виконання на комп'ютері з установленим Docker:

```bash
docker build -t book-catalog:1.0 .
docker volume create book-catalog-data
docker run --rm -p 8000:8000 ^
  -e APP_ENV=production ^
  -e LOG_LEVEL=INFO ^
  -e DATABASE_URL=sqlite:////app/data/book_catalog.db ^
  -v book-catalog-data:/app/data ^
  book-catalog:1.0
```

У PowerShell команду можна виконати одним рядком, якщо оператор продовження рядка `^` не підходить для поточного термінала. Після запуску потрібно перевірити `http://localhost:8000/health` та `http://localhost:8000/docs`.

**Примітка щодо перевірки:** у середовищі підготовки архіву Docker executable відсутній, тому фактичний Docker image/container і скриншоти запущеного контейнера тут не створювалися. Команди та конфігурація готові для перевірки на комп'ютері з Docker.

## 9. GitHub Actions CI

Workflow `.github/workflows/ci.yml` запускається на `push` до `main`/`develop` і на `pull_request`. Він виконує:

1. Checkout репозиторію.
2. Налаштування Python 3.12.
3. Встановлення `.[dev]`.
4. `ruff check .`.
5. `ruff format --check .`.
6. `mypy src`.
7. `pytest -v` з coverage threshold 80%.
8. `python -m build` та перевірку wheel/sdist.
9. `docker build`.

Після push у власний GitHub репозиторій потрібно відкрити вкладку **Actions** і перевірити результат workflow. Статус remote GitHub Actions не можна підтвердити до такого push.

## 10. Результати локальних перевірок у середовищі підготовки

- `pytest`: **9 тестів пройшли**.
- Coverage: **90%**.
- Wheel: створено та встановлено в окреме чисте virtual environment; імпорт пакета повернув версію `1.0.0`.
- sdist: створено.
- Ruff та mypy: не запускалися в цьому середовищі, оскільки ці команди не були встановлені, а доступ до інтернету для встановлення залежностей був недоступний.
- Docker build/run: не запускалися, оскільки Docker executable відсутній.
- GitHub Actions: необхідно перевірити після push.

## 11. Команди повної перевірки

```bash
python -m pip install -e ".[dev]"
ruff check .
ruff format --check .
mypy src
pytest -v --cov=book_catalog --cov-report=term-missing --cov-fail-under=80
python -m build
docker build -t book-catalog:1.0 .
```

## 12. Production checklist

- [x] `src-layout` та пакет `book_catalog`.
- [x] `pyproject.toml` і project metadata.
- [x] Wheel і sdist створені.
- [x] Wheel встановлено в окреме virtual environment.
- [x] Конфігурація через environment variables.
- [x] `.env.example` додано, `.env` ігнорується.
- [x] У коді не задані справжні credentials.
- [x] `Dockerfile` та `.dockerignore` створені.
- [x] Health endpoint реалізовано.
- [x] GitHub Actions workflow створено.
- [x] Тести пройшли локально; coverage 90%.
- [x] README і звіт додані.
- [ ] Ruff lint і format check фактично запустити.
- [ ] mypy фактично запустити.
- [ ] Docker image/container і health check перевірити на машині з Docker.
- [ ] Push до GitHub і підтвердити green CI.
- [ ] Зробити скриншоти `dist`, Docker image/container, `/health`, Swagger та green CI для остаточного звіту.

## 13. Контрольні запитання — короткі відповіді

1. **Python package** — імпортований набір модулів; **distribution package** — артефакт, який встановлюють.
2. **Wheel** — готовий до встановлення формат `.whl`; **sdist** — архів вихідного коду, зазвичай `.tar.gz`.
3. `pyproject.toml` зберігає метадані проєкту, залежності та конфігурацію інструментів. `[build-system]` визначає backend збірки, `[project]` — метадані та залежності.
4. Збірка виконується командою `python -m build`.
5. Semantic versioning має формат `MAJOR.MINOR.PATCH`: MAJOR — несумісні зміни, MINOR — нова сумісна функціональність, PATCH — виправлення.
6. Environment variable — параметр конфігурації, переданий процесу ззовні; це дозволяє не змінювати код для різних середовищ.
7. Secret — пароль, токен, API key або інші приватні credentials. Їх не можна commit у Git. `.env` зберігає локальні значення і додається до `.gitignore`, а `.env.example` містить лише назви та безпечні приклади параметрів.
8. Dockerfile — інструкції створення image; image — шаблон середовища; container — запущений екземпляр image. `docker build` створює image, `docker run` запускає контейнер.
9. `WORKDIR` задає робочу директорію, `COPY` копіює файли, `EXPOSE` документує порт, `CMD` задає команду запуску, `.dockerignore` виключає зайві файли. Volume зберігає дані поза життєвим циклом контейнера.
10. `/health` дозволяє перевірити стан сервісу; Docker `HEALTHCHECK` періодично виконує таку перевірку.
11. CI — автоматичні перевірки змін; CD — автоматизація доставки/розгортання. GitHub Actions запускає workflow, що складається з jobs і steps на runner.
12. Lint перевіряє стиль і типові помилки; Ruff виконує lint та форматування; mypy перевіряє типи; pytest запускає тести; coverage показує частку виконаного коду.
13. Package build у CI перевіряє, що distribution артефакти можна зібрати; Docker build перевіряє, що образ збирається. GitHub Secrets передаються workflow через `${{ secrets.NAME }}`.
14. README має пояснювати призначення, встановлення, конфігурацію, запуск, API, тести, Docker і CI/CD. Docstrings описують призначення функцій/класів. OpenAPI — машинозчитуваний опис API; `/docs` — Swagger UI, `/redoc` — ReDoc, `/openapi.json` — схема.
15. Logging записує діагностичні події з рівнями важливості та налаштуванням; це гнучкіше за `print`. Production configuration використовує зовнішні параметри та безпечні налаштування. Non-root user зменшує привілеї контейнера, multi-stage build розділяє етапи збірки та runtime, а green CI означає успішне проходження всіх jobs.

## 14. Висновок

У лабораторній роботі підготовлено систему обліку книг до production-oriented використання: оформлено Python package, REST API, persistence layer, конфігурацію через environment variables, документацію, тести, Dockerfile та CI workflow. У середовищі підготовки успішно пройшли 9 тестів із coverage 90%, було створено wheel і sdist та перевірено встановлення wheel в окремому virtual environment. Перед остаточним захистом потрібно запустити Ruff і mypy, зібрати та запустити Docker image, а також перевірити green GitHub Actions після push.
