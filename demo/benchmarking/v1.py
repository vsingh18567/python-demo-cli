from dataclasses import dataclass
from math import sqrt
import os
import time
from typing import Callable, Sequence
from reading.v3 import (
    generate_readings_batch_write,
    generate_readings_fast,
    generate_readings_multi_process,
    generate_readings_single_write,
    generate_readings_trash,
)
from tabulate import tabulate


GeneratingFunc = Callable[[int, int, str], None]


def _benchmark_once(n: int, function: GeneratingFunc) -> None:
    print(f"\tBenchmarking {function.__name__}")
    output_file = f"{function.__name__}_{n}.csv"
    start = time.time()
    function(n, n // 10, output_file)
    duration = time.time() - start
    os.remove(output_file)
    print(f"{function.__name__}: {duration:.3f}s")


def main() -> None:
    os.environ["DISABLE_TQDM"] = "1"
    FUNCS = [
        generate_readings_trash,
        generate_readings_fast,
        generate_readings_batch_write,
        generate_readings_single_write,
        generate_readings_multi_process,
    ]
    SIZE = 10_000
    for func in FUNCS:
        _benchmark_once(SIZE, func)


if __name__ == "__main__":
    main()
