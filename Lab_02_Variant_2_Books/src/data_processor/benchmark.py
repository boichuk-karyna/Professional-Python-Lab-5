from time import perf_counter


def find_linear(books: list[dict], book_id: int) -> dict | None:
    for book in books:
        if book["id"] == book_id:
            return book
    return None


def benchmark_search(sizes: tuple[int, ...] = (1_000, 10_000, 100_000)) -> list[dict]:
    results = []

    for size in sizes:
        books = [
            {
                "id": i,
                "title": f"Book {i}",
                "author": f"Author {i % 100}",
                "year": 2000 + (i % 25),
                "pages": 100 + (i % 900),
            }
            for i in range(size)
        ]
        target = size - 1

        start = perf_counter()
        find_linear(books, target)
        list_time = perf_counter() - start

        start = perf_counter()
        index = {book["id"]: book for book in books}
        build_time = perf_counter() - start

        start = perf_counter()
        index.get(target)
        dict_time = perf_counter() - start

        results.append(
            {
                "records": size,
                "list_search": list_time,
                "dict_build": build_time,
                "dict_search": dict_time,
            }
        )

    return results
