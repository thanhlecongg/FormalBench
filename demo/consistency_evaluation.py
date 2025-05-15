from FormalBench.evaluation import eval_consistency

success_rate, failure_rate, results = eval_consistency(
                                        spec_dir = "../tests/testcases/results/specs", # Path to the directory containing the generated specifications
                                        analysis_dir = "../tests/testcases/results/analysis_results", # Path to the directory containing the analysis results
                                        language="java", # Programming language to be used for the experiment
                                        verifier_name="OpenJML", # Name of the verifier to be used
                                        re_evaluate=False # Select whether to re-evaluate the results
                                    )
print("Success rate: ", success_rate)
print("Failure rate: ", failure_rate)