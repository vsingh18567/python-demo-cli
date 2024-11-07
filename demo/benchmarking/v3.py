from collections import defaultdict
from dataclasses import dataclass
import json
from math import sqrt
import time
from typing import Callable, Sequence
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from demo.reading.v3 import (
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
    times = {}
    for func in functions:
        if "trash" in func.__name__ and n > 100_000:
            continue
        times_for_func = []
        print(f"\tBenchmarking {func.__name__}")
        for _ in range(NUM_RUNS):
            times_for_func.append(_benchmark_once(n, func))
        print(f"\t{sum(times_for_func) / NUM_RUNS:.4f} s")
        times[func.__name__] = times_for_func
    return times


@dataclass
class Stats:
    n: int
    mean: float
    stdev: float
    min_: float
    max_: float
    time_per_row: float
    margin_of_error: float


def convert_times_to_stats(times: list[float], n: int) -> Stats:
    mean = sum(times) / len(times)
    stdev = sqrt(sum((t - mean) ** 2 for t in times) / len(times))
    min_time = min(times)
    max_time = max(times)
    margin_of_error = 1.96 * stdev / sqrt(len(times))
    return Stats(n, mean, stdev, min_time, max_time, mean / n, margin_of_error)


def benchmark(
    sizes: Sequence[int], functions: list[GeneratingFunc]
) -> dict[int, dict[str, Stats]]:
    times = {}
    for size in sizes:
        print(f"Benchmarking for size {size}")
        times_for_size = benchmark_with_size(size, functions)
        stats = {}
        for k, v in times_for_size.items():
            stats[k] = convert_times_to_stats(v, size)
        times[size] = stats
    return times


def pretty_print_and_dump(benchmark_results: dict[int, dict[str, Stats]]) -> None:
    print("\n" * 5)
    json_data = defaultdict(dict)
    for size, stats in benchmark_results.items():
        print(f"Results for size {size}")
        data = list(stats.items())
        data.sort(key=lambda x: x[1].mean)
        headers = [
            "Rank",
            "Function",
            "Mean (s)",
            "Margin of Error (s)",
            "Range (s, s)",
            "Time per row (us)",
        ]
        tabulated_data = []
        for i, (func_name, stat) in enumerate(data):
            tabulated_data.append(
                [
                    i + 1,
                    func_name,
                    f"{stat.mean:.4f}",
                    f"{stat.margin_of_error:.4f}",
                    f"[{stat.min_:.4f}, {stat.max_:.4f}]",
                    f"{(stat.time_per_row * 1_000_000):.2f}",
                ]
            )
            json_data[size][func_name] = stat.__dict__
        print(tabulate(tabulated_data, headers=headers, tablefmt="fancy_grid"))
    with open("benchmark_results.json", "w") as f:
        json.dump(json_data, f, indent=2)


def main() -> None:
    os.environ["DISABLE_TQDM"] = "1"
    FUNCS = [
        generate_readings_trash,
        generate_readings_fast,
        generate_readings_batch_write,
        generate_readings_single_write,
        generate_readings_multi_process,
    ]
    SIZES = [10**i for i in range(3, 8)]
    benchmark_results = benchmark(SIZES, FUNCS)  # type: ignore
    pretty_print_and_dump(benchmark_results)


if __name__ == "__main__":
    main()
