from DataTypes.value import Value
from DataTypes.number import Number


class String(Value):
    def __init__(self, value) -> None:
        super().__init__()
        self.value = value

    def add_to(self, other):
        if isinstance(other, String):
            string = String(self.value + other.value)
            string.set_context(self.context)
            return string, None
        else:
            return None, Value.illegal_operation(self, other)

    def mult_to(self, other):
        if isinstance(other, Number):
            string = String(self.value * other.value)
            string.set_context(self.context)
            return string, None
        else:
            return None, Value.illegal_operation(self, other)

    def copy(self):
        copy = String(self.value)
        copy.set_pos(self.start_pos, self.end_pos)
        copy.set_context(self.context)
        return copy

    def is_true(self):
        return len(self.value) > 0

    def __repr__(self) -> str:
        return f'"{self.value}"'
