import json
import os

from dice import *


class Character(object):

    def __init__(self, name, sheet=None, **kwargs):
        self.name = name

        if sheet is not None:
            with open(sheet) as f:
                sheet = json.load(f)
            sheet.update(kwargs)
        else:
            sheet = kwargs

        for key, value in sheet.items():
            self.__setattr__(key, value)

        if isinstance(self.max_hp, str):
            self.max_hp = eval(self.max_hp)
        self.hp = self.max_hp

    @property
    def _global_name(self):
        return self.name.lower().replace(" ", "_")

    def _roll_initiative(self):
        self.initiative = d20 + self.dex

    def __repr__(self):
        return f"{self.name} ({self.hp} / {self.max_hp})"


class CharacterFactory(object):
    
    def __init__(self, directory):
        for sheet in os.listdir(directory):
            if not sheet.endswith(".json"):
                continue
            name = sheet[:-5]
            sheet = os.path.join(directory, sheet)
            constructor = self.__curried_constructor(name, sheet)
            setattr(self, name.replace(" ", "_"), constructor)

    @staticmethod
    def __curried_constructor(name, sheet):
        def constructor():
            return Character(name, sheet=sheet)
        return constructor
