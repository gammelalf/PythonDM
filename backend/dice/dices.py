import random


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


