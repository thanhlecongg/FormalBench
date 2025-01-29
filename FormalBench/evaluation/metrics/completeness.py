from .. import create_verifier, Verifier, create_mutator, MutantGenerator
import os
import concurrent.futures
from typing import Tuple, List, Optional

class CoverageScore():

    def __init__(self, verifier: Verifier, mutator: MutantGenerator) -> None:
        super().__init__()
        self.verifier = verifier
        self.mutator = mutator

    def measure_completeness(
            self, 
            path: str, 
            save_dir: str,
            n_proc: int, 
            timeout: int
        ) -> Tuple[Optional[float], Optional[int], Optional[int]]:
        
        results, n_mutants = self.mutation_analysis(path, save_dir, n_proc, timeout)

        if n_mutants is None:
            print("[WARNING] No mutants generated. Skipping !!!")
            return 1, 0, 0

        if results["Original"] != 0:
            print("Original specification is unsound. Skipping !!!")
            return None, None, None

        total_mutants = 0
        killed_mutants = 0
        survived_mutants = 0

        for mutant, n_errors in results.items():
            if mutant == "Original":
                continue
            total_mutants += 1
            if n_errors == 0:
                killed_mutants += 1
            else:
                survived_mutants += 1
        assert total_mutants == n_mutants, "Total mutants should be equal to the number of mutants generated"

        coverage = survived_mutants / total_mutants
        return coverage, survived_mutants, total_mutants

    def load_results(self, result_path: str) -> dict:
        results = {}
        assert os.path.exists(result_path), "Result file not found: {}".format(
            result_path)
        with open(result_path, "r") as f:
            for line in f:
                splits = line.split(":")
                if len(splits) < 2:
                    continue
                n_errors = int(splits[1].strip())
                ID = splits[0].strip()
                results[ID] = n_errors
        return results

    def mutation_analysis(
            self, 
            path: str, 
            save_dir: str,
            n_proc: int, 
            timeout: int
        ) -> Tuple[dict, Optional[int]]:
        
        print("Measuring mutation score for path: {}".format(path))
        mutation_dir = os.path.join(save_dir, "mutants")

        if not os.path.exists(mutation_dir) or len(
                os.listdir(mutation_dir)) == 0:
            self.mutator.generate_mutants(path, save_dir)
            basename = os.path.basename(path)

            if not os.path.exists(mutation_dir):
                print("Mutants directory not found. Exiting !!!")
                return {}, None

        n_mutants = len(os.listdir(mutation_dir))

        if n_mutants == 0:
            print("No mutants generated. Exiting !!!")
            return {}, None

        result_path = os.path.join(save_dir, "completeness.txt")

        if os.path.exists(result_path):
            results = self.load_results(result_path)
            if len(results) == n_mutants + 1 or results.get("Original",
                                                            0) != 0:
                print("Results already computed. Skipping !!!")
                return results, n_mutants

        results = {}
        f = open(result_path, "w")
        n_errors, _ = self.verifier.verify(path=path, basedir="", timeout=timeout)
        
        f.write(f"Original: {n_errors}\n")
        
        results["Original"] = n_errors
        
        if n_errors != 0:
            print("[WARNING] Original specification is unsound. Skipping !!!")
            f.close()
            return results, n_mutants
        assert n_errors == 0, "Original specification should be verified: {}".format(
            path)

        basename = os.path.basename(path)
        with concurrent.futures.ThreadPoolExecutor(
                max_workers=n_proc) as executor:
            futures = {
                executor.submit(self.verify_mutant, mutant, mutation_dir, basename, timeout):
                mutant
                for i, mutant in enumerate(os.listdir(mutation_dir))
            }
            for future in concurrent.futures.as_completed(futures):
                mutant, n_errors = future.result()
                f.write(f"{mutant}: {n_errors}\n")
                results[mutant] = n_errors
        f.close()

        return results, n_mutants

    def verify_mutant(
        self, 
        mutant: str, 
        mutation_dir: str,
        basename: str, 
        timeout: int
    ) -> Tuple[str, int]:
        
        mutant_path = os.path.join(mutation_dir, mutant, basename)
        print("Verifying mutant: {}".format(mutant_path))
        n_errors, output = self.verifier.verify(path=mutant_path,
                                                basedir=mutant,
                                                timeout=timeout)
        print("Output", output)
        print("Errors: {}".format(n_errors))
        return mutant, n_errors
    
def eval_completeness(
        data_dir: str,
        save_dir: str,
        verifier_name: str = "OpenJML",
        verifier_version: int = 21,
        n_proc: int = 8,
        language: str = "java", 
        data_ids: Optional[str] = None,
        timeout: int = 300
    ) -> Tuple[float, List[float]]:
    
    assert os.path.exists(data_dir), "Data directory not found: {}".format(data_dir)
    
    os.makedirs(save_dir, exist_ok=True)
    if language == "java":
        assert verifier_name == "OpenJML", "Only OpenJML is supported for Java programs"
        ending = ".java"
        verifier = create_verifier(verifier_name, verifier_version)
        mutator = create_mutator("Major")
    else:
        raise ValueError("Unsupported language: {}. Please select from ['java']".format(language))
    
    if data_ids is None:
        benchmarks = os.listdir(data_dir)
        benchmarks = [file_name[:-len(ending)] for file_name in benchmarks if file_name.endswith(ending)]
    else:
        benchmarks = data_ids.split(",")

    coverage_results = []
    unsound = 0
    for b in benchmarks:
        coverage_score = CoverageScore(verifier, mutator)
        coverage, survived, total = coverage_score.measure_completeness(
            os.path.join(data_dir, f"{b}{ending}"),
            os.path.join(save_dir, b), n_proc, timeout)
        if coverage is None:
            unsound += 1
            print(f"Skipping {b}")
            continue
        coverage_results.append(coverage)
    
    print("Completeness evaluation completed")
    print("Unsound: {}".format(unsound))
    avg_coverage = sum(coverage_results) / len(coverage_results)
    print("Average completeness: {:.2f}".format(avg_coverage))
    
    return avg_coverage, coverage_results