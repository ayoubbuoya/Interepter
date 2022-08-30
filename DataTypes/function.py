import os
from DataTypes.list import List
from DataTypes.string import String
from DataTypes.value import Value
from DataTypes.number import Number
from Errors.errors import RunTimeError


class BaseFunction(Value):
    def __init__(self, name) -> None:
        super().__init__()
        self.name = name or "<anonymous>"

    def generate_new_context(self):
        from Interepter.interepter import Vars
        from Errors.errors import Context
        new_context = Context(self.name, self.context, self.start_pos)
        new_context.vars = Vars(new_context.parent.vars)
        return new_context

    def check_args(self, func_args, args):
        from Interepter.interepter import RTResult
        from Errors.errors import RunTimeError

        res = RTResult()
        if len(args) > len(func_args):
            return res.failure(RunTimeError(
                self.start_pos, self.end_pos,
                f"Too Many Args Passed Into {self}", self.context
            ))
        if len(args) > len(func_args):
            return res.failure(RunTimeError(
                self.start_pos, self.end_pos,
                f"Few Args Passed Into {self}", self.context
            ))

        return res.success(None)

    def populate_args(self, func_args, args, exec_context):
        for i in range(len(args)):
            arg_name = func_args[i]
            arg_value = args[i]
            arg_value.set_context(exec_context)
            exec_context.vars.set_var(arg_name, arg_value)

    def check_and_populate_args(self, func_args, args, exec_context):
        from Interepter.interepter import RTResult
        res = RTResult()
        res.register(self.check_args(func_args, args))
        if res.err:
            return res
        self.populate_args(func_args, args, exec_context)
        return res.success(None)


class Function(BaseFunction):
    def __init__(self, name,  args, body) -> None:
        super().__init__(name)
        self.func_args = args
        self.func_body = body

    def execute(self, args):
        from Interepter.interepter import RTResult, Interepter, Vars
        from Errors.errors import RunTimeError, Context
        res = RTResult()
        interepter = Interepter()
        exec_context = self.generate_new_context()

        res.register(self.check_and_populate_args(
            self.func_args, args, exec_context))
        if res.error:
            return res
        value = res.register(interepter.visit(self.func_body, exec_context))
        print(value)
        if res.err:
            return res

        return res.success(value)

    def copy(self):
        copy = Function(self.name, self.func_args, self.func_body)
        copy.set_pos(self.start_pos, self.end_pos)
        copy.set_context(self.context)
        return copy

    def __repr__(self) -> str:
        return f"<function {self.name}>"


