class Coord:
    """
    An implementation of 2 dimensional coordiantes.

    The values for x and y are integers and count the games' base unit.
    For DnD this would be 5 feet.

    Coordinates support the abs() function. It will give the distance
    the coordinate is from the origin. Like in DnD every second diagonal
    step adds 2 and every other one just 1 to the distance.
    """

    __slots__ = ["x", "y"]

    def __init__(self, x, y):
        if isinstance(x, int) and isinstance(y, int):
            self.x = x
            self.y = y
        else:
            raise TypeError("Arguments 'x' and 'y' must be of type 'int'")

    def __add__(self, obj):
        if isinstance(obj, Coord):
            return Coord(self.x + obj.x, self.y + obj.y)
        else:
            raise TypeError(f"unsupported operand type(s) for +: 'type(self)' and '{type(obj)}'")

    def __sub__(self, obj):
        if isinstance(obj, Coord):
            return Coord(self.x - obj.x, self.y - obj.y)
        else:
            raise TypeError(f"unsupported operand type(s) for +: 'type(self)' and '{type(obj)}'")

    def __abs__(self):
        x = abs(self.x)
        y = abs(self.y)
        if x < y:
            return y + x // 2
        else:
            return x + y // 2

    def __repr__(self):
        return f"Coord({self.x}, {self.y})"

    def __str__(self):
        return f"({x}, {y})"
