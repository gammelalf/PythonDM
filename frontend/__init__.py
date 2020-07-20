from backend import dice
from backend.util import real_path
from backend.sheet import SheetDirectory

from frontend.game import Game

__all__ = ["sheets", "enemies", "__game",
           "new_battle", "battle_add", "roll_initiative",
           "characters", "damage_character",
           "dice"]

sheets = SheetDirectory(real_path("data/sheets"))
enemies = sheets.enemies

__game = Game(sheets.players)
__game.new_battle()

new_battle = __game.new_battle
battle_add = __game.battle_add
roll_initiative = __game.roll_initiative

characters = __game.character_access
damage_character = __game.damage_character
