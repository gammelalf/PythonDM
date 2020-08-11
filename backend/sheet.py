from .character import Character
from .util import json_load


class Sheet(dict):

    def __init__(self, path):
        self.__path = path
        self.update(json_load(path))

    def __rmul__(self, n):
        """
        Syntactic sugar for "[Character(self) for i in range(n)]"
        """
        return [Character(self) for i in range(n)]
