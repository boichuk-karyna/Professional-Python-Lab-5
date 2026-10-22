from itertools import accumulate, chain, islice
from pathlib import Path

from stream_processor.analytics import (
    count_by_author,
    find_largest_book,
    process_batch,
    streaming_average_pages,
)
from stream_processor.batches import batched_books
from stream_processor.experiments import (
    generate_test_file,
    measure,
    measure_first_result,
)
from stream_processor.iterators import BookPageIterator
from stream_processor.pipeline import (
    build_author_pipeline,
    build_pipeline,
    build_search_pipeline,
    build_year_pipeline,
    combine_pipelines,
)


def main() -> None:
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    data_path = data_dir / "books_100000.csv"

    if not data_path.exists():
        print("Creating 100 000 records...")
        generate_test_file(data_path, 100_000)

    print("=== VARIANT 2: BOOK STREAM PROCESSING ===")

    author_pipeline = build_author_pipeline(
        data_path,
        "J.K. Rowling",
    )
    first_author_books = list(islice(author_pipeline, 5))

    print("\nFirst 5 books by J.K. Rowling:")
    for book in first_author_books:
        print(book)

    year_pipeline = build_year_pipeline(
        data_path,
        2020,
    )
    first_after_2020 = list(islice(year_pipeline, 5))

    print("\nFirst 5 books after 2020:")
    for book in first_after_2020:
        print(book)

    search_pipeline = build_search_pipeline(
        data_path,
        "George Orwell",
    )
    first_search = next(search_pipeline, None)

    print("\nFirst search result for 'George Orwell':")
    print(first_search)

    average = streaming_average_pages(
        build_pipeline(data_path)
    )
    print(f"\nStreaming average pages: {average:.2f}")

    largest = find_largest_book(
        build_pipeline(data_path)
    )
    print("\nLargest book:")
    print(largest)

    counts = count_by_author(
        build_pipeline(data_path)
    )
    print("\nBooks by authors:")
    print(counts)

    print("\nBatch processing:")
    batches = batched_books(
        build_pipeline(data_path),
        1000,
    )
    for index, batch in enumerate(islice(batches, 3), start=1):
        print(
            f"Batch {index}: "
            f"{len(batch)} records, "
            f"{process_batch(batch)} pages"
        )

    print("\nGenerator expression:")
    pages = (
        book.pages
        for book in islice(build_pipeline(data_path), 10)
    )
    print(f"Total pages in first 10 books: {sum(pages)}")

    print("\nItertools chain:")
    first_part = build_author_pipeline(data_path, "J.K. Rowling")
    second_part = build_author_pipeline(data_path, "George Orwell")
    combined = chain(first_part, second_part)
    print(f"First combined record: {next(combined, None)}")

    print("\nItertools accumulate:")
    first_pages = (
        book.pages
        for book in islice(build_pipeline(data_path), 5)
    )
    print("Cumulative pages:", list(accumulate(first_pages)))

    print("\nCustom iterator:")
    sample = list(islice(build_pipeline(data_path), 3))
    for book in BookPageIterator(sample):
        print(book.title)

    print("\nEager vs lazy experiment:")
    eager_time, eager_memory, eager_count_value = measure(
        eager_count,
        data_path,
    )
    lazy_time, lazy_memory, lazy_count_value = measure(
        lazy_count,
        data_path,
    )
    first_result_time = measure_first_result(data_path)

    print(
        f"Eager: time={eager_time:.4f}s, "
        f"peak memory={eager_memory:.2f} MB, "
        f"records={eager_count_value}"
    )
    print(
        f"Lazy:  time={lazy_time:.4f}s, "
        f"peak memory={lazy_memory:.2f} MB, "
        f"records={lazy_count_value}"
    )
    print(
        f"Time to first lazy result: "
        f"{first_result_time:.6f}s"
    )

    print("\nLab requirements covered:")
    print("✓ streaming CSV reading")
    print("✓ validation and invalid-record skipping")
    print("✓ author/year filtering")
    print("✓ lazy search")
    print("✓ streaming average pages")
    print("✓ largest book")
    print("✓ first N books with islice")
    print("✓ batch processing")
    print("✓ generator expression")
    print("✓ yield from")
    print("✓ itertools: chain, islice, accumulate")
    print("✓ custom iterator")
    print("✓ 100 000 records")
    print("✓ eager/lazy time and memory comparison")


if __name__ == "__main__":
    main()
