import random


def normal(n):
    """
    Roll a normal ´n´ sided dice.
    """
    return random.randint(1, n)


def __gauss_int(lower, upper, sigma=1/6):
    """
    Like random.randint but with a normal distribution

    Use random.gauss with the mean at 0 to get a random value.
    Reroll until the value is between -r and r where r (also radius) is the middle of the lower and upper bound.
    Add the radius, the lower bound and round to get an integer in [lower, upper].

    The used standard variant (usually called sigma) is the product of the distance between the bounds
    and the argument `sigma`. So doubling the range also doubles the distribution's spread.
    """
    radius = (upper-lower)/2

    value = random.gauss(0, sigma*(upper-lower))
    while not -radius < value < radius:
        value = random.gauss(0, sigma*(upper-lower))

    return round(value+radius+lower)


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


