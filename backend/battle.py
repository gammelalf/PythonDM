from collections import defaultdict

from .character import Character
from .sheet import Sheet


class Battle(object):

    def __init__(self, *chars):
        # For sorting by initiative and iterating
        self.__list__ = []

        # For counting of names
        self.__names__ = defaultdict(int)

        if len(chars) != 0:
            self.add(*chars)

    def __repr__(self):
        return f"Battle({self.__list__})"

    def __str__(self):
        return "\n".join(map(repr, self))

    def __iter__(self):
        return iter(self.__list__)

    def add(self, char, *chars):
        """
        Add a character to the battle

        Accepts Characters, Sheets, lists of those
        """
        if isinstance(char, int):
            n = char
            char = chars[0]
            chars = chars[1:]
            for i in range(n):
                self.add(char)

        elif isinstance(char, list):
            self.add(*char)

        elif isinstance(char, Sheet):
            self.__add_single(Character(char))

        elif isinstance(char, Character):
            self.__add_single(char)

        else:
            raise TypeError(type(char))

        if len(chars) != 0:
            self.add(*chars)

    def __add_single(self, char):
        """
        Add a single character to the battle
        """
        # Increase name counter
        self.__names__[char.name] += 1

        # If creature is second, label the first
        if self.__names__[char.name] == 2:
            first = getattr(self, char.global_name)
            delattr(self, first.global_name)
            first.name += " 1"
            setattr(self, first.global_name, first)

        # If creature isn't the first, label it
        if self.__names__[char.name] > 1:
            char.name += f" {self.__names__[char.name]}"

        # Add the creature
        self.__list__.append(char)
        setattr(self, char.global_name, char)

    def remove(self, char, *chars):
        """
        Remove a character from the battle
        """
        if isinstance(char, Character):
            self.__list__.remove(char)
            delattr(self, char.global_name)
        else:
            raise TypeError()

        if len(chars) != 0:
            self.remove(*chars)

    def order(self, roll=True):
        """
        Order combatants in list by initiative
        """
        self.__list__.sort(key=lambda x: x.initiative, reverse=True)
