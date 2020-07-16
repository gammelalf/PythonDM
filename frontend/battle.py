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
        self.__players__ = {}

        # For sorting by initiative and iterating
        self.__list__ = []

        # For counting of names
        self.__names__ = defaultdict(int)

        if len(chars) != 0:
            self.add(*chars)

    def __repr__(self):
        return f"Battle({self.__list__})"

    def __str__(self):
        return "\n".join(map(str, self))

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
        if isinstance(char, Player):
            self.__players__[char.global_name] = char
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

    def roll_initiative(self, roll=True):
        """
        Roll initiatives and order combatants in list by initiative
        """
        # Clean old initiatives
        for char in self.__list__:
            char.initiative = Initiative(char.roll_initiative)

        # Add players' first rolls
        for i in range(len(self.__players__)):
            name, value = input().split(" ")
            value = int(value)
            self.__get_player_from_abbr(name).initiative.append(value)

        self.__list__.sort(key=lambda x: x.initiative, reverse=True)
