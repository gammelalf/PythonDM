from functools import partial
from functools import wraps
from collections import defaultdict
from math import exp
from math import sqrt
from math import tau

from matplotlib import pyplot as plt

from .expression import __parse
from .expression import compile
from . import dices


def __prec_range(lower, upper, prec=1):
    for i in range(lower*prec, upper*prec+1):
        yield i / prec


def __create_dist(func):
    @wraps(func)
    def new_func(prec, n):
        return tuple((i, func(i, n)) for i in __prec_range(1, n, prec))
    return new_func


@__create_dist
def normal(i, n):
    return 1/n


@__create_dist
def gauss(i, n):
    x = i - (n+1)/2
    mu = 0
    sigma = 1/6*(n-1)
    return exp(-0.5 * ((x - mu) / sigma)**2)/(sigma*sqrt(tau))


def __add(y, x=0):
    if isinstance(x, int) and isinstance(y, int):
        return x + y
    elif isinstance(x, int):
        return tuple((key + x, value) for key, value in y)
    elif isinstance(y, int):
        return __add(x, y)
    else:
        s = defaultdict(float)
        for x_k, x_v in x:
            for y_k, y_v in y:
                s[x_k + y_k] += x_v + y_v

        return tuple(s.items())


def __sub(y, x=0):
    if isinstance(x, int) and isinstance(y, int):
        return x - y
    elif isinstance(x, int):
        return __add(y, -x)
    elif isinstance(y, int):
        return __add(-y, x)
    else:
        s = defaultdict(float)
        for x_k, x_v in x:
            for y_k, y_v in y:
                s[x_k - y_k] += x_v + y_v

        return tuple(s.items())


def __dice(dice, y, x=1):
    if x == 1:
        return dice(y)
    else:
        s = 0
        for i in range(x):
            s = __add(dice(y), s)
        return s


__dices_to_plot = {
    dices.normal: normal,
    dices.gauss: gauss
}


def create(expr, prec=1, dice=normal):
    if dice in __dices_to_plot:
        dice = __dices_to_plot[dice]

    operations = {"d": partial(__dice, partial(dice, prec)), "+": __add, "-": __sub}
    dist = list(__parse(expr, operations, const=int))
    dist.sort(key=lambda t: t[0])

    x = [x for x, y in dist]
    y = [y for x, y in dist]

    # Normalize
    print(sum(y))
    total = sum(y)#/prec
    for i in range(len(y)):
        y[i] /= total
    print(sum(y))

    plot = plt.plot(x, y)
    return plot


def create_by_rolling(expr, dice, n=10**3):
    expr = compile(expr)
    results = defaultdict(int)
    for i in range(n):
        results[expr(dice)] += 1

    results = list(results.items())
    results.sort(key=lambda x: x[0])

    x = [x for x, y in results]
    y = [y for x, y in results]

    for i in range(len(y)):
        y[i] /= n

    plot = plt.plot(x, y)
    return plot

def test(expr, dice):
    create(expr, dice=dice)
    create_by_rolling(expr, dice=dice, n=10**5)
