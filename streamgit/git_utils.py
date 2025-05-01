import subprocess
import os
import shutil

def run_cmd(cmd):
    try:
        out = subprocess.getoutput(cmd + " 2>&1")
        success = "fatal:" not in out.lower() and "error" not in out.lower()
        return {"cmd": cmd, "output": out, "success": success}
    except Exception as e:
        return {"cmd": cmd, "output": str(e), "success": False}

def init_repo(path="."):
    return run_cmd(f"git init {path}")

def remove_git(path="."):
    git_dir = os.path.join(path, ".git")
    if os.path.isdir(git_dir):
        try:
            shutil.rmtree(git_dir)
            return {"cmd": f"rm -rf {git_dir}", "output": ".git removed", "success": True}
        except Exception as e:
            return {"cmd": f"remove {git_dir}", "output": str(e), "success": False}
    return {"cmd": "", "output": "No .git folder found", "success": False}

def clone_repo(url, target_dir=".", path="."):
    return run_cmd(f"git clone {url} {target_dir}")

def status(path="."):
    return run_cmd("git status")

def status_porcelain(path="."):
    res = run_cmd("git status --porcelain")
    files = []
    for line in res["output"].splitlines():
        line = line.strip()
        if not line:
            continue
        # Porcelain output format: 2-letter status + space + filename
        # Example: '?? new.py' or ' M modified.py'
        filename = line[3:].strip()  # Strip the 2-char status and the space
        files.append(filename)
    return {"cmd": res["cmd"], "files": files, "success": res["success"]}

def stage_files(files, path="."):
    if not files:
        return {"cmd": "", "output": "No files selected", "success": False}
    return run_cmd(f"git add {' '.join(files)}")

def commit(message, path="."):
    return run_cmd(f'git commit -m "{message}"')

def get_current_branch(path="."):
    return run_cmd("git rev-parse --abbrev-ref HEAD")

def push(remote="origin", branch=None, path="."):
    if branch is None:
        branch = get_current_branch()["output"].strip()
    return run_cmd(f"git push {remote} {branch}")

def pull(remote="origin", branch=None, path="."):
    if branch is None:
        branch = get_current_branch()["output"].strip()
    return run_cmd(f"git pull {remote} {branch}")

def add_remote(name, url, path="."):
    return run_cmd(f"git remote add {name} {url}")

def list_branches(path="."):
    return run_cmd("git branch --all")

def checkout(branch, path="."):
    return run_cmd(f"git checkout {branch}")

def create_branch(branch, path="."):
    return run_cmd(f"git checkout -b {branch}")

def merge(branch, path="."):
    return run_cmd(f"git merge {branch}")

def stash(path="."):
    return run_cmd("git stash")

def stash_apply(path="."):
    return run_cmd("git stash apply")

def log(path="."):
    return run_cmd("git log --oneline --graph --decorate -n 20")
