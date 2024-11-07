import os
import random
import sys
from tqdm import tqdm
from multiprocessing import cpu_count, Process
import argparse
from dataclasses import dataclass
import numpy as np

BP_RANGE = (100, 140)
SPO2_RANGE = (95, 100)
HR_RANGE = (60, 100)
TIME_RANGE = (0, 1000000)


def _generate_reading(id, num_patients):
    patient_id = random.randint(0, num_patients - 1)
    bp = random.uniform(*BP_RANGE)
    spo2 = random.uniform(*SPO2_RANGE)
    hr = random.uniform(*HR_RANGE)
    timestamp = int(random.uniform(*TIME_RANGE))
    return {
        "id": id,
        "timestamp": timestamp,
        "patient_id": patient_id,
        "spo2": spo2,
        "hr": hr,
        "bp": bp,
    }


def generate_readings_trash(n, num_patients, output_file):
    with open(output_file, "w") as f:
        f.write("id,timestamp,patient_id,spo2,hr,bp\n")
    for i in tqdm(range(n)):
        r = _generate_reading(i, num_patients)
        with open(output_file, "a") as f:
            f.write(
                f"{r['id']},{r['timestamp']},{r['patient_id']},{r['spo2']},{r['hr']},{r['bp']}\n"
            )


def main():
    n = int(sys.argv[1])
    num_patients = int(sys.argv[2])
    output_file = sys.argv[3]
    generate_readings_trash(n, num_patients, output_file)


if __name__ == "__main__":
    main()
