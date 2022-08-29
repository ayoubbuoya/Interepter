
class NumberNode:
    def __init__(self, token) -> None:
        self.tok = token

        self.start_pos = self.tok.start_pos
        self.end_pos = self.tok.end_pos

    def __repr__(self) -> str:
        return str(self.tok)


# Opration Nodes


class BinOpNode:
    def __init__(self, left_node, operation, right_node) -> None:
        self.left = left_node
        self.op = operation
        self.right = right_node

        self.start_pos = self.left.start_pos
        self.end_pos = self.right.end_pos

    def __repr__(self) -> str:
        return f"({self.left}, {self.op}, {self.right})"

# add supports for parenthesis


class UnaryOpNode:
    def __init__(self, operation, node) -> None:
        self.op = operation
        self.node = node

        self.start_pos = self.op.start_pos
        self.end_pos = self.node.end_pos

    def __repr__(self) -> str:
        return f"({self.op}, {self.node})"


class VarAccessNode:
    def __init__(self, name) -> None:
        self.var_name = name
        self.start_pos = self.var_name.start_pos
        self.end_pos = self.var_name.end_pos

    def __repr__(self) -> str:
        return str(self.var_name)


class VarAssignNode:
    def __init__(self, name, value) -> None:
        self.var_name = name
        self.value = value
        self.start_pos = self.var_name.start_pos
        self.end_pos = self.var_name.end_pos

    def __repr__(self) -> str:
        return f"{self.var_name} : {self.value}"


class IFNode():
    def __init__(self, cases, else_case) -> None:
        self.cases = cases
        self.else_case = else_case

        self.start_pos = self.cases[0][0].start_pos  # condition of first case
        self.end_pos = (self.else_case or self.cases[-1][0]).end_pos


class WhileNode:
    def __init__(self, condition, body) -> None:
        self.condition = condition
        self.body = body

        self.start_pos = self.condition.start_pos
        self.end_pos = self.body.end_pos


class ForNode:
    def __init__(self, var_name, start_value, end_value, step_value, body_value) -> None:
        self.var_name = var_name
        self.start_val = start_value
        self.end_val = end_value
        self.step_val = step_value
        self.body_val = body_value

        self.start_pos = self.var_name.start_pos
        self.end_pos = self.body_val.end_pos

    def __repr__(self) -> str:
        return f"{self.var_name} : [{self.start_val}, {self.end_val}], {self.step_val}: {self.body_val} "


class FunctionNode:
    def __init__(self, func_name, args_name, body) -> None:
        self.func_name = func_name
        self.args_name = args_name
        self.body = body

        if self.func_name:
            self.start_pos = self.func_name.start_pos
        elif len(self.args_name) > 0:
            self.start_pos = self.args_name[0].start_pos
        else:
            self.start_pos = self.body.start_pos

        self.end_pos = self.body.end_pos

    def __repr__(self) -> str:
        return str(self.body)


class CallFuncNode:
    def __init__(self, func_to_call, func_args) -> None:
        self.func_to_call = func_to_call
        self.func_args = func_args

        self.start_pos = self.func_to_call.start_pos

        if len(self.func_args) > 0:
            self.end_pos = self.func_args[-1].end_pos
        else:
            self.end_pos = self.func_to_call.end_pos

    def __repr__(self) -> str:
        return f"{self.func_to_call}, {self.func_args} "


class StringNode:
    def __init__(self, token) -> None:
        self.tok = token

        self.start_pos = self.tok.start_pos
        self.end_pos = self.tok.end_pos

    def __repr__(self) -> str:
        return str(self.tok)
