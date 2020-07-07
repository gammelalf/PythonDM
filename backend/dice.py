import ast
import operator as op

import random
import re


def dice(n):
    """
    Roll a normal n sided dice.
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


def gauss_dice(n):
    return __gaussint(1, n)


__dice_pattern = re.compile("([1-9]\d*)?d([1-9]\d*)")
def roll(expr, dice=dice):
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
