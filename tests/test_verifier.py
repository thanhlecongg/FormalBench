from FormalBench.evaluation.tools.verifier import create_verifier

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
