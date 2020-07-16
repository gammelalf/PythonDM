from functools import wraps

from .battle import Battle
from .player import Player
from backend.bords import DictBord


class Game:

    def __init__(self, players_sheetdir):
        self.players = []
        for sheet in players_sheetdir.__dict__:
            self.players.append(Player(getattr(players_sheetdir, sheet)))

        self.battle = Battle()
        self.bord = DictBord()

    # ================== Battle ================== #
    def new_battle(self, add_players=True):
        """
        Initialize a new and fresh battle and dump the old one.
        """
        self.battle = Battle()
        if add_players:
            self.battle.add(self.players)

    @wraps(Battle.add)
    def battle_add(self, *args):
        self.battle.add(*args)

    def show_battle(self):
        """
        Print the battle
        """
        print(str(self.battle))
