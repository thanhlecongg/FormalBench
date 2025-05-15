from FormalBench.evaluation import create_verifier

# Create a verifier`
verifier = create_verifier(
    name="OpenJML",  # Name of the verifier. Please select from ["OpenJML", "FramaC"]
)

# Specify the path to the Java file
java_file_path = "../tests/testcases/results/specs/AccessElements.java"  # Replace with the actual path to your Java file

# Specify the timeout in seconds
n_errors, output = verifier.verify(
    path=java_file_path,
    timeout=300,  # Timeout in seconds
)

print("Number of errors:", n_errors)
print("Output:", output)