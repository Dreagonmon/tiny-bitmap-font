
import sys, os, shutil
from subprocess import run
_this_script_folder = os.path.abspath(os.path.dirname(__file__))

PYTHON = sys.executable
HOOK_FOLDER = os.path.join(_this_script_folder, "git-hook")
HOOK_TARGET_FOLDER = os.path.join(_this_script_folder, ".git", "hooks")

if __name__ == "__main__":
    run([PYTHON, "-m", "pip", "install", "gitpython"])
    shutil.copy2(os.path.join(HOOK_FOLDER, "pre-commit"), HOOK_TARGET_FOLDER)
