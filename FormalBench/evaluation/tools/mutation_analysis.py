from abc import ABC, abstractmethod
import os
import atexit
import docker
from ..utils import (
    execute_command, 
    copy_to_container, 
    copy_from_container
)

import FormalBench

_LIB_DIR = os.path.dirname(os.path.abspath(FormalBench.__file__))

def create_mutator(name: str) -> "MutantGenerator":
    """
    Create a code mutator instance

    Args:
        name (str): Name of the code mutator

    Raises:
        ValueError: If the mutator is not supported

    Returns:
        MutantGenerator: A code mutator instance
    """
    if name == "Major":
        return MajorMutantGenerator()
    elif name == "MajorWithoutDocker":
        return MajorMutantGeneratorWithoutDocker()
    else:
        raise ValueError(
            "Unknown mutator: {}. Please select Major for Java programs"
            .format(name)
        )

class MutantGenerator(ABC):

    def __init__(self) -> None:
        """
        Create a new code mutator instance

        Args:
            home_dir (_type_): Path to the home directory of the container
            image_name (_type_): Name of the docker image
            environment (_type_, optional): Environment variables for the container. Defaults to None.
        """
        pass
    
    @abstractmethod
    def generate_mutants(self, path: str, out_dir: str):
        """
        Generate mutants for a given program

        Args:
            path (str): Path to the program
            out_dir (str): Path to the output directory
        """
        pass

class MajorMutantGenerator(MutantGenerator):

    def __init__(self) -> None:
        self.tmp_dir = os.path.join("/tmp/")
        self.config_path = os.path.join(self.tmp_dir, "major.mml.bin")
        
        self.home_dir = "/home/specInfer"
        self.image_name = "thanhlecong/major:latest"
        self.client = docker.from_env()
        self.container = self.client.containers.run(
            self.image_name,
            "/bin/bash",
            detach=True,
            tty=True,
            volumes={os.getcwd(): {
                         'bind': self.home_dir,
                         'mode': 'rw'
                     }},
            environment=None
        )
        
        assert self.container.status == "created", "Container failed to start"
        atexit.register(self.clean_up)
        
        self.executable_path = "/home/major/bin/major"
        local_config_path = os.path.abspath(os.path.join(_LIB_DIR, "config/major.mml.bin"))
        assert os.path.exists(
            local_config_path
        ), "MML file not found at: {}. Please re-download our package.".format(
            local_config_path)

        copy_to_container(self.container, local_config_path, self.tmp_dir)

    def generate_mutants(self, path: str, out_dir: str):
        os.makedirs(out_dir, exist_ok=True)
        
        file_name = os.path.basename(path)
        copy_to_container(self.container, path, self.tmp_dir)
        path_in_container = os.path.join(self.tmp_dir, file_name)

        ""
        cmd = "{} --mml {} {} --export export.mutants".format(
            self.executable_path, self.config_path, path_in_container)
        cmd_splitted = cmd.split(" ")
        print("Executing command: {}".format(cmd))

        exec_result = self.container.exec_run(cmd_splitted)
        output = exec_result.output.decode("utf-8")
        print(output)
        
        exec_result = self.container.exec_run("ls /mutants")
        if exec_result.exit_code != 0:
            print("[WARNING]: No mutants generated")
            return
        
        copy_from_container(self.container, "/mutants", out_dir)
        
        self.container.exec_run("rm -rf {}".format(path_in_container, path_in_container))
        
        self.container.exec_run("rm -rf /mutants")
    
    def clean_up(self):
        """
        Clean up the docker container and temporary files
        """
        
        print("Cleaning up the docker container")
        self.container.stop()
        self.container.remove()
        if os.path.exists(os.path.abspath(os.path.join(_LIB_DIR, "config/major.mml.bin.tar"))):
            os.remove(os.path.abspath(os.path.join(_LIB_DIR, "config/major.mml.bin.tar")))

class MajorMutantGeneratorWithoutDocker(MutantGenerator):

    def __init__(self) -> None:
        super().__init__()
        major_dir = os.path.abspath(os.path.join(_LIB_DIR, "../executables/mutators/"))
        os.makedirs(major_dir, exist_ok=True)
        self.executable_path = os.path.abspath(f"{major_dir}/major/bin/major")
        if not os.path.exists(self.executable_path):
            execute_command(f"wget http://mutation-testing.org/major-latest.zip -O {major_dir}/major-latest.zip")
            execute_command(f"unzip {major_dir}/major-latest.zip -d {major_dir}")

        assert os.path.exists(
            self.executable_path
        ), "Major executable not found at: {}. Please download Major v.3.0.1 and put into the mutators/ folder".format(
            self.executable_path)
        
        self.config_path = os.path.abspath(os.path.join(_LIB_DIR, "config/major.mml.bin"))
        
        assert os.path.exists(
            self.config_path
        ), "MML file not found at: {}. Please re-download our package.".format(
            self.config_path)
        
        self.executable_cmd = "{} --mml {} {} --export export.mutants"
    
    def generate_mutants(self, path: str, out_dir: str):
        os.makedirs(out_dir, exist_ok=True)
        execute_command("cp {} {}".format(os.path.abspath(path), out_dir))

        absolute_path = os.path.join(os.path.abspath(out_dir),
                                     os.path.basename(path))
        current_dir = os.getcwd()
        os.chdir(out_dir)
        command = self.executable_cmd.format(self.executable_path,
                                             self.config_path, absolute_path)
        output = execute_command(command)
        print(output)
        os.chdir(current_dir)
