from abc import ABC, abstractmethod
from typing import Tuple
import re
import os
import docker
import atexit
from ..utils import execute_command, copy_to_container
import FormalBench

_LIB_DIR = os.path.dirname(os.path.abspath(FormalBench.__file__))

def create_verifier(name: str, version: int = 21) -> "Verifier":
    """
    Create a verifier instance

    Args:
        name (str): Name of the verifier. Currently only OpenJML is supported
        version (int, optional): Version of the verifier. Defaults to 21.

    Returns:
        Verifier: An instance of the verifier
    """
    if name == "OpenJML":
        return OpenJMLVerifier(version=version)
    elif name == "OpenJMLWithoutDocker":
        return OpenJMLVerifierWithoutDocker(version=version)
    elif name == "FramaC":
        return FramaCVerifier()
    elif name == "FramaCWithoutDocker":
        raise NotImplementedError(
            "FramaC without docker is not implemented yet. Please use FramaC with docker."
        )
    else:
        raise ValueError(
            "Unknown verifier: {}. Please select OpenJML for Java"
            .format(name))

class Verifier(ABC):
    def __init__(self) -> None:
        pass
    
    @abstractmethod
    def verify(
        self, 
        path: str, 
        timeout: int = 1800, 
        basedir: str = ""
    ) -> Tuple[int, str]:
        """
        Verify a source code file annotated formal specifciation using the verifier

        Args:
            path (str): path to the file to be verified. The path should be an .java file
            timeout (int): timeout in seconds
            basedir (str): base directory to store the file in the container. This base directory is only neccessary when the verifier is running using docker.

        Returns:
            Tuple[int, str]: A tuple containing the number of errors and the output of the verifier
        """
        pass
        
    @abstractmethod
    def extract_output(self, output: str) -> Tuple[int, str]:
        """
        Extract the number of errors from the output of the verifier

        Args:
            output (str): output message from the verifier

        Returns:
            Tuple[int, str]: A tuple containing the number of errors and the output of the verifier
        """
        pass
    

class OpenJMLVerifier(Verifier):
    
    def __init__(self, version=21) -> None:
        assert version in [21, 17], "OpenJML version must be either 21 or 17"
        self.home_dir = "/home/specInfer"
        self.image_name = "thanhlecong/openjml:latest"
        self.client = docker.from_env()
        self.container = self.client.containers.run(
            self.image_name,
                    "/bin/bash",
                    detach=True,
                    tty=True,
                    volumes={
                        os.getcwd(): {
                            "bind": self.home_dir,
                            "mode": "rw"
                        }
                    },
            )

        self.tmp_dir = os.path.join("/tmp/")
        assert self.container.status == "created", "Container failed to start"
        atexit.register(self.clean_up)
        self.openjml_version = version

    def check(
            self,
            path: str,
            basedir: str = "",
            timeout: int = 1800
        ) -> Tuple[int, str]:

        path = os.path.abspath(path)
        print("Path: {}".format(path))
        if basedir == "":
            tmp_dir = self.tmp_dir
        else:
            tmp_dir = os.path.join(self.tmp_dir, basedir)
            self.container.exec_run(["mkdir", "-p", tmp_dir])
        
        
        copy_to_container(self.container, path, tmp_dir)
        path_in_container = os.path.join(tmp_dir, os.path.basename(path))

        cmd = f"timeout {timeout} /home/openjml{self.openjml_version}/openjml --esc --prover=cvc4 --nullable-by-default --command=check --esc-max-warnings 1 {path_in_container}"

        cmd_splitted = cmd.split(" ")
        print("Executing command: {}".format(cmd))

        # Call the docker container to run the command
        exec_result = self.container.exec_run(cmd_splitted)
        if exec_result.exit_code == 124:
            tar_file = path + ".tar"
            if os.path.exists(tar_file):
                os.remove(tar_file)
            return (-1, "Timeout")
        output = exec_result.output.decode("utf-8")
        
        tar_file = path + ".tar"
        if os.path.exists(tar_file):
            os.remove(tar_file)
        return self.extract_output(output)
    
    def verify(
            self,
            path: str,
            timeout: int = 1800,
            basedir: str = ""
        ) -> Tuple[int, str]:
        
        path = os.path.abspath(path)
        print("Path: {}".format(path))
        if basedir == "":
            tmp_dir = self.tmp_dir
        else:
            tmp_dir = os.path.join(self.tmp_dir, basedir)
            self.container.exec_run(["mkdir", "-p", tmp_dir])
        
        
        copy_to_container(self.container, path, tmp_dir)
        path_in_container = os.path.join(tmp_dir, os.path.basename(path))

        cmd = f"timeout {timeout} /home/openjml{self.openjml_version}/openjml --esc --prover=cvc4 --nullable-by-default --esc-max-warnings 1 {path_in_container}"

        cmd_splitted = cmd.split(" ")
        print("Executing command: {}".format(cmd))

        # Call the docker container to run the command
        exec_result = self.container.exec_run(cmd_splitted)
        if exec_result.exit_code == 124:
            tar_file = path + ".tar"
            if os.path.exists(tar_file):
                os.remove(tar_file)
            return (-1, "Timeout")
        output = exec_result.output.decode("utf-8")
        tar_file = path + ".tar"
        if os.path.exists(tar_file):
            os.remove(tar_file)
        return self.extract_output(output)

    def extract_output(self, output: str) -> Tuple[int, str]:

        failure_count_pattern = re.compile(r"(\d+) verification failure")
        warning_count_pattern = re.compile(r"(\d+) warning")
        compilation_error_pattern = re.compile(r"(\d+) error")

        # Remove local path from the output
        print("Current working directory: {}".format(os.getcwd()))
        output = output.replace(os.getcwd() + "/", "")
        failure_match = failure_count_pattern.search(output)
        warning_match = warning_count_pattern.search(output)
        compilation_error_match = compilation_error_pattern.search(output)

        failure_count = int(failure_match.group(1)) if failure_match else 0
        warning_count = int(warning_match.group(1)) if warning_match else 0
        compilation_error_count = (int(compilation_error_match.group(1))
                                   if compilation_error_match else 0)

        if failure_match or warning_match or compilation_error_match:
            return (
                failure_count + warning_count + compilation_error_count, output
            )
        else:
            print("Output: {}".format(output))
            if "Internal JML bug" in output:
                return (-5, output)
            return (0, output)

    def clean_up(self):
        print("Cleaning up the docker container")
        self.container.stop()
        self.container.remove()
            
