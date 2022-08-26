

from DataTypes.value import Value


class Function(Value):
    def __init__(self, name,  args, body) -> None:
        super().__init__()
        self.func_name = name or "<anonymous>"
        self.func_args = args
        self.func_body = body

    def execute(self, args):
        from Interepter.interepter import RTResult, Interepter, Vars
        from Errors.errors import RunTimeError, Context
        res = RTResult()
        interepter = Interepter()
        new_context = Context(self.func_name, self.context, self.start_pos)
        new_context.vars = Vars(new_context.parent.vars)

        # too many passed args
        if len(args) > len(self.func_args):
            return res.failure(RunTimeError(
                self.start_pos, self.end_pos,
                f"Too Many Args Passed Into {self.func_name}", self.context
            ))
        # few passed args
        if len(args) > len(self.func_args):
            return res.failure(RunTimeError(
                self.start_pos, self.end_pos,
                f"Few Args Passed Into {self.func_name}", self.context
            ))

        for i in range(len(args)):
            arg_name = self.func_args[i]
            arg_value = args[i]
            arg_value.set_context(new_context)
            new_context.vars.set_var(arg_name, arg_value)

        value = res.register(interepter.visit(self.func_body, new_context))
        if res.err:
            return res

        return res.success(value)

    def copy(self):
        copy = Function(self.func_name, self.func_args, self.func_body)
        copy.set_pos(self.start_pos, self.end_pos)
        copy.set_context(self.context)
        return copy

    def __repr__(self) -> str:
        return f"<function {self.func_name}>"
