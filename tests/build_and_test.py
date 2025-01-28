import os
from FormalBench.evaluation import create_verifier

def test_create_verifier():
    assert create_verifier("OpenJML", 21)
    assert create_verifier("OpenJML", 17)
    assert create_verifier("OpenJMLWithoutDocker", 17)
    assert create_verifier("OpenJMLWithoutDocker", 21)
    try: 
        create_verifier("OpenJML", 22)
    except AssertionError as e:
        assert str(e) == "OpenJML version must be either 21 or 17"
    else:
        assert False
    
    try:
        create_verifier("OpenJMLWithoutDocker", 22)
    except AssertionError as e:
        assert str(e) == "OpenJML version must be either 21 or 17"
    else:
        assert False
    
    try:
        create_verifier("Unknown")
    except ValueError as e:
        assert str(e) == "Unknown verifier: Unknown. Please select OpenJML for Java"
    else:
        assert False

def test_verifier():
    verifier = create_verifier("OpenJML", 21)
    n_errors, output = verifier.verify("tests/testcases/Absolute.java")
    assert n_errors == 0, "No errors should be found"
    assert output == "", "No output should be found"
    
    n_errors, output = verifier.verify("tests/testcases/Absolute_wrong.java")
    assert n_errors > 0, "Errors should be found"
    assert len(output) > 0, "Output should be found"
    
    n_errors, output = verifier.verify("tests/testcases/Absolute_wrong.java", timeout=0.001)
    assert n_errors == -1, "Timeout should be returned"
    assert output == "Timeout", "Timeout should be returned"
    
    assert not os.path.exists("tests/testcases/Absolute_wrong.java.tar"), "Local tar file should be deleted"
    assert not os.path.exists("tests/testcases/Absolute.java.tar"), "Local tar file should be deleted"
    
    
