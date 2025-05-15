from FormalBench.evaluation import eval_completeness


avg_coverage, coverage_results, inconsistent_instances = eval_completeness(
                                        spec_dir = "../tests/testcases/results/specs", # path to the directory containing the specs
                                        analysis_dir= "../tests/testcases/results/analysis_results", # path to the directory containing the analysis results
                                        save_dir = "../tests/testcases/results/completeness", # path to the directory where the results will be saved
                                        language="java", # programming language to be used for the experiment
                                        n_proc= 8, # number of processes to be used for the experiment
                                        timeout= 300
                                    )

print("Average coverage: ", avg_coverage)