from FormalBench.evaluation import eval_completeness


avg_coverage, coverage_results, inconsistent_instances = eval_completeness(
                                        spec_dir = "../results/main/o3-mini-high/specs", # path to the directory containing the specs
                                        analysis_dir= "../results/main/o3-mini-high/analysis_results", # path to the directory containing the analysis results
                                        save_dir = "../results/main/o3-mini-high/completeness", # path to the directory where the results will be saved
                                        timeout= 300
                                    )

print("Average coverage: ", avg_coverage)