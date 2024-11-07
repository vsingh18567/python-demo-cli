**toy example of a simple cli application used to demonstrate some modern python development practices**

This example solves the fictional problem of needing to generate lots of synthetic cardiac data quickly for testing purposes. We both oversimplify the problem and overengineer the solution for the sake of demonstration.

## Installation
```bash
pip3 install poetry
poetry install
```
## Usage
Generate readings by running `python3 reading/v3.py`
```bash
❯ python3 reading/v3.py [-h] [-n N] [--num_patients NUM_PATIENTS] [--mode {trash,fast,numpy,batch_write,single_write,multi_process}]
                  [--summarize]
                  output_file

positional arguments:
  output_file           Output file

options:
  -h, --help            show this help message and exit
  -n N                  Number of readings to generate
  --num_patients NUM_PATIENTS
                        Number of patients
  --mode {trash,fast,numpy,batch_write,single_write,multi_process}
                        Mode to generate readings
  --summarize           Summarize the output file
```

Also have a benchmark script to compare the performance of  different modes. Run `python3 benchmark/v3.py` to see the results (takes a long time -- modify the`SIZES` variable to make it thefaster).

## Versions

reading/v1.py is the simplest and most naive implementation of the reading generation. It is the baseline for the other implementations.

reading/v2.py introduces type hints and dataclasses to make the code more readable and maintainable.

reading/v3.py is the final implementation of the reading generation. It introduces several modes to generate readings, each with different performance characteristics

benchmarking/v1.py is the simplest and most naive implementation of the benchmarking script. It is the baseline for the other implementations.

benchmarking/v2.py introduces running the benchmark multiple times and over multiple input sizes to get a better idea of the performance characteristics of each mode

benchmarking/v3.py introduces visualizing the results of the benchmarking script to make it easier to understand the performance characteristics of each mode