import re

def extract_errors(error_message):
    pattern = r'(/tmp/[^:]+:\d+: )(\w+):'
    matches = re.split(r'(?=/tmp/[^:]+:\d+: \w+:)', error_message)
    errors = []
    for i, match in enumerate(matches, start=1):
        if match.strip(): 
            level_match = re.search(pattern, match)
            if level_match:
                error_level = level_match.group(2)  # Capture the error level
                if error_level != "warning":
                    if "Associated declaration:" in match or "Associated method exit" in match:
                        if len(errors) == 0:
                            continue
                        errors[-1] = (errors[-1][0], errors[-1][1] + match)
                    else:
                        errors.append((error_level, match.strip()))
    return errors

def verification_failure_map(error_message):
    if "The prover cannot establish an assertion (LoopInvariantBeforeLoop)" in error_message:
        return "LoopInvariantFailure"
    elif "The prover cannot establish an assertion (ArithmeticOperationRange)" in error_message:
        return "ArithmeticOperationRange"
    elif "The prover cannot establish an assertion (Assignable" in error_message:
        return "AssignableFailure"
    elif "The prover cannot establish an assertion (Postcondition:" in error_message:
        return "PostconditionFailure"
    elif "The prover cannot establish an assertion (Assert)" in error_message:
        return "AssertFailure"
    elif "The prover cannot establish an assertion (UndefinedNullDeReference)" in error_message:
        return "NullDeReference"
    elif "The prover cannot establish an assertion (PossiblyNullDeReference)" in error_message:
        return "NullDeReference"
    elif "The prover cannot establish an assertion (LoopInvariant)" in error_message:
        return "LoopInvariantFailure"
    elif "The prover cannot establish an assertion (PossiblyNegativeIndex)" in error_message:
        return "ArrayIndex"
    elif "The prover cannot establish an assertion (PossiblyNegativeSize)" in error_message:
        return "NegativeSize"
    elif "The prover cannot establish an assertion (PossiblyTooLargeIndex)" in error_message:
        return "ArrayIndex"
    elif "The prover cannot establish an assertion (LoopDecreases)" in error_message:
        return "RankingFunctionFailure"
    elif "The prover cannot establish an assertion (PossiblyBadArrayAssignment)" in error_message:
        return "BadArrayAssignment"
    elif "The prover cannot establish an assertion (Precondition:" in error_message:
        return "PreconditionFailure"
    elif "Precondition conjunct is false:" in error_message:
        return "PreconditionFailure"
    elif "The prover cannot establish an assertion (UndefinedTooLargeIndex)" in error_message:
        return "ArrayIndex"
    elif "The prover cannot establish an assertion (PossiblyDivideByZero)" in error_message:
        return "DivideByZero"
    elif "The prover cannot establish an assertion (PossiblyBadCast)" in error_message:
        return "BadCast"
    elif "The prover cannot establish an assertion (UndefinedDivideByZero" in error_message:
        return "DivideByZero"
    elif "The prover cannot establish an assertion (ExceptionalPostcondition:" in error_message:
        return "ExceptionalPostconditionFailure"
    elif "The prover cannot establish an assertion (UndefinedCalledMethodPrecondition:" in error_message:
        return "CalledMethodPrecondition"
    elif "The prover cannot establish an assertion (UndefinedNegativeIndex)" in error_message:
        return "ArrayIndex"
    elif "The prover cannot establish an assertion (PossiblyNullUnbox) " in error_message:
        return "NullUnbox"
    elif "The prover cannot establish an assertion (LoopDecreasesNonNegative)" in error_message:
        return "RankingFunctionFailure"
    elif "The prover cannot establish an assertion (Postcondition)" in error_message:
        return "PostconditionFailure"
    elif "The prover cannot establish an assertion (ArithmeticCastRange)" in error_message:
        return "ArithmeticCastRange"
    elif "The prover cannot establish an assertion (UndefinedNullUnbox)" in error_message:
        return "NullUnbox"
    elif "The prover cannot establish an assertion (PossiblyLargeShift" in error_message:
        return "LargeShift"

    
    raise ValueError(f"Unknown verification failure: {error_message}")

def error_map(error_message):
    return "SyntaxError"
    
def classify_failures(error_level, error_message):
    if error_level == "error":
        return error_map(error_message)
    elif error_level == "verify":
        return verification_failure_map(error_message)
    else:
        raise ValueError(f"Unknown error level: {error_level}")

