import os
from FormalBench.evaluation import create_verifier, create_mutator, eval_consistency, eval_completeness


def test_create_verifier():
    assert create_verifier("OpenJML", 21)
    assert create_verifier("OpenJML", 17)
    assert create_verifier("OpenJMLWithoutDocker", 17)
    assert create_verifier("OpenJMLWithoutDocker", 21)
    try: 
        create_verifier("OpenJML", 22)
    except AssertionError as e:
        assert str(e) == "OpenJML version must be either 21 or 17"
    except:
        assert False
    
    try:
        create_verifier("OpenJMLWithoutDocker", 22)
    except AssertionError as e:
        assert str(e) == "OpenJML version must be either 21 or 17"
    except:
        assert False
    
    try:
        create_verifier("Unknown")
    except ValueError as e:
        assert str(e) == "Unknown verifier: Unknown. Please select OpenJML for Java"
    except:
        assert False

def test_verifier():
    verifier = create_verifier("OpenJML", 21)
    n_errors, output = verifier.verify("tests/testcases/specs/Absolute.java")
    assert n_errors == 0, "No errors should be found"
    assert output == "", "No output should be found"
    
    n_errors, output = verifier.verify("tests/testcases/specs/Absolute_wrong.java")
    assert n_errors > 0, "Errors should be found"
    assert len(output) > 0, "Output should be found"
    
    n_errors, output = verifier.verify("tests/testcases/specs/Absolute_wrong.java", timeout=1)
    assert n_errors == -1, "Timeout should be returned"
    assert output == "Timeout", "Timeout should be returned"
    
    assert not os.path.exists("tests/testcases/specs/Absolute_wrong.java.tar"), "Local tar file should be deleted"
    assert not os.path.exists("tests/testcases/specs/Absolute.java.tar"), "Local tar file should be deleted"
    
def test_mutation_analysis():
    create_mutator("Major")
    create_mutator("MajorWithoutDocker")
    
def test_consistency():
    success_rate, failure_rate, results = eval_consistency("tests/testcases/results/specs", "tests/testcases/results/analysis_results")
    assert success_rate == 0.25, "Success rate should be 0.5"
    assert failure_rate == 0.5, "Failure rate should be 0.5"
    
    try: 
        eval_consistency("tests/testcases/results/specs1", "tests/testcases/results/analysis_results")
    except AssertionError as e:
        assert str(e) == "Spec directory does not exist"
    except:
        assert False
        
    try:
        eval_consistency("", "", language="python")
    except ValueError as e:
        assert str(e) == "Unknown language: python. Please select ['java']"
    except:
        assert False
        
    try:
        eval_consistency("", "", language="java", verifier_name="Unknown")
    except AssertionError as e:
        assert str(e) == "Only OpenJML is supported for Java programs"
    except:
        assert False
        
def test_completeness():
    avg_coverage, coverage_results, inconsistent_instances = eval_completeness("tests/testcases/results/specs", "tests/testcases/results/completeness", timeout=20)
    assert len(inconsistent_instances) == 3, "Three inconsistent specifications should be found"
    assert avg_coverage == 1.0, "Average coverage should be 1.0"
    
    try:
        eval_completeness("tests/testcases/results/specs1", "tests/testcases/results/completeness")
    except AssertionError as e:
        assert str(e) == "Data directory not found: tests/testcases/results/specs1"
    except:
        assert False
    
    try:
        eval_completeness("tests/testcases/results/specs", "tests/testcases/results/completeness", language="python")
    except ValueError as e:
        assert str(e) == "Unsupported language: python. Please select from ['java']"
    except:
        assert False
    