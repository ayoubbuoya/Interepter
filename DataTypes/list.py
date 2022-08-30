from DataTypes.value import Value
from DataTypes.number import Number
from Errors.errors import RunTimeError


class List(Value):
    def __init__(self, elements) -> None:
        super().__init__()
        self.elements = elements

    def add_to(self, other):
        ret_list = self.copy()
        if isinstance(other, List):
            ret_list.elements.extend(other.elements)
        elif isinstance(other, Number):
            ret_list.elements.append(other.value)
        else:
            return None, Value.illegal_operation(self, other)

        return ret_list, None

    def sub_by(self, other):
        ret_list = self.copy()
        if isinstance(other, Number):
            try:
                ret_list.elements.pop(other.value)
                return ret_list, None
            except:
                return None, RunTimeError(
                    other.start_pos, other.end_pos,
                    "Element at this index could not be removed from list because index is out of bounds",
                    self.context
                )
        else:
            return None, Value.illegal_operation(self, other)

    def div_by(self, other):
        if isinstance(other, Number):
            try:
                return self.elements[other.value], None
            except:
                return None, RunTimeError(
                    other.start_pos, other.end_pos,
                    "Element at this index could not be retrieved from list because index is out of bounds",
                    self.context
                )
        else:
            return None, Value.illegal_operation(self, other)

    def copy(self):
        copy = List(self.elements)
        copy.set_pos(self.start_pos, self.end_pos)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return f'[{", ".join([str(x) for x in self.elements])}]'
