import backend
from backend.util import real_path

from frontend.game import Game

__all__ = ["sheets", "enemies", "__game", "new_battle", "battle_add"]

sheets = backend.sheet.SheetDirectory(real_path("sheets"))
enemies = sheets.enemies

__game = Game(sheets.players)
__game.new_battle()

new_battle = __game.new_battle
battle_add = __game.battle_add
