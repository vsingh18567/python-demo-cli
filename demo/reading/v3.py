import os
import random
from tqdm import tqdm
from multiprocessing import cpu_count, Process
import argparse
from dataclasses import dataclass
import numpy as np

BP_RANGE = (100, 140)
SPO2_RANGE = (95, 100)
HR_RANGE = (60, 100)
TIME_RANGE = (0, 1000000)
PROCESSES = cpu_count()


def custom_tqdm(iterable, *args, **kwargs):
    if os.environ.get("DISABLE_TQDM"):
        return iterable
    return tqdm(iterable, *args, **kwargs)


@dataclass
class Reading:
    id: int
    timestamp: int
    patient_id: int
    spo2: float
    hr: float
    bp: float

    def to_csv(self) -> str:
        return f"{self.id},{self.timestamp},{self.patient_id},{self.spo2},{self.hr},{self.bp}\n"


def _generate_reading(id: int, num_patients: int) -> Reading:
    patient_id = random.randint(0, num_patients - 1)
    bp = random.uniform(*BP_RANGE)
    spo2 = random.uniform(*SPO2_RANGE)
    hr = random.uniform(*HR_RANGE)
    timestamp = int(random.uniform(*TIME_RANGE))
    return Reading(id, timestamp, patient_id, spo2, hr, bp)


def generate_readings_trash(n: int, num_patients: int, output_file: str) -> None:
    with open(output_file, "w") as f:
        f.write("id,timestamp,patient_id,spo2,hr,bp\n")
    for i in custom_tqdm(range(n)):
        reading = _generate_reading(i, num_patients)
        with open(output_file, "a") as f:
            f.write(reading.to_csv())


def generate_readings_batch_write(n: int, num_patients: int, output_file: str) -> None:
    readings = []
    for i in custom_tqdm(range(n)):
        readings.append(_generate_reading(i, num_patients))
    with open(output_file, "w") as f:
        f.write("id,timestamp,patient_id,spo2,hr,bp\n")
        for r in readings:
            f.write(r.to_csv())


def generate_readings_single_write(n: int, num_patients: int, output_file: str) -> None:
    with open(output_file, "w") as f:
        f.write("id,timestamp,patient_id,spo2,hr,bp\n")
        for i in custom_tqdm(range(n)):
            reading = _generate_reading(i, num_patients)
            f.write(reading.to_csv())


def generate_readings_fast(n: int, num_patients: int, output_file: str) -> None:
    ids = [i for i in range(n)]
    timestamps = [int(random.uniform(*TIME_RANGE)) for _ in range(n)]
    patient_ids = [random.randint(0, num_patients - 1) for _ in range(n)]
    spo2s = [random.uniform(*SPO2_RANGE) for _ in range(n)]
    hrs = [random.uniform(*HR_RANGE) for _ in range(n)]
    bps = [random.uniform(*BP_RANGE) for _ in range(n)]
    with open(output_file, "w") as f:
        f.write("id,timestamp,patient_id,spo2,hr,bp\n")
        for i in range(n):
            f.write(
                f"{ids[i]},{timestamps[i]},{patient_ids[i]},{spo2s[i]},{hrs[i]},{bps[i]}\n"
            )


def _helper(n: int, num_patients: int, return_list: list[Reading]) -> None:
    for i in range(n):
        return_list.append(_generate_reading(i, num_patients))


def generate_readings_multi_process(
    n: int, num_patients: int, output_file: str
) -> None:
    procs: list[Process] = []
    return_lists: list[list[Reading]] = [[] for _ in range(PROCESSES)]
    for i in range(PROCESSES):
        proc = Process(
            target=_helper, args=(n // PROCESSES, num_patients, return_lists[i])
        )
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()

    with open(output_file, "w") as f:
        f.write("id,timestamp,patient_id,spo2,hr,bp\n")
        for return_list in return_lists:
            for r in return_list:
                f.write(r.to_csv())


def main() -> None:
    parser = argparse.ArgumentParser()

    mode_to_func = {
        "trash": generate_readings_trash,
        "fast": generate_readings_fast,
        "batch_write": generate_readings_batch_write,
        "single_write": generate_readings_single_write,
        "multi_process": generate_readings_multi_process,
    }

    parser.add_argument(
        "-n", type=int, help="Number of readings to generate", default=1_000_000
    )
    parser.add_argument(
        "--num_patients", type=int, help="Number of patients", default=10
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=list(mode_to_func.keys()),
        default="single_write",
        help="Mode to generate readings",
    )

    parser.add_argument(
        "--summarize", action="store_true", help="Summarize the output file"
    )

    parser.add_argument(
        "output_file", type=str, help="Output file", default="readings.csv"
    )

    args = parser.parse_args()
    mode_to_func[args.mode](args.n, args.num_patients, args.output_file)


if __name__ == "__main__":
    main()
