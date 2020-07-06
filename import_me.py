from backend.dice import *
from battle import Battle
from sheet import SheetDirectory, Sheet
from util import real_path, Context
from backend.character import Player, Character

# Load sheets
sheets = SheetDirectory(real_path("sheets"))
enemys = sheets.enemys

# Put all sheets from sheets/players/ as Characters into a list
players = []
for player in sheets.players.__dict__:
    players.append(Player(getattr(sheets.players, player)))

# Clear namespace
del player

# Get a fresh new Battle object with the players already added
def reset_battle():
    global battle
    battle = Battle()
    battle._add(players)
reset_battle()

# Enable Contexts
Context._set_globals(globals())
