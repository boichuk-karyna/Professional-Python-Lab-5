import csv
import json

from book_manager.parallel import read_files_sequential, read_files_threaded
from book_manager.profiling import measure_memory


def test_threaded_file_loading_matches_sequential(tmp_path):
    paths = []
    for i in range(3):
        path = tmp_path / f"books{i}.json"
        path.write_text(json.dumps([{"title": f"Book {i}"}] * (i + 1)), encoding="utf-8")
        paths.append(str(path))
    assert read_files_threaded(paths, workers=2) == read_files_sequential(paths) == [1, 2, 3]


def test_memory_measurement_returns_result():
    result, current, peak = measure_memory(lambda: [x * x for x in range(100)])
    assert len(result) == 100
    assert current >= 0
    assert peak >= current
