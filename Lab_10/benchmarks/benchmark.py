from time import perf_counter
from statistics import mean
import csv
from pathlib import Path
from warehouse_system.analytics import (
    generate_large_dataset,
    calculate_total_value_python,
    calculate_total_value_numpy
)
from warehouse_system.parallel import process_items_processes


def benchmark_repeated(func, *args, repeats: int = 3) -> float:
    times = []
    for _ in range(repeats):
        start = perf_counter()
        func(*args)
        elapsed = perf_counter() - start
        times.append(elapsed)
    return mean(times)


def run_benchmarks() -> None:
    dataset_sizes = [10_000, 100_000, 500_000]
    results = []

    print(f"{'Dataset Size':<12} | {'Method':<22} | {'Workers':<8} | {'Mean Time (s)':<15} | {'Speedup'}")
    print("-" * 75)

    for size in dataset_sizes:
        dataset = generate_large_dataset(size)

        # Baseline Python
        base_time = benchmark_repeated(calculate_total_value_python, dataset, repeats=3)
        results.append([size, "Baseline (Python)", 1, f"{base_time:.6f}", "1.00x"])
        print(f"{size:<12} | {'Baseline (Python)':<22} | {1:<8} | {base_time:<15.6f} | 1.00x")

        # NumPy Vectorized
        numpy_time = benchmark_repeated(calculate_total_value_numpy, dataset, repeats=3)
        speedup_np = f"{base_time / numpy_time:.2f}x" if numpy_time > 0 else "N/A"
        results.append([size, "NumPy Vectorized", 1, f"{numpy_time:.6f}", speedup_np])
        print(f"{size:<12} | {'NumPy Vectorized':<22} | {1:<8} | {numpy_time:<15.6f} | {speedup_np}")

        # ProcessPoolExecutor
        if size <= 100_000:
            for w in [2, 4]:
                proc_time = benchmark_repeated(process_items_processes, dataset, w, repeats=2)
                proc_speedup = f"{base_time / proc_time:.2f}x" if proc_time > 0 else "N/A"
                results.append([size, "ProcessPoolExecutor", w, f"{proc_time:.6f}", proc_speedup])
                print(f"{size:<12} | {'ProcessPoolExecutor':<22} | {w:<8} | {proc_time:<15.6f} | {proc_speedup}")

    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    csv_file = results_dir / "benchmark_results.csv"

    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Dataset Size", "Method", "Workers", "Mean Time (s)", "Speedup"])
        writer.writerows(results)

    print(f"\n[УСПІХ] Результати збережено у {csv_file}")


if __name__ == "__main__":
    run_benchmarks()