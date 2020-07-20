from functools import wraps
from collections import defaultdict

from .battle import Battle
from .battle import CharacterAccess
from .player import Player

from backend.bords import DictBord
from backend.character import Character
from backend.character import Initiative


class Game:

    def __init__(self, players_sheetdir):
        self.players = []
        for sheet in players_sheetdir.__dict__:
            self.players.append(Player(getattr(players_sheetdir, sheet)))

        self.battle = Battle()
        self.character_access = CharacterAccess(self.battle)

        self.bord = DictBord()

    # ================== Battle ================== #
    def new_battle(self, add_players=True):
        """
        Initialize a new and fresh battle and dump the old one.
        """
        # Initialize battle
        self.battle = Battle()

        # Pre-add players if desired
        if add_players:
            self.battle.add(self.players)

        # Update character access
        self.character_access.__init__(self.battle)

    @wraps(Battle.add)
    def battle_add(self, *args):
        self.battle.add(*args)

    def __player_abbr_lookup(self, name):
        """
        A helper function for roll_initiative

        It takes an abbreviated player name and returns the player object, if it can find one and only one.
        """
        shortened_dict = {}
        shortened_keys_count = defaultdict(int)
        for player in self.players:
            key = player.name[:len(name)].lower()
            shortened_keys_count[key] += 1
            shortened_dict[key] = player

        if shortened_keys_count[name.lower()] == 0:
            raise KeyError(name)
        elif shortened_keys_count[name.lower()] == 1:
            return shortened_dict[name.lower()]
        else:
            raise KeyError(f"{name.lower()} is not precise enough")

    def roll_initiative(self):
        """
        Reset, reroll and sort by initiative

        It will ask for the player's first roll in advance and any other, when the need arises.
        """
        for char in self.battle.list:
            char.initiative = Initiative(char.roll_initiative)

        for i in range(len(self.players)):
            try:
                print("Enter player's name:")
                player = self.__player_abbr_lookup(input())
            except KeyError:
                print("Invalid player")
                continue
            except KeyboardInterrupt:
                break

            try:
                print(f"Enter {player.name}'s initiative:")
                player.initiative.append(int(input()))
            except ValueError:
                print("Invalid number")
                continue
            except KeyboardInterrupt:
                break

        self.battle.list.sort(key=lambda x: x.initiative, reverse=True)

    # ================== Characters ================== #
    def damage_character(self, char: Character, amount):
        char.hp -= amount
        if char.hp <= 0:
            char.hp = 0
            char.name = "\t" + char.name + " (Defeated)"
