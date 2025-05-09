from FormalBench.evaluation import eval_consistency

success_rate, failure_rate, results = eval_consistency(
                                        spec_dir = "../results/gpt4o/specs", # Path to the directory containing the generated specifications
                                        analysis_dir = "../results/gpt4o/analysis_results", # Path to the directory containing the analysis results
                                        language="c", # Programming language to be used for the experiment
                                        verifier_name="FramaC", # Name of the verifier to be used
                                        re_evaluate=False # Select whether to re-evaluate the results
                                    )
print("Success rate: ", success_rate)
print("Failure rate: ", failure_rate)