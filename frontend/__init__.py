from backend import dice
from backend.util import real_path
from backend.sheet import SheetDirectory

from frontend.game import Game

__all__ = ["sheets", "enemies", "__game", "new_battle", "battle_add", "dice"]

sheets = SheetDirectory(real_path("data/sheets"))
enemies = sheets.enemies

__game = Game(sheets.players)
__game.new_battle()

new_battle = __game.new_battle
battle_add = __game.battle_add