class OpenJMLVerifierWithoutDocker(Verifier):
    
    def __init__(self, version=21) -> None:
        assert version in [21, 17], "OpenJML version must be either 21 or 17"
        verifier_dir = os.path.abspath(os.path.join(_LIB_DIR, "../executables/verifiers/openjml{}".format(version)))
        if not os.path.exists(verifier_dir):
            os.makedirs(verifier_dir)
        self.exec_path = os.path.abspath(f"{verifier_dir}/openjml")
        if not os.path.exists(self.exec_path):
            if version == 21:
                print("Downloading OpenJML version 0.21.0-alpha-0")
                execute_command(f"wget https://github.com/OpenJML/OpenJML/releases/download/0.21.0-alpha-0/openjml-ubuntu-20.04-0.21.0-alpha-0.zip -O {verifier_dir}/openjml-ubuntu-20.04-0.21.0-alpha-0.zip")
                execute_command(f"unzip {verifier_dir}/openjml-ubuntu-20.04-0.21.0-alpha-0.zip -d {verifier_dir}/")
            elif version == 17:
                print("Downloading OpenJML version 0.17.0-alpha-12")
                execute_command(f"wget https://github.com/OpenJML/OpenJML/releases/download/0.17.0-alpha-12/openjml-ubuntu-20.04-0.17.0-alpha-12.zip -O {verifier_dir}/openjml-ubuntu-20.04-0.17.0-alpha-12.zip")
                execute_command(f"unzip {verifier_dir}/openjml-ubuntu-20.04-0.17.0-alpha-12.zip -d {verifier_dir}/")
        assert os.path.exists(self.exec_path), "OpenJML executable not found at: {}. Please download OpenJML and put into the verifier/openjml/ folder".format(self.exec_path)
        print("OpenJML executable path: {}".format(self.exec_path))
    
    def verify(
            self, 
            path: str, 
            timeout: int = 1800, 
            basedir=None
        ) -> Tuple[int, str]:
        
        abs_path = os.path.abspath(path)
        command = "{} --esc --prover=cvc4 --nullable-by-default --esc-max-warnings 1 {}".format(self.exec_path, abs_path)
        print("Executing command: {}".format(command))
        output = execute_command(command, timeout)
        print(output)
        return self.extract_output(output)
    
    def extract_output(self, output: str) -> Tuple[int, str]:
        failure_count_pattern = re.compile(r'(\d+) verification failure')
        warning_count_pattern = re.compile(r'(\d+) warning')
        compilation_error_pattern = re.compile(r'(\d+) error')
        
        #### Remove local path from the output
        print("Current working directory: {}".format(os.getcwd()))
        output = output.replace(os.getcwd() + "/", "")
        failure_match = failure_count_pattern.search(output)
        warning_match = warning_count_pattern.search(output)
        compilation_error_match = compilation_error_pattern.search(output)
        
        failure_count = int(failure_match.group(1)) if failure_match else 0
        warning_count = int(warning_match.group(1)) if warning_match else 0
        compilation_error_count = int(compilation_error_match.group(1)) if compilation_error_match else 0
        
        if failure_match or warning_match or compilation_error_match:
            # return number of failures and warnings
            return (failure_count + warning_count + compilation_error_count, output)
        elif output == "Timeout":
            return (-1, output)
        else:
            if "Internal JML bug" in output:
                return (-5, output)
            return (0, output)

