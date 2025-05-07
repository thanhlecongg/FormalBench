from ..evaluation import load_base_dataset
import os
from tqdm import tqdm
import uuid
import json
from ..assistants.inference import SpecInfer

def experiment(
    data_dir=None,
    use_remote=True,
    language="java",
    model_name="gpt-3.5-turbo",
    prompt_type="zero-shot",
    output_dir=None,
    use_docker=True,
    verbose=False,
    workflow="basic",
):
    """
    Run the experiment with base dataset for a specific programming language.
    Args:
        data_dir (str): Directory to load the dataset from.
        use_remote (bool): Whether to use remote dataset or local directory.
        language (str): Programming language to use for the experiment.
        model_name (str): Name of the model to use for inference.
        prompt_type (str): Type of prompt to use for inference.
        output_dir (str): Directory to save the output files.
        use_docker (bool): Whether to use Docker for inference.
        verbose (bool): Whether to print verbose output.
        workflow (str): Workflow type for the experiment.
    """
    assert language in ["java","c"], "Language not supported. Only java and c are supported"
    
    print("Starting experiment with base dataset for {} programming language".format(language.upper()))
    meta_data, data_dir = load_base_dataset(data_dir=data_dir, use_remote=use_remote)
    data_dir = os.path.join(data_dir, "programs")
    print("Data directory: ", data_dir)
    print("Data size: ", len(meta_data))

    if output_dir is None:
        print("Output directory not specified, using default at ./output")
        output_dir = os.path.join("output", language) 
    else:
        print("Output directory specified: ", output_dir)
    
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, "analysis_results"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "specs"), exist_ok=True)
    
    cnt = 0
    for class_name in tqdm(meta_data):
        config = {
            "configurable": {
                "thread_id": str(uuid.uuid4()) + str(cnt),
            }
        }
        file_path = os.path.join(data_dir, class_name + ".java")
        output_path = os.path.join(output_dir, "analysis_results", class_name + ".json")
        spec_path = os.path.join(output_dir, "specs", class_name + ".java")
        with open(file_path, "r") as f:
            code = f.read()
                
        if os.path.exists(output_path) and os.path.exists(spec_path):
            spec = open(spec_path, "r").read()
            analysis_result = json.load(open(output_path, "r"))
            if len(analysis_result["analysis_results"]) > 0 and len(spec) > 0:
                print("Skipping: {}".format(class_name))
                continue   
            
        results = generator.generate(code, class_name, config, verbose)
        with open(output_path, "w") as f:
            json.dump(results, f)
        
        with open(spec_path, "w") as f:
            f.write("// {}\n".format(results["status"]))
            if results["spec"] is not None:
                f.write(results["spec"])
            else:
                f.write("// No specification generated")
        cnt += 1
    
    generator = SpecInfer(workflow=workflow, prompt_type=prompt_type, model_name=model_name, use_docker=use_docker, language=language)
    print("Experiment completed successfully")