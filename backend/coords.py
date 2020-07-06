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

    def __eq__(self, obj):
        if isinstance(obj, Coord):
            return self.x == obj.x and self.y == obj.y
        else:
            return False

    def __hash__(self):
        return hash((self.x, self.y, ))

    def __repr__(self):
        return f"Coord({self.x}, {self.y})"

    def __str__(self):
        return f"({self.x}, {self.y})"


def position_argument_at(index):
    def decorator(func):
        def decorated_func(*args, **kwargs):
            # If the argument is already a Coord, no action is needed
            if isinstance(args[index], Coord):
                return func(*args, **kwargs)

            # Convert to list for easier manipulation
            args = list(args)
            if isinstance(args[index], tuple) and len(args[index]) == 2:
                args[index] = Coord(args[index][0], args[index][1])
            elif isinstance(args[index], int) and isinstance(args[index+1], int):
                args[index] = Coord(args[index], args[index+1])
                del args[index+1]
            else:
                raise TypeError(f"unsupported position argument type: '{type(args[index])}'")
            return func(*args, **kwargs)
        return decorated_func
    return decorator
