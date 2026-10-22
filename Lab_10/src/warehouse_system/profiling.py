import cProfile
import pstats
import tracemalloc
from warehouse_system.analytics import (
    generate_large_dataset,
    calculate_total_value_python,
)


def profile_execution_time() -> None:
    """Аналіз продуктивності та виявлення bottlenecks за допомогою cProfile."""
    print("=== cProfile: Аналіз часу виконання ===")
    dataset = generate_large_dataset(100_000)

    profiler = cProfile.Profile()
    profiler.enable()

    _ = calculate_total_value_python(dataset)

    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats("cumulative")
    stats.print_stats(10)


def profile_memory_usage() -> None:
    """Аналіз використання пам'яті за допомогою tracemalloc."""
    print("\n=== tracemalloc: Аналіз використання пам'яті ===")
    tracemalloc.start()

    dataset = generate_large_dataset(200_000)
    current, peak = tracemalloc.get_traced_memory()

    print(f"Поточна виділена пам'ять: {current / (1024 * 1024):.2f} MB")
    print(f"Пікова виділена пам'ять:    {peak / (1024 * 1024):.2f} MB")

    tracemalloc.stop()


if __name__ == "__main__":
    profile_execution_time()
    profile_memory_usage()