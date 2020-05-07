import random


__all__ = [ "d4",  "d6",  "d8",  "d12",  "d20",  "d100",
           "gd4", "gd6", "gd8", "gd12", "gd20", "gd100"]


class Dice:
    """
    Dice(n) represents a n-sided dice
    To throw the dice, call it.

    A dice obj implements the following operators:
    (+) Throw the dice and add a value
    (-) Throw the dice and subtract a value
    (*) Throw the dice "value-times" and sum the results

    Example of use:
    > d6 = Dice(6) # Define dice
    > 6 * d6 + 1   # Throw dice 6 times and add 1
    """

    __slots__ = ["n", "func"]

    def __init__(self, n, func=random.randint):
        self.n = n
        self.func = func

    def __repr__(self):
        return f"Dice({self.n})"

    def __call__(self):
        return self.func(1, self.n)

    def __add__(self, value):
        return self() + value

    def __radd__(self, value):
        return self.__add__(value)

    def __sub__(self, value):
        return self() - value

    def __rsub__(self, value):
        return self.__sub__(value)

    def __mul__(self, value):
        return sum([self() for i in range(value)])

    def __rmul__(self, value):
        return self.__mul__(value)


d4   = Dice(4)
d6   = Dice(6)
d8   = Dice(8)
d10  = Dice(10)
d12  = Dice(12)
d20  = Dice(20)
d100 = Dice(100)


def gaussint(lower, upper, sigma=1, radius=3):
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


def curried_gaussint(sigma=1, radius=3):
    def func(lower, upper):
        return gaussint(lower, upper, sigma, radius)
    return func


gd4   = Dice(4,   curried_gaussint())
gd6   = Dice(6,   curried_gaussint())
gd8   = Dice(8,   curried_gaussint())
gd10  = Dice(10,  curried_gaussint())
gd12  = Dice(12,  curried_gaussint())
gd20  = Dice(20,  curried_gaussint())
gd100 = Dice(100, curried_gaussint())


def test(func, prob_size=1000, lower=0, upper=10):
    """
    Shitty function for testing randint's distribution

    Call random.randint-like ´func´ ´prob_size´-times
    and count the result.
    """
    list = [0 for i in range(lower, upper+1)]
    for i in range(prob_size):
        list[func(lower, upper)-lower] += 1
    return list

