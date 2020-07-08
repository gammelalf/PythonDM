from .coords import position_argument_at
from .coords import Point
from .shapes import Line


@position_argument_at(0)
@position_argument_at(1)
def get_step(start, end, size, bord=None):
    """
    Create a step from a start position towards an end position of a length.
    """
    step = Point(0, 0)
    while abs(step) < size:
        steps = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                dp = Point(dx, dy)
                if bord is None or bord.get_character(start + step + dp) is None:
                    steps.append((abs(end - start - step - dp), dp))
        steps.sort(key=lambda x: x[0])
        step += steps[0][1]
    return step

