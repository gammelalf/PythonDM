from collections import defaultdict

from backend.character import Character
from backend.character import Initiative
from backend.sheet import Sheet

from .player import Player


class Battle(object):
    """
    A Battle contains a bunch of characters who are fighting each other.
    It can also sort them by their initiative.
    """

    def __init__(self, *chars):
        # For sorting by initiative and iterating
        self.list = []

        # For easy access
        self.dict = {}

        # For counting of names
        self.names = defaultdict(int)

        if len(chars) != 0:
            self.add(*chars)

    def __str__(self):
        return "\n".join(map(str, self))

    def __iter__(self):
        return iter(self.list)

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
        self.names[char.name] += 1

        # If creature is second, label the first
        if self.names[char.name] == 2:
            first = self.dict[char.global_name]
            del self.dict[first.global_name]
            first.name += " 1"
            self.dict[first.global_name] = first

        # If creature isn't the first, label it
        if self.names[char.name] > 1:
            char.name += f" {self.names[char.name]}"

        # Add the creature
        self.list.append(char)
        self.dict[char.global_name] = char

    def remove(self, char, *chars):
        """
        Remove a character from the battle
        """
        if isinstance(char, Character):
            self.list.remove(char)
            del self.dict[char.global_name]
        else:
            raise TypeError()

        if len(chars) != 0:
            self.remove(*chars)

    def __get_player_from_abbr(self, abbr):
        """
        Get a player from an abbreviation of his name
        """
        # Initialize lookup for abbreviated names
        for length in range(100):
            lookup = {}
            for name, player in self.__players__.items():
                if len(name) <= length:
                    key = name.lower()
                else:
                    key = name[:length].lower()
                if key in lookup:
                    break
                lookup[key] = player
            else:
                break
        return lookup[abbr[:length].lower()]


class CharacterAccess:

    def __init__(self, battle):
        self.__dict__ = battle.dict
        self.__repr__ = battle.__str__

    def __repr__(self):
        return self.__repr__()

