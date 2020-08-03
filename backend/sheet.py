import os

from .character import Character
from .util import json_load


class Sheet(object):

    def __init__(self, path=None):
        self.__path = path

        self.name = ""

        self.hp = 0
        self.ac = 10

        self.str = 0
        self.dex = 0
        self.con = 0
        self.int = 0
        self.wis = 0
        self.cha = 0

        self.skills = {}

        if path is not None:
            self.__dict__.update(json_load(path))
        self.skills = Skills(self)
        #self.saving_throws = SavingThrows(self)

    def __repr__(self):
        return f"Sheet({self.__path})"

    def __str__(self):
        return f"""
        """

    def __rmul__(self, n):
        """
        Syntactic sugar for "[Character(self) for i in range(n)]"
        """
        return [Character(self) for i in range(n)]


class Skills:

    __skill2attr__ = {} #json_load("data/skills.json")
    __slots__ = ["__sheet__", "__skills__"] \
        + list(__skill2attr__.keys())  # For tab completion

    def __init__(self, sheet):
        self.__sheet__ = sheet
        self.__skills__ = sheet.skills

    def __getattr__(self, key):
        if key in self.__skills__:
            return self.__skills__[key]
        elif key in Skills.__skill2attr__:
            return getattr(self.__sheet__, Skills.__skill2attr__[key])
        else:
            raise AttributeError(key)


class SavingThrows:

    __slots__ = ["__sheet__", "__saving_throws__",
                 # For tab completion:
                 "str", "dex", "con", "int", "wis", "cha"]

    def __init__(self, sheet):
        self.__sheet__ = sheet
        self.__saving_throws__ = sheet.saving_throws

    def __getattr__(self, key):
        if key in self.__saving_throws__:
            return self.__saving_throws__[key]
        elif key in ["str", "dex", "con", "int", "wis", "cha"]:
            return getattr(self.__sheet__, key)
        else:
            raise AttributeError(key)


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
