import asyncio
import os
from typing import Any

import httpx
from dotenv import load_dotenv

load_dotenv()

DEFAULT_TIMEOUT = float(os.getenv("HTTP_TIMEOUT", "3.0"))
DEFAULT_RETRIES = max(1, int(os.getenv("HTTP_RETRIES", "3")))
DEFAULT_CONCURRENCY = max(1, int(os.getenv("HTTP_CONCURRENCY", "3")))
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")


async def fetch_with_retry(
    client: httpx.AsyncClient,
    url: str,
    attempts: int = DEFAULT_RETRIES,
) -> dict[str, Any]:
    """GET JSON with timeout configured on AsyncClient and exponential retry."""
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            response = await client.get(url)
            response.raise_for_status()
            payload = response.json()
            if not isinstance(payload, dict):
                raise ValueError("Expected a JSON object from the API")
            return payload
        except (httpx.RequestError, httpx.HTTPStatusError, ValueError) as exc:
            last_error = exc
            if attempt + 1 == attempts:
                raise
            await asyncio.sleep(0.1 * (2 ** attempt))
    raise RuntimeError("Retry loop ended unexpectedly") from last_error


async def fetch_many_author_books(
    author_ids: list[int],
    base_url: str = API_BASE_URL,
    timeout: float = DEFAULT_TIMEOUT,
    retries: int = DEFAULT_RETRIES,
    concurrency: int = DEFAULT_CONCURRENCY,
) -> list[dict[str, Any]]:
    """Fetch each author's book list concurrently, limiting simultaneous HTTP requests."""
    semaphore = asyncio.Semaphore(concurrency)
    async with httpx.AsyncClient(timeout=timeout) as client:
        async def limited_fetch(author_id: int) -> dict[str, Any]:
            async with semaphore:
                return await fetch_with_retry(
                    client, f"{base_url.rstrip('/')}/authors/{author_id}/books", attempts=retries
                )

        tasks = [
            asyncio.create_task(limited_fetch(author_id), name=f"author-books-{author_id}")
            for author_id in author_ids
        ]
        try:
            return list(await asyncio.wait_for(asyncio.gather(*tasks), timeout=timeout * max(2, len(tasks))))
        except Exception:
            for task in tasks:
                if not task.done():
                    task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
            raise
