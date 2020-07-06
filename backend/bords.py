from .coords import Coord, position_argument_at
from .character import Character

class DictBord:

    def __init__(self):
        # Map from Position (Coordinate) to Character
        self.__p2c__ = {}

        # Map from Character to Position (Coordinate)
        self.__c2p__ = {}

    @position_argument_at(1)
    def get_character(self, position, *args):
        if position in self.__p2c__:
            return self.__p2c__[position]
        else:
            return None

    def get_position(self, character):
        if character in self.__c2p__:
            return self.__c2p__[character]
        else:
            return None

    @position_argument_at(2)
    def move(self, character, new_position, *args):
        if new_position in self.__p2c__:
            raise ValueError("Position is already occupied")
        else:
            try:
                self.__unset(character)
            except ValueError:
                # The character didn't have any position yet
                pass
            self.__set(character, new_position)

    def __set(self, character, position, *args):
        if isinstance(character, Character) and isinstance(position, Coord):
            self.__p2c__[position] = character
            self.__c2p__[character] = position
        else:
            raise TypeError(f"unsupported argument types: '{type(character)}' and '{type(position)}'")

    def __unset(self, obj):
        if isinstance(obj, Coord):
            if obj in self.__p2c__:
                del self.__c2p__[self.__p2c__[obj]]
                del self.__p2c__[obj]
            else:
                raise ValueError("position is already unoccupied")
        elif isinstance(obj, Character):
            if obj in self.__c2p__:
                del self.__p2c__[self.__c2p__[obj]]
                del self.__c2p__[obj]
            else:
                raise ValueError("character already has no position")
        else:
            raise TypeError(f"unsupported argument type: '{type(obj)}'")
