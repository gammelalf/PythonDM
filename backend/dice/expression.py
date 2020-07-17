"""
This file implements a parser for dice expressions
"""

import re

from .dices import normal


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


def __eval_operation(op, dice, right, left=None):
    if left is None:
        return op(dice, right)
    else:
        return op(dice, right, left)


def __eval_const(value):
    return value


def __compile_operation(op, dice, right, left=None):
    if left is None:
        def func(dice):
            return op(dice, right(dice))
    else:
        def func(dice):
            return op(dice, right(dice), left(dice))
    return func


def __compile_const(value):
    def func(dice):
        return value
    return func


def __parse(expr, dice=normal):
    # Switch between compile and eval
    if dice is None:
        operation = __compile_operation
        const = __compile_const
    else:
        operation = __eval_operation
        const = __eval_const

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
            if op == "d" and i+2 < len(tokens) and tokens[i+2] == "d":
                raise SyntaxError("Two dice operations directly one after another are prohibited")
            if i == 0 or tokens[i-1] in __operations.keys():
                y = tokens.pop(i+1)
                tokens[i] = operation(__operations[op], dice, y)
            elif i == len(tokens)-1 or tokens[i+1] in __operations.keys():
                raise SyntaxError(f"The operator {op} is missing an operand: {repr(tokens)}")
            else:
                y = tokens.pop(i+1)
                x = tokens.pop(i-1)
                tokens[i-1] = operation(__operations[op], dice, y, x)

    return tokens[0]


def roll(expr, dice=normal):
    return __parse(expr, dice)


def compile(expr):
    return __parse(expr, None)
