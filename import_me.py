from backend import *
from backend.character import Player

from battle import Battle
from sheet import SheetDirectory
from util import real_path


# Load sheets
sheets = SheetDirectory(real_path("sheets"))
enemies = sheets.enemies


# Get a fresh new Battle object with the players already added
def reset_battle():
    global battle
    battle = Battle()
    for player in sheets.players.__dict__:
        battle._add(Player(getattr(sheets.players, player)))


reset_battle()
