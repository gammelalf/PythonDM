import json
import os

from dice import roll, gauss_dice, dice


class Character(object):

    def __init__(self, sheet):
        self.sheet = sheet
        self.name = sheet.name

        self.max_hp = sheet.hp
        if isinstance(self.max_hp, str):
            self.max_hp = roll(self.max_hp, gauss_dice)
        self.hp = self.max_hp

        self.initiative = Initiative(self._roll_initiative)

    @property
    def _global_name(self):
        return self.name.lower().replace(" ", "_")

    def __repr__(self):
        return f"{self.name} ({self.hp} / {self.max_hp})"

    def _roll_initiative(self):
        """
        Roll for initiative and simply return the rolled value
        (possibly with modifiers)
        """
        return dice(20) + self.sheet.dex


class Initiative(list):

    def __init__(self, roll_func):
        self._roll = roll_func

    def __getitem__(self, n):
        if n < 0:
            raise ValueError("Initiative doesn't support negative indecies")

        while len(self) <= n:
            self.append(self._roll())

        return super().__getitem__(n)
    
    def __lt__(self, obj, n=0):
        if self[n] == obj[n]:
            return self.__lt__(obj, n+1)
        else:
            return self[n] < obj[n]

    def __gt__(self, obj, n=0):
        if self[n] == obj[n]:
            return self.__gt__(obj, n+1)
        else:
            return self[n] > obj[n]

    def __eq__(self, obj):
        return False


class Player(Character):

    def _roll_initiative(self):
        print(f"{self.name}'s initiative:")
        return int(input())
