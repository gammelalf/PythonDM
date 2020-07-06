from .coords import Point
from .coords import position_argument_at as paa


class Shape:

    @paa(1)
    def __contains__(self, point):
        raise NotImplemented

    def __iter__(self):
        raise NotImplemented


class Circle(Shape):

    __slots__ = ["pos", "r"]

    @paa(1)
    def __init__(self, position, radius):
        self.pos = position
        self.r = radius

    @paa(1)
    def __contains__(self, point):
        return abs(point - self.pos) <= self.r

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

    def __repr__(self):
        return f"Circle({repr(self.pos)}, {self.r})"


class Rect(Shape):

    __slots__ = ["pos1", "pos2"]

    @paa(1)
    @paa(2)
    def __init__(self, pos1, pos2):
        x1, x2 = pos1.x, pos2.x
        y1, y2 = pos1.y, pos2.y
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        self.pos1 = Point(x1, y1)
        self.pos2 = Point(x2, y2)

    @paa(1)
    def __contains__(self, point):
        return self.pos1.x <= point.x and point.x <= self.pos2.x \
           and self.pos1.y <= point.y and point.y <= self.pos2.y

    def __iter__(self):
        for x in range(self.pos1.x, self.pos2.x+1):
            for y in range(self.pos1.y, self.pos2.y+1):
                yield Point(x, y)

    def __repr__(self):
        return f"Rect({repr(self.pos1)}, {repr(self.pos2)})"


def iter_test(shape, size=16):
    field = [[' ' for i in range(size)] for i in range(size)]
    for p in shape:
        if field[p.x][p.y] == 'X':
            print(f"Got {p} more than just once")
        field[p.x][p.y] = 'X'
    print("\n".join(map(lambda x: "".join(x), field)))

def contains_iter_test(shape):
    for p in shape:
        if p not in shape:
            print(f"{p} is returned by the iterator, but __contains__ returns False")
    print("If you see only this, then everything is fine")
