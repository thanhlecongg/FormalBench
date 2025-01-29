import subprocess
import psutil
import os
import tarfile
import io

def kill_process_tree(pid):
    try:
        parent = psutil.Process(pid)
        for child in parent.children(recursive=True):
            child.kill()
        parent.kill()
    except psutil.NoSuchProcess:
        pass


def execute_command(command, timeout=None):
    try:
        process = subprocess.Popen(command,
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        try:
            output, error = process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            kill_process_tree(process.pid)
            return "Timeout"

        if process.returncode != 0:
            if error:
                return error.decode("utf-8")
            if output:
                return output.decode("utf-8")
            assert False, "Command failed with no output"
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        return e.output.decode("utf-8")

def copy_to_container(container, src: str, dest: str) -> None:
    src_dir = os.path.dirname(src)
    print("src_dir: {}".format(src_dir))
    src_name = os.path.basename(src)
    tar_path = src + '.tar'
    
    with tarfile.open(tar_path, mode='w') as tar:
        tar.add(src, arcname=src_name)

    with open(tar_path, 'rb') as f:
        data = f.read()
        container.put_archive(dest, data)
        
def copy_from_container(container, src: str, dest: str) -> str:
    data, stat = container.get_archive(src)
    file_like_object = io.BytesIO()
    for chunk in data:
        file_like_object.write(chunk)
    file_like_object.seek(0)
    with tarfile.open(fileobj=file_like_object) as tar:
        tar.extractall(path=dest)
    return dest

def execute_command_in_container(container, cmd: str) -> str:
    exec_result = container.exec_run(cmd.split(" "))
    return exec_result.output.decode("utf-8")