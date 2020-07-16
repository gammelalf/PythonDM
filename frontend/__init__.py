import backend
from backend.character import Player
from backend.util import real_path
from backend.character import Character

from frontend.battle import Battle


# Load sheets
sheets = backend.sheet.SheetDirectory(real_path("sheets"))
enemies = sheets.enemies


# Get a fresh new Battle object with the players already added
def reset_battle():
    global battle
    battle = Battle()
    for player in sheets.players.__dict__:
        battle.add(Player(getattr(sheets.players, player)))


reset_battle()
