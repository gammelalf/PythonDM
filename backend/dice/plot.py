from math import exp
from math import sqrt
from math import tau

from matplotlib import pyplot as plt

from .expression import __parse
from .expression import __add
from .expression import __sub
from .expression import compile
from . import dices


class Distribution:

    def __init__(self, prec=1):
        self.xs = []
        self.ys = []
        self.prec = 1
        self.rank = 1

    @staticmethod
    def from_dice(dice, prec, n):
        self = Distribution()
        for i in range(prec, n*prec+1):
            i /= prec
            self.xs.append(i)
            self.ys.append(dice(i, n))
        self.prec = prec
        return self

    @staticmethod
    def get_operation(dice, prec):
        def __dice(y, x=1):
            if x == 1:
                return Distribution.from_dice(dice, prec, y)
            else:
                s = 0
                for i in range(x):
                    s += Distribution.from_dice(dice, prec, y)
                return s
        return __dice

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
        new.rank = self.rank
        return new

    def normalize(self):
        new = self.copy()
        total = sum(new.ys)
        for i in range(len(new.ys)):
            new.ys[i] /= total
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
            new.rank = self.rank + obj.rank
            new.xs = list(range(self.min + obj.min, self.max + obj.max + 1))
            new.ys = [0 for x in new.xs]

            for self_x, self_y in zip(self.xs, self.ys):
                for obj_x, obj_y in zip(obj.xs, obj.ys):
                    new.ys[int((self_x + obj_x)*new.prec) - new.min] += obj.rank*self_y + self.rank*obj_y

            print(new)
            return new.normalize()
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
        return f"Distribution(rank={self.rank}, min={self.min}, max={self.max})"


def normal(i, n):
    return 1/n


def gauss(i, n):
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

    operations = {"d": Distribution.get_operation(dice, prec), "+": __add, "-": __sub}
    dist = __parse(expr, operations, const=int)
    dist = dist.normalize()

    plot = plt.plot(dist.xs, dist.ys)
    return plot


def create_by_rolling(expr, dice, n=10**5):
    expr = compile(expr)
    results = dict((i, 0) for i in range(expr(dices.lowest), expr(dices.highest)+1))

    for i in range(n):
        results[expr(dice)] += 1

    x = list(results.keys())
    y = list(results.values())

    for i in range(len(y)):
        y[i] /= n

    plot = plt.plot(x, y)
    return plot

def test(expr, dice):
    create(expr, dice=dice)
    create_by_rolling(expr, dice=dice, n=10**5)
