from typing import Tuple, Dict
import os
from tqdm import tqdm
import json
from .. import create_verifier

def eval_consistency(
        spec_dir: str, 
        analysis_dir: str, 
        verifier_name: str = "OpenJML",
        verifier_version: int = 21,
        timeout: int = 300,
        language: str = "java"
    ) -> Tuple[float, float, Dict]:
    """
    Measure the consistency metrics of a set of specifications againts their reference implementations

    Args:
        spec_dir (str): Path to the directory containing the specifications
        analysis_dir (str, optional): Path to the directory storing the analysis results. 

    Returns:
        Tuple[int, int]: A tuple containing (1) verification success rate, (2) verification failure rate and (3) a dictionary containing the detailed verification results
    """
    
    if language == "java":
        assert verifier_name == "OpenJML", "Only OpenJML is supported for Java programs"
        verifier = create_verifier(verifier_name, verifier_version)
        ending = ".java"
    else:
        raise ValueError("Unknown language: {}. Please select ['java']".format(language))
    
    assert os.path.exists(spec_dir), "Spec directory does not exist"
    os.makedirs(analysis_dir, exist_ok=True)
    
    evaluated_specs = os.listdir(spec_dir)
    evaluated_specs = [file_name[:-len(ending)] for file_name in evaluated_specs if file_name.endswith(ending)]
    evaluation_results = {}
    
    total_evaluated_specs = len(evaluated_specs)
    
    print("Evaluating the consistency of {} specifications stored in {}".format(total_evaluated_specs, spec_dir))
    
    number_of_failures = 0
    number_of_successes = 0
    number_of_unknown = 0
    
    for spec_name in tqdm(evaluated_specs):
        spec_path = os.path.join(spec_dir, spec_name + ".java")
        analysis_path = os.path.join(analysis_dir, spec_name + ".json")
        if os.path.exists(analysis_path):
            print("Analysis result file exists. Loading the result")
            try:
                with open(analysis_path, "r") as f:
                    result_dict = json.load(f)
                    if isinstance(result_dict["analysis_results"][0], list):
                        n_errors, output, _ = result_dict["analysis_results"][-1]
                    else:
                        n_errors, output, _ = result_dict["analysis_results"]
            except:
                raise ValueError("Analysis result file is corrupted")
        else:
            n_errors, output = verifier.verify(spec_path, timeout=timeout)
            spec = open(spec_path, "r").read()
            with open(analysis_path, "w") as f:
                json.dump({"analysis_results": [n_errors, output, spec]}, f)
        
        evaluation_results[spec_name] = {
            "details": (n_errors, output)
        }
        
        if n_errors == 0:
            number_of_successes += 1
            evaluation_results[spec_name]["status"] = "Success"
        elif n_errors == -1:
            number_of_unknown += 1
            evaluation_results[spec_name]["status"] = "Unknown"
        else:
            number_of_failures += 1
            evaluation_results[spec_name]["status"] = "Failure"

    return number_of_successes / total_evaluated_specs, number_of_failures / total_evaluated_specs, evaluation_results
        
        
        
    
    
    
    
    