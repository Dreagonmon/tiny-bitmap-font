import sys, os

_env_script_folder = os.path.abspath(os.path.dirname(__file__))
ROOT_FOLDER = os.path.abspath(os.path.join(_env_script_folder, '..'))

def ensure_import_path():
    # sys.path.append(_env_script_folder)
    sys.path.append(os.path.join(ROOT_FOLDER, "src"))
    # add more lib path...
    pass
