from Errors.errors import *
from DataTypes.value import Value


class Number(Value):
    def __init__(self, value) -> None:
        super().__init__()
        self.value = value

    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.start_pos, self.end_pos)
        copy.set_context(self.context)
        return copy
    # Math Function

    def add_to(self, other_num):
        if isinstance(other_num, Number):
            return Number(self.value + other_num.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other_num)

    def sub_by(self, other_num):
        if isinstance(other_num, Number):
            return Number(self.value - other_num.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other_num)

    def mult_to(self, other_num):
        if isinstance(other_num, Number):
            return Number(self.value * other_num.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other_num)

    def div_by(self, other_num):
        if isinstance(other_num, Number):
            if other_num.value == 0:
                return None, RunTimeError(
                    other_num.start_pos, other_num.end_pos,
                    "Division By 0",
                    self.context
                )
            return Number(self.value / other_num.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other_num)

    def power_by(self, other_num):
        if isinstance(other_num, Number):
            return Number(self.value ** other_num.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other_num)
    # comparison functions

    def get_comparison_eq(self, other_num):
        if isinstance(other_num, Number):
            result = Number(int(self.value == other_num.value))
            result.set_context(self.context)
            return result, None
        else:
            return None, Value.illegal_operation(self, other_num)

    def get_comparison_ne(self, other_num):
        if isinstance(other_num, Number):
            result = Number(int(self.value != other_num.value))
            result.set_context(self.context)
            return result, None
        else:
            return None, Value.illegal_operation(self, other_num)

    def get_comparison_lt(self, other_num):
        if isinstance(other_num, Number):
            result = Number(int(self.value < other_num.value))
            result.set_context(self.context)
            return result, None
        else:
            return None, Value.illegal_operation(self, other_num)

    def get_comparison_gt(self, other_num):
        if isinstance(other_num, Number):
            result = Number(int(self.value > other_num.value))
            result.set_context(self.context)
            return result, None
        else:
            return None, Value.illegal_operation(self, other_num)

    def get_comparison_le(self, other_num):
        if isinstance(other_num, Number):
            result = Number(int(self.value <= other_num.value))
            result.set_context(self.context)
            return result, None
        else:
            return None, Value.illegal_operation(self, other_num)

    def get_comparison_ge(self, other_num):
        if isinstance(other_num, Number):
            result = Number(int(self.value >= other_num.value))
            result.set_context(self.context)
            return result, None
        else:
            return None, Value.illegal_operation(self, other_num)

    def and_this(self, other_num):
        if isinstance(other_num, Number):
            result = Number(int(self.value and other_num.value))
            result.set_context(self.context)
            return result, None
        else:
            return None, Value.illegal_operation(self, other_num)

    def or_this(self, other_num):
        if isinstance(other_num, Number):
            result = Number(int(self.value or other_num.value))
            result.set_context(self.context)
            return result, None
        else:
            return None, Value.illegal_operation(self, other_num)

    def not_(self):
        result = Number(1 if self.value == 0 else 0)
        result.set_context(self.context)
        return result, None

    def is_true(self):
        return self.value != 0

    def is_false(self):
        return self.value == 0

    def __repr__(self) -> str:
        return str(self.value)
