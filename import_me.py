from dice import *
from battle import Battle
from sheet import SheetDirectory
from util import real_path, Context

sheets = SheetDirectory(real_path("sheets"))
enemys = sheets.enemys

Context._set_globals(globals())
