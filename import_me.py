import backend
from backend import *
from backend.character import Player
from backend.battle import Battle
from backend.sheet import SheetDirectory
from backend.util import real_path

from exposer import Exposer


def Battle(*chars):
    return Exposer(backend.battle.Battle(*chars))


# Load sheets
sheets = SheetDirectory(real_path("sheets"))
enemies = sheets.enemies


# Get a fresh new Battle object with the players already added
def reset_battle():
    global battle
    battle = Battle()
    for player in sheets.players.__dict__:
        battle.add(Player(getattr(sheets.players, player)))


reset_battle()
