import json
import os


class Sheet(object):

    def __init__(self):
        self.name = ""

        self.size = "Medium"
        self.race = "Humanoid"
        self.alignment = ["any", "any"]

        self.hp = 0
        self.ac = 10
        self.armor = []
        self.speed = {
                "walk": 30,
                "swim": 0,
                "fly": 0,
                "burrow": 0
                }

        self.str = 0
        self.dex = 0
        self.con = 0
        self.int = 0
        self.wis = 0
        self.cha = 0

        self.saving_throws = {}
        self.skills = {}
        self.damage_resistances = []
        self.senses = {"passive Perception": 10}
        self.language = ["Common"]
        self.challenge = 1

        self.actions = []

    def dump(self, path):
        with open(path, "w") as f:
            json.dump(self.__dict__, f, indent=4)

    def load(path):
        self = Sheet()
        with open(path) as f:
            self.__dict__.update(json.load(f))
        return self

    def __str__(self):
        return f"""
        """


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
            with open(value) as f:
                value = Sheet()
                value.__dict__.update(json.load(f))
        return value
