from fastapi import FastAPI
from book_catalog.config import settings, logger

app = FastAPI(title=settings.app_name)

@app.get("/health")
async def health() -> dict[str, str]:
    logger.info("Health check endpoint accessed.")
    return {"status": "ok", "environment": settings.environment}

@app.get("/books")
async def get_books():
    return []

@app.get("/authors")
async def get_authors():
    return []

@app.get("/authors/{id}/books")
async def get_author_books(id: int):
    return []
