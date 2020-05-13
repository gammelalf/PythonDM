import ast
import operator as op

import random


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


def roll(expr, dice=dice):
    """
    Evaluate an expression containing dice rolls.
    To roll a dice, use the optional function
    which takes the number of sides as an argument.

    zB "2d6+2"
    """
    def m_dice(m, n):
        return sum(dice(n) for i in range(m))

    expr = expr.replace("+", "@")
    expr = expr.replace("d", "+")

    op_dict = {ast.Add: m_dice,      # <m> d <n>
               ast.UAdd: dice,       # d <n>
               ast.MatMult: op.add,  # <a> + <b>
               ast.Sub: op.sub,      # <a> - <b>
               ast.USub: op.neg}     # - <a>

    return __eval(ast.parse(expr, mode="eval").body, op_dict)


def __eval(node, op_dict):
    if isinstance(node, ast.Num):
        return node.n
    elif isinstance(node, ast.BinOp):
        args = (node.left, node.right)
    elif isinstance(node, ast.UnaryOp):
        args = (node.operand, )
    else:
        raise TypeError(f"Not a operator: {node}")

    args = tuple(map(lambda x: __eval(x, op_dict), args))
    try:
        return op_dict[type(node.op)](*args)
    except KeyError:
        raise TypeError(f"Unsupported operator: {type(node.op)}")
