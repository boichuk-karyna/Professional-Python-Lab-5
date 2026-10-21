from __future__ import annotations

import cProfile
import pstats
import tracemalloc
from pathlib import Path
from typing import Callable, Any


def profile_callable(function: Callable[[], Any], output: str | Path = "results/profile.prof") -> None:
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    profiler = cProfile.Profile()
    profiler.enable()
    function()
    profiler.disable()
    profiler.dump_stats(str(path))
    pstats.Stats(profiler).sort_stats("cumulative").print_stats(15)


def measure_memory(function: Callable[[], Any]) -> tuple[Any, float, float]:
    tracemalloc.start()
    try:
        result = function()
        current, peak = tracemalloc.get_traced_memory()
        return result, current / (1024 * 1024), peak / (1024 * 1024)
    finally:
        tracemalloc.stop()
