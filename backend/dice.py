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


import random
import re


# ================== Dices ================== #
def normal(n):
    """
    Roll a normal ´n´ sided dice.
    """
    return random.randint(1, n)


def __gauss_int(lower, upper, sigma=1, radius=3):
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
    return __gauss_int(1, n)


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
def __add(dice, y, x=0):
    return x + y


def __sub(dice, y, x=0):
    return x - y


def __dice(dice, y, x=1):
    if x == 1:
        return dice(y)
    else:
        return sum([dice(y) for i in range(x)])


__tokens = re.compile(r"d|\+|\-|[1-9]\d*|(?!\s*)")
__operations = {"d": __dice, "-": __sub, "+": __add}


def roll(expr, dice=normal):
    """
    Evaluate a dice expression using the given ´dice´
    """
    # Tokenize
    tokens = __tokens.findall(expr)

    # There should be some
    if len(tokens) == 0:
        raise ValueError(f"The string contains no expression: {repr(expr)}")

    # Convert to integers
    for i, token in enumerate(tokens):
        if token not in __operations.keys():
            tokens[i] = int(token)

    for op in __operations.keys():
        while op in tokens:
            i = tokens.index(op)
            if op == "d" and i+2 < len(tokens) and tokens[i+2] == "d":
                raise SyntaxError("Two dice operations directly one after another are prohibited")
            if i == 0 or tokens[i-1] in __operations.keys():
                y = tokens.pop(i+1)
                tokens[i] = __operations[op](dice, y)
            elif i == len(tokens)-1 or tokens[i+1] in __operations.keys():
                raise SyntaxError(f"The operator {op} is missing an operand: {repr(tokens)}")
            else:
                y = tokens.pop(i+1)
                x = tokens.pop(i-1)
                tokens[i-1] = __operations[op](dice, y, x)

    return tokens[0]


# ================== Compiler ================== #
def operation(op, right, left=None):
    if left is None:
        def func(dice):
            return op(dice, right(dice))
    else:
        def func(dice):
            return op(dice, right(dice), left(dice))
    return func


def const(value):
    def func(dice):
        return value
    return func


def compile(expr):
    """
    Compile a dice expression and return a callable object which takes a dice to evaluate the original expression
    """
    # Tokenize
    tokens = __tokens.findall(expr)

    # There should be some
    if len(tokens) == 0:
        raise ValueError(f"The string contains no expression: {repr(expr)}")

    # Convert to integers
    for i, token in enumerate(tokens):
        if token not in __operations.keys():
            tokens[i] = const(int(token))

    for op in __operations.keys():
        while op in tokens:
            i = tokens.index(op)
            if i == 0 or tokens[i-1] in __operations.keys():
                y = tokens.pop(i+1)
                tokens[i] = operation(__operations[op], y)
            elif i == len(tokens)-1 or tokens[i+1] in __operations.keys():
                raise SyntaxError(f"The operator {op} is missing an operand: {repr(tokens)}")
            else:
                y = tokens.pop(i+1)
                x = tokens.pop(i-1)
                tokens[i-1] = operation(__operations[op], y, x)

    return tokens[0]
