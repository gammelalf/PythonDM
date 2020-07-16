from functools import wraps

from .battle import Battle
from backend.character import Player


class Game:

    def __init__(self, players_sheetdir):
        self.players = []
        for sheet in players_sheetdir.__dict__:
            self.players.append(Player(getattr(players_sheetdir, sheet)))

        self.battle = Battle()
        self.bord = None

    def new_battle(self, add_players=True):
        self.battle = Battle()
        if add_players:
            self.battle.add(self.players)

    @wraps(Battle.add)
    def battle_add(self, *args):
        self.battle.add(*args)

    def show_battle(self):
        print(str(self.battle))
