from math import sqrt
import random
from multiprocessing import Process, cpu_count
import time


def gen_random(totals, i):
    local_total = 0
    for _ in range(1000000):
        local_total += random.randint(0, 1000)
    totals[i] = local_total
    
if __name__ == "__main__":
    NUM_PROCESSES = cpu_count()
    processes = []
    totals = [0] * NUM_PROCESSES
    start = time.time()
    for i in range(NUM_PROCESSES):
        process = Process(target=gen_random, args=(totals, i))
        processes.append(process)
        process.start()
    for p in processes:
        p.join()
    total = sum(totals)
    print(f"Multi Process Time taken: {time.time() - start}")
    start = time.time()
    for i in range(1000000 * NUM_PROCESSES):
        total += random.randint(0, 1000)
    print(f"Single Process Time taken: {time.time() - start}")
