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

NUM_RUNS = 5

GeneratingFunc = Callable[[int, int, str], None]


def _benchmark_once(n: int, function: GeneratingFunc) -> float:
    output_file = f"{function.__name__}_{n}.csv"
    start = time.time()
    function(n, n // 10, output_file)
    duration = time.time() - start
    os.remove(output_file)
    return duration


def benchmark_with_size(
    n: int, functions: list[GeneratingFunc]
) -> dict[str, list[float]]:
    for func in functions:
        if "trash" in func.__name__ and n > 100_000:
            continue
        times_for_func = []
        print(f"\tBenchmarking {func.__name__}")
        for _ in range(NUM_RUNS):
            times_for_func.append(_benchmark_once(n, func))
        print(f"\t{sum(times_for_func) / NUM_RUNS:.4f} s")


def benchmark(sizes: Sequence[int], functions: list[GeneratingFunc]) -> None:
    for size in sizes:
        print(f"Benchmarking for size {size}")
        benchmark_with_size(size, functions)


def main() -> None:
    os.environ["DISABLE_TQDM"] = "1"
    FUNCS = [
        generate_readings_trash,
        generate_readings_fast,
        generate_readings_batch_write,
        generate_readings_single_write,
        generate_readings_multi_process,
    ]
    SIZES = [10**i for i in range(2, 5)]
    benchmark(SIZES, FUNCS)  # type: ignore


if __name__ == "__main__":
    main()
