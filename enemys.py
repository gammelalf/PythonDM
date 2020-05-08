import os
import json

from dice import * # Required for eval in Enemy.__init__
from character import Character

__all__ = ["enemys"]

class Enemy(Character):

    def __init__(self, name):
        with open(os.path.join("enemys", f"{name}.json")) as f:
            data = json.load(f)
        super().__init__(name, **data)

        if isinstance(self.max_hp, str):
            # TODO Huge insecurity, needs better solution
            self.max_hp = eval(self.max_hp)
        self.hp = self.max_hp

class Enemys(object):
    """
    Namespace containing all enemys provided by json files.
    """

    def __init__(self):
        for enemy in [f[:-5] for f in os.listdir("enemys") if f.endswith(".json")]:
            setattr(self, enemy.replace(" ", "_"), Enemys.__curried_constructor(enemy))

    @staticmethod
    def __curried_constructor(enemy):
        def constructor():
            return Enemy(enemy)
        return constructor

enemys = Enemys()
