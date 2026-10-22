FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ENVIRONMENT=production \
    DATABASE_URL=sqlite:////app/data/books.db \
    LOG_LEVEL=INFO

WORKDIR /app
RUN addgroup --system app && adduser --system --ingroup app app \
    && mkdir -p /app/data && chown -R app:app /app
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir .
USER app
EXPOSE 8000
VOLUME ["/app/data"]
CMD ["book-manager"]
