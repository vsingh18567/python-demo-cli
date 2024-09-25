**toy example of a simple cli application used to demonstrate some modern python development practices**

This example solves the fictional problem of needing to generate lots of synthetic cardiac data quickly for testing purposes. We both oversimplify the problem and overengineer the solution for the sake of demonstration.

## Installation
```bash
pip3 install poetry
poetry install
```
## Usage
Generate readings by running `python3 reading.py`
```bash
❯ python3 reading.py [-h] [-n N] [--num_patients NUM_PATIENTS] [--mode {trash,fast,numpy,batch_write,single_write,multi_process}]
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

Also have a benchmark script to compare the performance of the different modes. Run `python3 benchmark.py` to see the results (takes a long time -- modify the`SIZES` variable to make it faster).
