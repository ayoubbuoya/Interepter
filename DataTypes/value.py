from Errors.errors import RunTimeError


class Value:
    def __init__(self) -> None:
        self.set_pos()
        self.set_context()

    def set_pos(self, start_pos=None, end_pos=None):
        self.start_pos = start_pos
        self.end_pos = end_pos
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def illegal_operation(self, other=None):
        if not other:
            other = self
        return RunTimeError(
            self.start_pos, self.end_pos,
            "Illegal Operation", self.context
        )

    def execute(self, args):
        from Interepter.interepter import RTResult
        return RTResult().failure(self.illegal_operation())

    def add_to(self, other):
        return None, self.illegal_operation(other)

    def sub_by(self, other):
        return None, self.illegal_operation(other)

    def mult_to(self, other):
        return None, self.illegal_operation(other)

    def div_by(self, other):
        return None, self.illegal_operation(other)

    def power_to(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_eq(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_ne(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_lt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_le(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_ge(self, other):
        return None, self.illegal_operation(other)

    def and_this(self, other):
        return None, self.illegal_operation(other)

    def or_this(self, other):
        return None, self.illegal_operation(other)

    def not_(self, other):
        return None, self.illegal_operation(other)

    def is_true(self):
        return False

    def is_false(self):
        return True

    # def copy_num(self):
    #     raise Exception("No Copy Methode Defined ")

    def copy(self):
        print("func copy error")
        raise Exception("No Copy Methode Defined ")
