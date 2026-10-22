import logging
from fastapi import FastAPI
from book_catalog.config import settings
from book_catalog.services import CatalogService

logger = logging.getLogger(__name__)

app = FastAPI(title=settings.app_name)
service = CatalogService()

@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "environment": settings.environment}

@app.get("/books")
async def get_books():
    return service.list_books()

@app.get("/authors")
async def get_authors():
    return service.list_authors()

@app.get("/authors/{author_id}/books")
async def get_author_books(author_id: int):
    return service.get_author_books(author_id)
