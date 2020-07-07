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


class Context:

    __globals__ = None
    __cur_con__ = None

    @staticmethod
    def _set_globals(global_dict):
        if Context.__cur_con__ is None:
            Context.__globals__ = global_dict
        else:
            cur_con = Context.__cur_con__
            cur_con.exit()
            Context.set_globals(global_dict)
            cur_con.enter()

    @staticmethod
    def _exit_current():
        if Context.__cur_con__ is not None:
            Context.__cur_con__.exit()

    def __setattr__(self, key, value):
        self.__dict__[key] = value
        if Context.__cur_con__ is self:
            Context.__globals__[key] = value

    def __delattr__(self, key):
        del self.__dict__[key]
        if Context.__cur_con__ is self:
            del Context.__globals__[key]

    def _enter(self):
        if Context.__globals__ is None:
            raise RuntimeError("Reference to globals dict not set. "
                               'Try running "Context.set_globals(globals())".')
        if Context.__cur_con__ is not None:
            raise RuntimeError("You already are in a context. Leave it before "
                               "entering a new one.")

        for key, value in self.__dict__.items():
            Context.__globals__[key] = value
        Context.__cur_con__ = self

    def __enter__(self):
        self._enter()
        return self

    def _exit(self):
        if Context.__cur_con__ is not self:
            raise RuntimeError("You are not in this context, "
                               "you can't leave it.")

        for key in self.__dict__:
            del Context.__globals__[key]
        Context.__cur_con__ = None

    def __exit__(self, type, value, traceback):
        self._exit()


if __name__ == "__main__":
    Context.set_globals(globals())
