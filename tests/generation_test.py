from FormalBench.assistants.inference import SpecInfer
from FormalBench.assistants.fixer import SpecFixer
import uuid
import json

def test_generator():
    generator = SpecInfer(workflow="only_gen", model_name="deepseekv3")
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
    
    generator = SpecInfer(workflow="basic", model_name="deepseekv3", timeout=10)
    code = open("tests/testcases/specs/Absolute_wrong.java").read()
    class_name = "AddLoop"
    config = {
            "configurable": {
                "thread_id": str(uuid.uuid4()),
            }
    }
    results = generator.generate(code, class_name, config)
    assert "spec" in results, "Specification should be generated"
    assert "messages" in results, "Messages should be generated"
    
def test_fixer():
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

