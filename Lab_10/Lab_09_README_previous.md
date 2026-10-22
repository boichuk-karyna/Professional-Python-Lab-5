# Professional Python — Lab 9, Variant 2
## Book catalog: concurrency, multiprocessing and optimization

This project extends the **book catalog** domain: each book has a title, author, publication year and page count. It keeps the required operations (add, search by author, filter by year, largest book, average pages) and adds profiling and performance experiments.

## Requirements
- Python 3.11+
- NumPy
- pytest for tests

## Setup (Windows / PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```
If editable installation is not desired, install dependencies with `python -m pip install -r requirements.txt`.

## Run the application
```powershell
python -m book_manager.main --count 100000
```
If running from the repository root without installing the package:
```powershell
$env:PYTHONPATH = "src"
python -m book_manager.main --count 100000
```

## Tests
```powershell
python -m pytest
```

## Run performance experiments
```powershell
python benchmarks/benchmark.py
```
Optional data size:
```powershell
python benchmarks/benchmark.py 100000
```
The benchmark performs three timing repetitions per implementation, records measured values to `results/benchmark_results.csv`, writes a cProfile snapshot to `results/profile.prof`, checks Python and NumPy results for correctness and prints a comparison table. Actual values depend on hardware and Python version; no example timing is presented as a measured result in advance.

## What is implemented against the requirements
- Reproducible generated catalog of 100,000 books by default (can be increased to 300,000).
- Baseline Python-loop statistics and NumPy vectorized statistics.
- CPU-bound sequential, `ThreadPoolExecutor`, and `ProcessPoolExecutor` implementations.
- Direct `threading.Thread` example and synchronization using `Lock` to protect a shared counter.
- ThreadPoolExecutor for parallel JSON/CSV file reads (I/O-bound example).
- `time.perf_counter` repeated benchmark, speedup relative to baseline, CSV results.
- `cProfile` and `tracemalloc` memory measurement.
- Cached author statistics, version-aware cache and invalidation after catalog mutation.
- Unit and integration-style tests for validation, catalog operations, correctness, parallel implementations, cache invalidation, I/O and memory measurement.

## Interpreting results
Concurrency means coordinating overlapping tasks; parallelism means executing work simultaneously on multiple CPU cores. In standard CPython, the GIL limits simultaneous execution of Python bytecode by threads, so CPU-bound Python code may not benefit from threads. Processes can use multiple cores, but startup and serialization overhead can outweigh gains for small workloads. NumPy can be faster for numeric aggregates because its core loops execute in optimized native code. Always use measured results for conclusions.

## Suggested Git commits
1. `Add book catalog performance benchmarks`
2. `Profile catalog analytics bottlenecks`
3. `Add threaded and process pool experiments`
4. `Add NumPy vectorized statistics`
5. `Add caching and performance tests`