class FramaCVerifier(Verifier):

    def __init__(self) -> None:
        self.home_dir = "/home/specInfer"
        self.image_name = "framac/frama-c:26.0.debian"
        self.client = docker.from_env()
        self.container = self.client.containers.run(
            self.image_name,
                    "/bin/bash",
                    detach=True,
                    tty=True,
                    volumes={
                        os.getcwd(): {
                            "bind": self.home_dir,
                            "mode": "rw"
                        }
                    },
            )

        self.tmp_dir = os.path.join("/tmp/")
        assert self.container.status == "created", "Container failed to start"
        atexit.register(self.clean_up)
        
    def verify(self,
               path: str,
               timeout: int = 1800,
               basedir: str = ""
            ) -> Tuple[str, str]:

        path = os.path.abspath(path)
        if basedir == "":
            tmp_dir = self.tmp_dir
        else:
            tmp_dir = os.path.join(self.tmp_dir, basedir)
            self.container.exec_run(["mkdir", "-p", tmp_dir])
            
        copy_to_container(self.container, path, tmp_dir)
        path_in_container = os.path.join(tmp_dir, os.path.basename(path))

        cmd = "timeout {} frama-c -wp -wp-precond-weakening -wp-no-callee-precond -warn-signed-overflow -warn-unsigned-overflow -warn-invalid-pointer -wp-model Typed+ref -wp-prover Alt-Ergo,Z3 -wp-print -wp-timeout 10 {}".format(
            timeout, path_in_container)
        cmd_splitted = cmd.split(" ")
        print("Executing command: {}".format(cmd))

        # Call the docker container to run the command
        exec_result = self.container.exec_run(cmd_splitted)
        if exec_result.exit_code == 124:
            tar_file = path + ".tar"
            if os.path.exists(tar_file):
                os.remove(tar_file)
            return (-1, "Timeout")
        output = exec_result.output.decode("utf-8")
        
        tar_file = path + ".tar"
        if os.path.exists(tar_file):
            os.remove(tar_file)
        return self.extract_output(output)

    def extract_output(self, output: str) -> Tuple[str, str]:

        # Convert from bytes to a list of strings (split by newline characters).
        result_type = "UK"
        context = output.split("\n")
        # Iterate through each line in the context.
        timeout_in_requires = 0
        all_timeout = 0
        for line in context:
            # If the line contains the string "[kernel] Frama-C aborted:", then the
            # build is invalid.
            if ("[kernel] Frama-C aborted:" in line
                    or "[kernel] Plug-in wp aborted" in line
                    or "[wp] Warning: No goal generated" in line
                    or "error: invalid preprocessing directive" in line):
                result_type = "SyntaxError"
                break
            elif "[wp] [Timeout] typed_" in line:
                if ("_requires (" in line or "_requires_" in line):
                    timeout_in_requires += 1
                all_timeout += 1
                continue
            # If the line contains the string "[wp] Proved goals:", then the build
            # is valid. The number of proved goals is given in the form "x/y",
            # where x is the number of proved goals and y is the number of total
            # goals. If x == y, then the build is a pass. Otherwise, the build is
            # a fail.
            elif "[wp] Proved goals:" in line:
                proportion = line.split(":")[-1]
                left, right = proportion.split("/")
                left = left.strip()
                right = right.strip()
                if int(left) + int(timeout_in_requires) == int(right):
                    result_type = "Pass_" + left + "_" + right
                else:
                    result_type = "Fail_" + left + "_" + right
                break
        if result_type.startswith("Pass"):
            return [0, output]
        elif result_type.startswith("Fail"):
            n_errors = int(right) - int(left) - all_timeout
            assert n_errors >= 0, "Number of errors should be greater than or equal to 0"
            if n_errors == 0:
                return [-1, output]
            return [n_errors, output]
        elif result_type == "SyntaxError":
            return [999, output]
        elif "Unexpected error" in output and "Please report as 'crash' at https://git.frama-c.com/pub/frama-c/issues" in output:
            return [-5, "Internal Frama-C bug"]
        else:
            assert output == "Timeout", "Unknown output: {}".format(output)
            return [-1, output]
    
    def clean_up(self):
        print("Cleaning up the docker container")
        self.container.stop()
        self.container.remove()