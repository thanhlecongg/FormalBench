from huggingface_hub import snapshot_download
import os
import json

def load_diverse_dataset(data_dir=None, use_remote=True):
    print("Loading Formal-Diverse dataset")
    assert data_dir is not None or use_remote, "local_dir should be None when use_remote is True"
    
    if data_dir is None:
        local_dir = snapshot_download("FormalBench/FormalBench", repo_type="dataset")
        print("Downloaded dataset successfully, storing in local directory: ", local_dir)
        data_dir = os.path.join(local_dir, "diverse")
        
    meta_path = os.path.join(data_dir, "natural.json")
    formatted_meta_data = {}
    with open(meta_path, "r") as f:
        meta_data = json.load(f)
        for data_id in meta_data:
            for rule_id, class_name in meta_data[data_id]:
                file_path = os.path.join(data_dir, rule_id, class_name + ".java")
                assert os.path.exists(file_path), f"File {file_path} does not exist"
                formatted_meta_data["{}--{}--{}".format(data_id, rule_id, class_name)] = {
                    "class_name": class_name,
                    "local_path": file_path
                }
    
    print("Diverse dataset loaded !!!")
    return formatted_meta_data, data_dir  
