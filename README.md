# FormalBench: A Comprehensive Benchmark for Formal Specification Inference

[![Build and test](https://github.com/thanhlecongg/FormalBench/actions/workflows/build_and_test.yml/badge.svg)](https://github.com/thanhlecongg/FormalBench/actions/workflows/build_and_test.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Release](https://img.shields.io/badge/Release-InProgress-orange.svg)]()

## Prerequisites

FormalBench have two modes:
- Docker mode, which requires the docker in your local computers
- Non-Docker mode, which requires Ubuntu 20.04

Versions:
- Python 3.12
- Pip 25.0
- Java 11

## Installation

- Step 1: Clone FormalBench to local computers:
```
git clone https://github.com/thanhlecongg/FormalBench.git
```

- Step 2: Create virtual environment with Python (default version of FormalBench is Python 3.12)
```
python3 -m venv .env
. .env/bin/activate
```

- Step 3: Install FormalBench
```
pip3 install -e .[default]
```

## Basic Usage

### Verification Tool
You can use verification tool to verify your generated specification using following code:
```python
from FormalBench.evaluation import create_verifier

### Create python wrapper for OpenJML verifier
verifier = create_verifier("OpenJML", 21)

### Verirify generated spec which is stored in a .java file
n_errors, output = verifier.verify("tests/testcases/specs/Absolute.java")
print("Number of errors: ", n_errors)
```

Expected output should be:

```
Path: FormalBench/tests/testcases/specs/Absolute.java
src_dir: FormalBench/tests/testcases/specs
Executing command: timeout 1800 /home/openjml21/openjml --esc --prover=cvc4 --nullable-by-default --esc-max-warnings 1 /tmp/Absolute.java
Current working directory: FormalBench
Output: 
Number of errors:  0
Cleaning up the docker container
```

### Consistency Metrics

You can use our built-in metrics to measure the consistency of your generated specification using the followwing code:

```python
from FormalBench.evaluation import eval_consistency

# Evaluate the consistency of the specifications
# spec_dir: str, the directory where the specifications are stored
# analysis_dir: str, the directory where the analysis results will be stored
success_rate, failure_rate, results = eval_consistency(
                                        spec_dir = "tests/testcases/results/specs", 
                                        analysis_dir = "tests/testcases/results/analysis_results"
                                    )
print("Success rate: ", success_rate)
print("Failure rate: ", failure_rate)

```

Expected output should be:

```
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 4/4 [00:00<00:00, 2621.85it/s]
Success rate: 0.25
Failure rate: 0.50
Cleaning up the docker container
```

### Completeness Metrics

You can use our built-in metrics to measure the completeness of your generated specification using the followwing code:
```python
from FormalBench.evaluation import eval_completeness


# Evaluate the consistency of the specifications
# data_dir: path to the directory containing the specifications
# save_dir: path to the directory storing the analysis results
avg_coverage, coverage_results, inconsistent_instances = eval_completeness(
                                        data_dir = "tests/testcases/results/specs", 
                                        save_dir = "tests/testcases/results/completeness", 
                                        timeout=20)

print("Average coverage: ", avg_coverage)

```
```
...
Average coverage:  1.0
Cleaning up the docker container
```

### Specification Inference

You can use our built-in LLM-based specification inference tool to generate formal specification for a given Java code as follows:
```python
generator = SpecInfer(workflow="basic", model_name="deepseekv3", timeout=10)
code = open("tests/testcases/code/AddLoop.java").read()
class_name = "AddLoop"
config = {
        "configurable": {
            "thread_id": str(uuid.uuid4()),
        }
}
results = generator.generate(code, class_name, config)
assert "spec" in results, "Specification should be generated"
assert "messages" in results, "Messages should be generated"
```

Expected output is LLM's response and verification results  


