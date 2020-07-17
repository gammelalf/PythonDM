"""
This module implements a parser and evaluator for dice-expressions.
It also provides different type of dice for evaluation such expressions.

Dice Types:
    - normal: a dice whose results are all equally likely
    - gauss: a dice whose results follow a normal distribution
    - lowest: always rolls the lowest possible result 1
    - highest: always rolls the highest possible result n
    - expected: always rolls the expected average of a normal dice
"""

from .dices import normal
from .dices import gauss
from .dices import lowest
from .dices import highest
from .dices import expected
from .expression import roll
from .expression import compile

__all__ = ["normal", "gauss", "lowest", "highest", "expected", "roll", "compile"]
