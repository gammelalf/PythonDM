import os

from character import Character

__all__ = ["enemys"]

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
            return Character(enemy, sheet=os.path.join("enemys", f"{enemy}.json"))
        return constructor

enemys = Enemys()
