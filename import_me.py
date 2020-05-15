from dice import *
from battle import Battle
from sheet import SheetDirectory, Sheet
from util import real_path, Context
from character import Player, Character

sheets = SheetDirectory(real_path("sheets"))
enemys = sheets.enemys

players = []
for player in sheets.players.__dict__:
    players.append(Player(getattr(sheets.players, player)))

def reset_battle():
    global battle
    battle = Battle()
    battle._add(players)
reset_battle()

Context._set_globals(globals())
