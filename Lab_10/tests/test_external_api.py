import asyncio

import httpx
import pytest

from book_catalog.external_api import fetch_many_author_books, fetch_with_retry


@pytest.mark.asyncio
async def test_fetch_with_retry_returns_json():
    calls = 0

    async def handler(request):
        nonlocal calls
        calls += 1
        if calls == 1:
            return httpx.Response(503, json={"error": "temporary"})
        return httpx.Response(200, json={"author_id": 7, "books": []})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler), timeout=1) as client:
        result = await fetch_with_retry(client, "https://example.test/authors/7/books", attempts=2)
    assert result["author_id"] == 7
    assert calls == 2


@pytest.mark.asyncio
async def test_fetch_with_retry_raises_after_attempts():
    async def handler(request):
        return httpx.Response(503, json={"error": "unavailable"})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler), timeout=1) as client:
        with pytest.raises(httpx.HTTPStatusError):
            await fetch_with_retry(client, "https://example.test/fail", attempts=2)


@pytest.mark.asyncio
async def test_fetch_many_uses_concurrent_requests_and_returns_results(monkeypatch):
    active = 0
    maximum = 0

    async def handler(request):
        nonlocal active, maximum
        active += 1
        maximum = max(maximum, active)
        await asyncio.sleep(0.01)
        active -= 1
        author_id = int(request.url.path.split("/")[-2])
        return httpx.Response(200, json={"author_id": author_id, "books": []})

    original = httpx.AsyncClient

    def factory(*args, **kwargs):
        kwargs["transport"] = httpx.MockTransport(handler)
        return original(*args, **kwargs)

    monkeypatch.setattr("book_catalog.external_api.httpx.AsyncClient", factory)
    results = await fetch_many_author_books([1, 2, 3, 4], "https://example.test", timeout=1, retries=1, concurrency=2)
    assert [item["author_id"] for item in results] == [1, 2, 3, 4]
    assert maximum <= 2
