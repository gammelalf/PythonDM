from collections import defaultdict

from util import Context
from character import Character
from sheet import Sheet

class Battle(Context):

    def __init__(self, *args):
        self.__list__ = []
        self.__names__ = defaultdict(int)

        args = list(args)
        while len(args) != 0:
            num = args[0]
            cls = args[1]
            for i in range(num):
                self._add(cls(i+1))
            args = args[2:]

    def __repr__(self):
        return "\n".join(map(repr, self))

    def __iter__(self):
        return iter(self.__list__)

    def _add(self, char, *chars):
        """
        Add a character to the battle
        """
        if isinstance(char, Sheet):
            self._add(Character(char))

        elif isinstance(char, Character):
            # Increase name counter
            self.__names__[char.name] += 1

            # If creature is second, label the first
            if self.__names__[char.name] == 2:
                first = getattr(self, char._global_name)
                delattr(self, first._global_name)
                first.name += " 1"
                setattr(self, first._global_name, first)

            # If creature isn't the first, label it
            if self.__names__[char.name] > 1:
                char.name += f" {self.__names__[char.name]}"

            # Add the creature
            self.__list__.append(char)
            setattr(self, char._global_name, char)

        else:
            raise TypeError()

        if len(chars) != 0:
            self._add(*chars)

    def _remove(self, char, *chars):
        """
        Remove a character from the battle
        """
        if isinstance(char, Character):
            self.__list__.remove(char)
            delattr(self, char._global_name)
        else:
            raise TypeError()

        if len(chars) != 0:
            self._add(*chars)

    def _order(self, roll=True):
        """
        Order combatants in list by initiative
        """
        if roll:
            for char in self:
                char._roll_initiative()

        self.__list__.sort(key=lambda x: x.initiative, reverse=True)
