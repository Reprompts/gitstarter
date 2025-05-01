import subprocess
import os


def git_installed():
    res = subprocess.getoutput("git --version 2>&1")
    return res.startswith("git version")


def is_git_repo(path="."):
    return os.path.isdir(os.path.join(path, ".git"))

def has_python_files(path="."):
    for root, _, files in os.walk(path):
        if any(f.endswith(".py") for f in files):
            return True
    return False
