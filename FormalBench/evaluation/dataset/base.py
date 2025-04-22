from huggingface_hub import snapshot_download
import os
import json

def load_base_dataset():
    print("Loading Formal-Base dataset")
    local_dir = snapshot_download("FormalBench/FormalBench", repo_type="dataset")
    print("Downloaded dataset successfully, storing in local directory: ", local_dir)
    data_dir = os.path.join(local_dir, "base")
    meta_path = os.path.join(data_dir, "meta_data.jsonl")
    meta_data = {}
    with open(meta_path, "r") as f:
        for line in f:
            data = json.loads(line)
            class_name = data["class_name"]
            meta_data[class_name] = data
            meta_data[class_name]["local_path"] = os.path.join(data_dir, class_name + ".java")
    
    print("Base dataset loaded !!!")
    return meta_data    