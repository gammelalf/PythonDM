import json
import os
import sys


def real_path(path):
    """
    Make a path who is relative to this project's directory
    relative to the current working directory.
    """
    return os.path.join(os.path.dirname(sys.argv[0]), path)


def json_load(path):
    """
    Load a json file.

    The `path` is relative to the project's folder.
    """
    with open(real_path(path)) as f:
        return json.load(f)
