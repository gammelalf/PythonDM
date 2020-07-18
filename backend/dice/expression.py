"""
This file implements a parser for dice expressions
"""

import re
from functools import partial

from .dices import normal


__tokens = re.compile(r"d|\+|\-|[1-9]\d*|(?!\s*)")


def __parse(expr, operations, const):
    def consume_const(tokens, i):
        tokens[i] = const(tokens[i])

    def consume_operation(tokens, i):
        op = tokens[i]
        if i + 1 == len(tokens) or tokens[i + 1] in operations:
            raise SyntaxError(f"Operator {op} is missing its operand.")
        elif isinstance(tokens[i+1], str):
            consume_const(tokens, i + 1)

        if i == 0 or tokens[i - 1] in operations:
            # Unary operation
            tokens[i] = operations[op](tokens.pop(i + 1))
            return i + 1
        else:
            # Binary operation
            tokens[i - 1] = operations[op](tokens.pop(i + 1), tokens.pop(i - 1))
            return i

    # Tokenize
    tokens = __tokens.findall(expr)

    # There should be some
    if len(tokens) == 0:
        raise ValueError(f"The string contains no expression: {repr(expr)}")

    if tokens[0] in operations:
        consume_operation(tokens, 0)
    else:
        consume_const(tokens, 0)

    while len(tokens) > 1:
        op = tokens[1]
        if op != "d":
            if 2 < len(tokens) and tokens[2] == "d":
                consume_operation(tokens, 2)
            elif 3 < len(tokens) and tokens[3] == "d":
                consume_const(tokens, 2)
                consume_operation(tokens, 3)
        elif 3 < len(tokens) and tokens[3] == "d":
            raise SyntaxError("Two dice operation directly one after another are prohibited")
        consume_operation(tokens, 1)
        continue

    return tokens[0]


def __add(dice, y, x=0):
    return x + y


def __sub(dice, y, x=0):
    return x - y


def __dice(dice, y, x=1):
    if x == 1:
        return dice(y)
    else:
        return sum([dice(y) for i in range(x)])


def roll(expr, dice=normal):
    operations = {"d": partial(__dice, dice), "+": partial(__add, dice), "-": partial(__sub, dice)}
    return __parse(expr, operations, int)


def __compile_const(value):
    def func(dice):
        return int(value)

    return func


def __compile_operation(op, left, right=None):
    def func(dice):
        if right is None:
            return op(dice, left(dice))
        else:
            return op(dice, left(dice), right(dice))
    return func


__compile_operations = {"d": partial(__compile_operation, __dice),
                        "+": partial(__compile_operation, __add),
                        "-": partial(__compile_operation, __sub)}


def compile(expr):
    return __parse(expr, __compile_operations, __compile_const)
