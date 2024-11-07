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
    for i in tqdm(range(n)):
        reading = _generate_reading(i, num_patients)
        with open(output_file, "a") as f:
            f.write(reading.to_csv())


def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-n", type=int, help="Number of readings to generate", default=1_000_000
    )
    parser.add_argument(
        "--num_patients", type=int, help="Number of patients", default=10
    )

    parser.add_argument(
        "--summarize", action="store_true", help="Summarize the output file"
    )

    parser.add_argument(
        "output_file", type=str, help="Output file", default="readings.csv"
    )

    args = parser.parse_args()
    generate_readings_trash(args.n, args.num_patients, args.output_file)


if __name__ == "__main__":
    main()
