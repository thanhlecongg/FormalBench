from FormalBench.assistants.inference import SpecInfer
import uuid

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
    