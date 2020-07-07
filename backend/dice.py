"""
This module implements a parser and evaluator for dice-expressions.
It also provides different type of dice for evaluation such expressions.

Dice Types:
    - normal: a dice whose results are all equally likely
    - gauss
    - lowest: always rolls the lowest possible result 1
    - highest: always rolls the highest possible result n
    - expected: always rolls the expected average of a normal dice
"""


import random
import re


# ================== Dices ================== #
def normal(n):
    """
    Roll a normal ´n´ sided dice.
    """
    return random.randint(1, n)


def __gaussint(lower, upper, sigma=1, radius=3):
    """
    Like random.randint but with a normal distribution

    Use random.gauss with ´sigma´ to get a random value on the x-axis.
    The ´radius´ then defines the x-axis' portion
    which will be mapped to the desired range.
    If the value falls outside this portion,
    it will be replaced by a new one.
    """
    value = random.gauss(radius, sigma)
    while value < 0 or value > 2*radius:
        value = random.gauss(sigma, radius)
        # Uncomment for checking likeliness of reroll
        # print("reroll")

    step = 2*radius/(upper - lower + 1)
    return lower + int(value // step)


def gauss(n):
    """
    Roll a ´n´ sided dice who follows a normal distribution.
    """
    return __gaussint(1, n)


def lowest(n):
    """
    Return 1
    """
    return 1


def highest(n):
    """
    Return ´n´
    """
    return n


def expected(n):
    """
    Return expected value of a ´n´ sided dice.
    """
    return (n+1)/2


# ================== Evaluator ================== #
__dice_pattern = re.compile(r"([1-9]\d*)?d([1-9]\d*)")


def roll(expr, dice=normal):
    """
    Evaluate all dice operations in the expression using the given ´dice´
    and hand the rest to python's eval function.
    """
    # find all dice operations
    matches = []
    match = __dice_pattern.search(expr)
    while match is not None:
        matches.append(match)
        match = __dice_pattern.search(expr, match.span()[1])

    # roll them
    rolls = []
    for match in matches:
        # get the values for n, m in the expression ndm
        if match.group(1) is None:
            m = 1
        else:
            m = int(match.group(1))
        n = int(match.group(2))

        # perform the rolls
        rolls.append(sum([dice(n) for i in range(m)]))

    # Recreate the expression but replace dice operations with their results
    rolled_expr = ""
    end = 0
    for i, match in enumerate(matches):
        rolled_expr += expr[end:match.start()]
        rolled_expr += str(rolls[i])
        end = match.end()
    rolled_expr += expr[end:]

    return eval(rolled_expr)
