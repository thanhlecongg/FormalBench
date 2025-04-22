from huggingface_hub import snapshot_download
import os
import json

def load_diverse_dataset():
    print("Loading Formal-Diverse dataset")
    local_dir = snapshot_download("FormalBench/FormalBench", repo_type="dataset")
    print("Downloaded dataset successfully, storing in local directory: ", local_dir)
    data_dir = os.path.join(local_dir, "diverse")
    meta_path = os.path.join(data_dir, "natural.json")
    score_path = os.path.join(data_dir, "scores.txt")
    meta_data = {}
    with open(meta_path, "r") as f:
        meta_data = json.load(f)
        print(meta_data.keys())
        exit()
    
    print("Base dataset loaded !!!")
    return meta_data    
