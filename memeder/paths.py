import os
from pathlib import Path


def get_py_lib_path():
    return Path('/'.join(os.path.abspath(__file__).split('/')[:-1]))


def get_lib_root_path():
    return Path('/'.join(os.path.abspath(__file__).split('/')[:-2]))
