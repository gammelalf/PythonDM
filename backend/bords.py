from .coords import position_argument_at
from .character import Character


class DictBord(dict):

    @position_argument_at(1)
    def __getitem__(self, pos):
        return super().__getitem__(pos)

    @position_argument_at(1)
    def __setitem__(self, pos, char):
        if isinstance(char, Character):
            super().__setitem__(pos, char)
            char.position = pos
        else:
            raise TypeError("invalid type '{type(char)}', must be {Character}")

    @position_argument_at(1)
    def __delitem__(self, pos):
        if pos in self:
            self[pos].position = None
            super().__delitem__(pos)
        else:
            raise KeyError("position is already unoccupied")

    @position_argument_at(1)
    def get_character(self, pos):
        if pos in self:
            return self[pos]
        else:
            return None

    @position_argument_at(2)
    def move(self, char, new_pos):
        if new_pos in self:
            raise ValueError("Position is already occupied")
        else:
            if char.position in self:
                del self[char.position]
            self[new_pos] = char
