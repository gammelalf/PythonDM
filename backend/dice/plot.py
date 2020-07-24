from math import exp
from math import sqrt
from math import tau
from functools import partial

from matplotlib import pyplot as plt

from .expression import __parse as parse
from .expression import __add as add
from .expression import __sub as sub
from .expression import compile
from . import dices


class Distribution:

    def __init__(self, prec=1):
        self.xs = []
        self.ys = []
        self.prec = 1

    @staticmethod
    def from_dice(dice, prec, n):
        """
        Create a distribution using a dice function.

        This function takes a number in the dices range and the amount of sides
        and returns the probability of rolling that number.
        """
        self = Distribution()
        for i in range(prec, n*prec+1):
            i /= prec
            self.xs.append(i)
            self.ys.append(dice(i, n))
        self.prec = prec
        return self

    @staticmethod
    def dice_operation(dice, prec, y, x=1):
        """
        The operation passed to expressions' __parse in the operations dict for the key `d`.

        The first two arguments hve to be given via ´partial´ first.
        """
        if x == 1:
            return Distribution.from_dice(dice, prec, y)
        else:
            s = 0
            for i in range(x):
                s += Distribution.from_dice(dice, prec, y)
            return s

    @staticmethod
    def from_expression(expr, dice, prec=1):
        """
        Parse a expression and return a Distribution object representing the expression for a given dice.

        How the dice should work, can be found at from_dice.
        """
        operations = {"d": partial(Distribution.dice_operation, dice, prec), "+": add, "-": sub}
        return parse(expr, operations, int)

    @property
    def max(self):
        return int(max(self.xs))

    @property
    def min(self):
        return int(min(self.xs))

    def copy(self):
        new = Distribution()
        new.xs = list(self.xs)
        new.ys = list(self.ys)
        new.prec = self.prec
        return new

    def __add__(self, obj):
        if isinstance(obj, int):
            new = self.copy()
            for i in range(len(new.xs)):
                new.xs[i] += obj
            return new
        elif isinstance(obj, Distribution):
            new = Distribution()
            new.prec = self.prec
            new.xs = list(range(self.min + obj.min, self.max + obj.max + 1))
            new.ys = [0 for x in new.xs]

            for self_x, self_y in zip(self.xs, self.ys):
                for obj_x, obj_y in zip(obj.xs, obj.ys):
                    new.ys[int((self_x + obj_x)*new.prec) - new.min] += self_y * obj_y
            return new
        else:
            raise TypeError()

    def __radd__(self, obj):
        return self.__add__(obj)

    def __sub__(self, obj):
        return self.__add__(- obj)

    def __rsub__(self, obj):
        return (- self).__add__(obj)

    def __neg__(self):
        new_dist = self.copy()
        new_dist.xs = [-x for x in self.xs]
        return new_dist

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return f"Distribution(min={self.min}, max={self.max})"


def normal(i, n):
    return 1/n


def gauss(i, n):
    # TODO redo
    x = i - (n+1)/2
    mu = 0
    sigma = 1/6*(n-1)
    return exp(-0.5 * ((x - mu) / sigma)**2)/(sigma*sqrt(tau))


__dices_to_plot = {
    dices.normal: normal,
    dices.gauss: gauss
}


def create(expr, prec=1, dice=normal):
    if dice in __dices_to_plot:
        dice = __dices_to_plot[dice]

    dist = Distribution.from_expression(expr, dice, prec)
    plot = plt.plot(dist.xs, dist.ys)
    plt.ylim((0, None))
    return plot


def create_by_rolling(expr, dice, n=10**5):
    expr = compile(expr)
    low = expr(dices.lowest)

    x = list(range(low, expr(dices.highest)+1))
    y = [0 for i in x]

    for i in range(n):
        y[expr(dice) - low] += 1

    for i in range(len(y)):
        y[i] /= n

    plot = plt.plot(x, y)
    plt.ylim((0, None))
    return plot

def test(expr, dice):
    create(expr, dice=dice)
    create_by_rolling(expr, dice=dice, n=10**5)
    plt.show()
