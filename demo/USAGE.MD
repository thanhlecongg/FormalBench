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

#### SpecInfer

You can use our built-in LLM-based specification inference tool to generate formal specification for a given Java code as follows:
```python
from FormalBench.assistants.inference import SpecInfer
import uuid

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

#### SpecFixer

If verification tool fails to verify the generated specification, you can use our built-in specification fixer to repair it as follows:

```python
from FormalBench.assistants.fixer import SpecFixer
import uuid
import json

generator = SpecFixer(workflow="basic", model_name="deepseekv3", timeout=10)

path = "tests/testcases/results/specs/AddDictToTuple.java"    
class_name = "AddDictToTuple"

with open(path, "r") as f:
    spec = f.read()
        
with open("tests/testcases/results/analysis_results/AddDictToTuple.json", "r") as f:
    analysis_results = json.load(f)

config = {
        "configurable": {
            "thread_id": str(uuid.uuid4()),
        }
}

last_results = analysis_results["analysis_results"]
generator.repair(spec, last_results, class_name, config)
```

Expected output is LLM's response and new verification results  