import os

from backend.sheet import Sheet


class SheetDirectory:

    def __init__(self, directory):
        for name in os.listdir(directory):
            path = os.path.join(directory, name)

            if os.path.isdir(path):
                key = name.replace(" ", "_")
                value = SheetDirectory(path)
            elif name.endswith(".json"):
                key = name[:-5].replace(" ", "_")
                value = path
            else:
                continue
            setattr(self, key, value)

    def __getattribute__(self, key):
        value = super().__getattribute__(key)
        if isinstance(value, str):
            value = Sheet(value)
            self.__setattr__(key, value)
        return value
