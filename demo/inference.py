from FormalBench.experiments import base_experiment

base_experiment(
    data_dir="../c-dataset", # Path to directory containing the dataset
    model_name="gpt-4o", # Name of the model to be used
    use_remote=False, # Select whether to use remote dataset or local directory
    language="c", # Programming language to be used for the experiment
    output_dir="../results/gpt4o", # Directory to save the output files
    prompt_type="zero_shot", # Type of prompt to be used for inference
    tmp_dir="../tmp/gpt4o", # Temporary directory for storing intermediate files
)