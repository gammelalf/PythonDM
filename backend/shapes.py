"""
This module provides and interface for shapes and some simple implementations.
A shape is basicly just a collection of points.

For more information look at Shape's docstring.

The implemented shapes are:
    - Line
    - Circle
    - Rect
"""


from math import sqrt

from .coords import Point
from .coords import position_argument_at


class Shape:
    """
    A shape provides two functionalities:
        1. iterate over all Point which are in the represented shape
        2. check whether a Point is contained inside the shape

    This is done by implementing the __iter__ and __contains__ functions.
    There is a default implementation for __contains__ which checks,
    if the point is in the iterator. This is inefficient and should be
    optimised for a specific shape.
    """

    def __iter__(self):
        raise NotImplementedError

    @position_argument_at(1)
    def __contains__(self, point):
        return point in iter(self)


class Line(Shape):
    """
    A Line is a straight connection of two points.
    """

    __slots__ = ["pos1", "pos2"]

    @position_argument_at(1)
    @position_argument_at(2)
    def __init__(self, pos1, pos2):
        self.pos1 = pos1
        self.pos2 = pos2

    def __iter__(self):
        direction = self.pos2 - self.pos1
        distance = round(sqrt(direction.x**2 + direction.y**2))
        old = None
        for i in range(distance+1):
            new = direction*(i/distance)+self.pos1
            if new != old:
                old = new
                yield new

    def __repr__(self):
        return f"Line({repr(self.pos1)}, {repr(self.pos2)})"


class Circle(Shape):
    """
    A Circle is defined with a center point and a radius.
    It consists of any point whose distance from the center is less or equal to the radius.
    To determine the distance the Point's __abs__ function is used, which implements a DnD
    like distance measurement.
    """

    __slots__ = ["pos", "r"]

    @position_argument_at(1)
    def __init__(self, position, radius):
        self.pos = position
        self.r = radius

    def __iter__(self):
        for dx in range(self.r+1):
            for dy in range(self.r+1):
                d = Point(dx, dy)
                if abs(d) <= self.r:
                    yield self.pos + d
                    if dx > 0:
                        yield self.pos + Point(-dx, dy)
                    if dy > 0:
                        yield self.pos + Point(dx, -dy)
                        if dx > 0:
                            yield self.pos + Point(-dx, -dy)
                else:
                    break

    @position_argument_at(1)
    def __contains__(self, point):
        return abs(point - self.pos) <= self.r

    def __repr__(self):
        return f"Circle({repr(self.pos)}, {self.r})"


class Rect(Shape):
    """
    A Rect (short for rectangle) is defined by two points.

    This class is probably not very usefull in this project, but was implemented anyway.
    """

    __slots__ = ["pos1", "pos2"]

    @position_argument_at(1)
    @position_argument_at(2)
    def __init__(self, pos1, pos2):
        x1, x2 = pos1.x, pos2.x
        y1, y2 = pos1.y, pos2.y
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        self.pos1 = Point(x1, y1)
        self.pos2 = Point(x2, y2)

    def __iter__(self):
        for x in range(self.pos1.x, self.pos2.x+1):
            for y in range(self.pos1.y, self.pos2.y+1):
                yield Point(x, y)

    @position_argument_at(1)
    def __contains__(self, point):
        return self.pos1.x <= point.x <= self.pos2.x and self.pos1.y <= point.y <= self.pos2.y

    def __repr__(self):
        return f"Rect({repr(self.pos1)}, {repr(self.pos2)})"


def iter_test(shape, size=16):
    """
    Iterate over a shape and mark the points with Xs in a textfield.
    """
    field = [[' ' for i in range(size)] for i in range(size)]
    for p in shape:
        if field[p.x][p.y] == 'X':
            print(f"Got {p} more than just once")
        field[p.y][p.x] = 'X'
    print("\n".join(map(lambda x: "".join(x), field)))


def contains_iter_test(shape):
    """
    This test function iterates over a shape and checks that all points the iterator returns,
    are also contained in the shape.

    There should also be the other way, where it checks if any point for which contains returns
    True is also iterated over.
    """
    for p in shape:
        if p not in shape:
            print(f"{p} is returned by the iterator, "
                  "but __contains__ returns False")
    print("If you see only this, then everything is fine")