class BuiltInFunction(BaseFunction):
    def __init__(self, name) -> None:
        super().__init__(name)

    def execute(self, args):
        from Interepter.interepter import RTResult
        res = RTResult()
        exec_context = self.generate_new_context()

        method_name = f"execute_{self.name}"
        # equivalent to self.method_name
        method = getattr(self, method_name, self.no_visit_method)
        res.register(self.check_and_populate_args(
            method.func_args, args, exec_context))
        if res.err:
            return res
        ret_val = res.register(method(exec_context))
        return res.success(ret_val)

    def no_visit_method(self, node, context):
        raise Exception(f"No execute_{self.name} method defined")

    def copy(self):
        copy = BuiltInFunction(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.start_pos, self.end_pos)
        return copy

    # buil-in funcions
    def execute_affichi(self, exec_ctx):
        from Interepter.interepter import RTResult
        print(str(exec_ctx.vars.get_var("value")))
        return RTResult().success(Number.null)
    execute_affichi.func_args = ["value"]

    def execute_input(self, exec_ctx):
        from Interepter.interepter import RTResult
        text = input()
        return RTResult().success(String(text))
    execute_input.func_args = []

    def execute_input_int(self, exec_ctx):
        from Interepter.interepter import RTResult
        while True:
            text = input()
            try:
                num = int(text)
                break
            except ValueError:
                print(f"'{text}' must be an integer. Try again!")
        return RTResult().success(Number(num))
    execute_input_int.func_args = []

    def execute_clear(self, exec_ctx):
        from Interepter.interepter import RTResult
        os.system("clear" if os.name == "posix" else "cls")
        return RTResult().success(Number.null)
    execute_clear.func_args = []

    def execute_is_number(self, exec_ctx):
        from Interepter.interepter import RTResult
        is_number = isinstance(exec_ctx.vars.get_var("value"), Number)
        return RTResult().success(Number.true if is_number else Number.false)
    execute_is_number.func_args = ["value"]

    def execute_is_string(self, exec_ctx):
        from Interepter.interepter import RTResult
        is_string = isinstance(exec_ctx.vars.get_var("value"), String)
        return RTResult().success(Number.true if is_string else Number.false)
    execute_is_string.func_args = ["value"]

    def execute_is_list(self, exec_ctx):
        from Interepter.interepter import RTResult
        is_list = isinstance(exec_ctx.vars.get_var("value"), List)
        return RTResult().success(Number.true if is_list else Number.false)
    execute_is_list.func_args = ["value"]

    def execute_is_function(self, exec_ctx):
        from Interepter.interepter import RTResult
        is_function = isinstance(exec_ctx.vars.get_var("value"), BaseFunction)
        return RTResult().success(Number.true if is_function else Number.false)
    execute_is_function.func_args = ["value"]

    def execute_append(self, exec_ctx):
        from Interepter.interepter import RTResult
        list_ = exec_ctx.vars.get_var("list")
        value = exec_ctx.vars.get_var("value")

        if not isinstance(list_, List):
            return RTResult().failure(RunTimeError(
                self.start_pos, self.end_pos,
                "First argument must be list",
                exec_ctx
            ))
        list_.elements.append(value)
        return RTResult().success(list_)
    execute_append.func_args = ["list", "value"]

    def execute_extend(self, exec_ctx):
        from Interepter.interepter import RTResult
        list1 = exec_ctx.vars.get_var("list1")
        list2 = exec_ctx.vars.get_var("list2")

        if not isinstance(list1, List):
            return RTResult().failure(RunTimeError(
                self.start_pos, self.end_pos,
                "First argument must be list",
                exec_ctx
            ))

        if not isinstance(list2, List):
            return RTResult().failure(RunTimeError(
                self.start_pos, self.end_pos,
                "Second argument must be list",
                exec_ctx
            ))
        list1.elements.extend(list2.elements)
        return RTResult().success(list1)
    execute_extend.func_args = ["list1", "list2"]

    def execute_pop(self, exec_ctx):
        from Interepter.interepter import RTResult
        list_ = exec_ctx.vars.get_var("list")
        index = exec_ctx.vars.get_var("index")

        if not isinstance(list_, List):
            return RTResult().failure(RunTimeError(
                self.start_pos, self.end_pos,
                "First argument must be list",
                exec_ctx
            ))
        try:
            element = list_.elements.pop(index.value)
        except:
            return RTResult().failure(RunTimeError(
                self.start_pos, self.end_pos,
                'Element at this index could not be removed from list because index is out of bounds',
                exec_ctx
            ))
        return RTResult().success(element)
    execute_pop.func_args = ["list", "index"]

    def __repr__(self) -> str:
        return f"<built-in function {self.name}>"


# built-in Function
BuiltInFunction.affichi = BuiltInFunction("affichi")
BuiltInFunction.input = BuiltInFunction("input")
BuiltInFunction.input_int = BuiltInFunction("input_int")
BuiltInFunction.clear = BuiltInFunction("clear")
BuiltInFunction.is_number = BuiltInFunction("is_number")
BuiltInFunction.is_string = BuiltInFunction("is_string")
BuiltInFunction.is_list = BuiltInFunction("is_list")
BuiltInFunction.is_function = BuiltInFunction("is_function")
BuiltInFunction.append = BuiltInFunction("append")
BuiltInFunction.pop = BuiltInFunction("pop")
