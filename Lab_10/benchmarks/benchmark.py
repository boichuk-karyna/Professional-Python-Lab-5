from __future__ import annotations

import csv
import statistics
import sys
from pathlib import Path
from time import perf_counter
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from book_manager.analytics import generate_books, pages_numpy, pages_python
from book_manager.parallel import score_processes, score_sequential, score_threads
from book_manager.profiling import measure_memory, profile_callable


def repeated(function: Callable, repeats: int = 3) -> tuple[float, object]:
    samples = []
    result = None
    for _ in range(repeats):
        start = perf_counter()
        result = function()
        samples.append(perf_counter() - start)
    return statistics.mean(samples), result


def main() -> None:
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 100_000
    books = generate_books(count)
    values = list(range(1, min(count, 20_000) + 1))
    experiments: list[tuple[str, Callable[[], object], int, str]] = [
        ("Python baseline", lambda: pages_python(books), 1, "statistics"),
        ("NumPy vectorized", lambda: pages_numpy(books), 1, "statistics"),
        ("Sequential CPU", lambda: score_sequential(values), 1, "cpu"),
        ("ThreadPoolExecutor CPU", lambda: score_threads(values, 4), 4, "cpu"),
        ("ProcessPoolExecutor CPU", lambda: score_processes(values, 4), 4, "cpu"),
    ]
    baseline_times: dict[str, float] = {}
    pending_rows = []
    print(f"Book catalog size: {len(books):,}; CPU workload size: {len(values):,}")
    for name, function, workers, group in experiments:
        (_, current_mb, peak_mb) = measure_memory(function)
        elapsed, result = repeated(function, repeats=3)
        if name in ("Python baseline", "Sequential CPU"):
            baseline_times[group] = elapsed
        pending_rows.append((name, count, workers, elapsed, current_mb, peak_mb, group))
        print(f"{name:28} mean={elapsed:.6f}s peak={peak_mb:.2f}MB")
    rows = []
    for name, data_size, workers, elapsed, current_mb, peak_mb, group in pending_rows:
        baseline_time = baseline_times[group]
        speedup = baseline_time / elapsed if elapsed else 1.0
        rows.append({"experiment": name, "data_size": data_size, "workers": workers,
                     "mean_time_s": f"{elapsed:.6f}", "current_memory_mb": f"{current_mb:.3f}",
                     "peak_memory_mb": f"{peak_mb:.3f}", "speedup_vs_group_baseline": f"{speedup:.3f}"})
        print(f"  speedup vs {group} baseline: {speedup:.2f}x")
    # Check that the two implementations of the same statistics agree.
    python_stats = pages_python(books)
    numpy_stats = pages_numpy(books)
    assert python_stats["count"] == numpy_stats["count"]
    assert abs(float(python_stats["average"]) - float(numpy_stats["average"])) < 1e-9
    assert python_stats["minimum"] == numpy_stats["minimum"]
    assert python_stats["maximum"] == numpy_stats["maximum"]
    output = ROOT / "results" / "benchmark_results.csv"
    output.parent.mkdir(exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    profile_callable(lambda: pages_python(books), ROOT / "results" / "profile.prof")
    print(f"\nCSV results: {output}")
    print("Correctness checks: PASSED")


if __name__ == "__main__":
    main()
