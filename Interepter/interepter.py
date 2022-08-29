from DataTypes.number import Number
from DataTypes.function import Function
from DataTypes.string import String
from DataTypes.list import List
from Lexer.lexer import Lexer
from Parser.parser import Parser
from Errors.errors import *
from Tokens_Keywords.toks_keys import *


class RTResult():
    # It Is For handling runtimes errors like the  parseResult class.
    def __init__(self) -> None:
        self.err = None
        self.value = None

    def register(self, res):
        if self.err:
            self.err = res.err
        return res.value

    def success(self, value):
        self.value = value
        return self

    def failure(self, error):
        self.err = error
        return self


# Number Value


class Interepter:
    # Visit Nodes (binopnde , number node , ..)
    def visit(self, node, context):
        node_type = type(node).__name__
        if node_type == "NumberNode":
            return self.visit_number_node(node, context)
        elif node_type == "BinOpNode":
            return self.visit_bin_op_node(node, context)
        elif node_type == "UnaryOpNode":
            return self.visit_unary_op_node(node, context)
        elif node_type == "VarAccessNode":
            return self.visit_var_access_node(node, context)
        elif node_type == "VarAssignNode":
            return self.visit_var_assign_node(node, context)
        elif node_type == "IFNode":
            return self.visit_if_node(node, context)
        elif node_type == "ForNode":
            return self.visit_for_node(node, context)
        elif node_type == "WhileNode":
            return self.visit_while_node(node, context)
        elif node_type == "FunctionNode":
            return self.visit_func_def_node(node, context)
        elif node_type == "CallFuncNode":
            return self.visit_call_func_node(node, context)
        elif node_type == "StringNode":
            return self.visit_string_node(node, context)
        elif node_type == "ListNode":
            return self.visit_list_node(node, context)
        else:
            return self.no_visit(node, context)

    def visit_number_node(self, node, context):
        # print("number")
        res = RTResult()
        num = Number(node.tok.value)
        num.set_context(context)
        num.set_pos(node.start_pos, node.end_pos)
        return res.success(num)

    def visit_bin_op_node(self, node, context):
        # print("bin")
        res = RTResult()
        # visit left and right
        left = res.register(self.visit(node.left, context))
        if res.err:
            return res
        right = res.register(self.visit(node.right, context))
        if res.err:
            return res

        if node.op.type == PLUS_T:
            result, error = left.add_to(right)
        elif node.op.type == MINUS_T:
            result, error = left.sub_by(right)
        elif node.op.type == MULT_T:
            result, error = left.mult_to(right)
        elif node.op.type == DIV_T:
            result, error = left.div_by(right)
        elif node.op.type == POWER_T:
            result, error = left.power_by(right)
        elif node.op.type == LESS_EQUAL_T:
            result, error = left.get_comparison_le(right)
        elif node.op.type == GREAT_EQUAL_T:
            result, error = left.get_comparison_ge(right)
        elif node.op.type == LESS_THAN_T:
            result, error = left.get_comparison_lt(right)
        elif node.op.type == GREAT_THAN_T:
            result, error = left.get_comparison_gt(right)
        elif node.op.type == NOT_EQUAL_T:
            result, error = left.get_comparison_ne(right)
        elif node.op.type == DOUBLE_EQUAL_T:
            result, error = left.get_comparison_eq(right)
        elif node.op.matches(KEYWORD_T, "and"):
            result, error = left.and_this(right)
        elif node.op.matches(KEYWORD_T, "or"):
            result, error = left.or_this(right)

        if error:
            return res.failure(error)
        else:
            result.set_pos(node.start_pos, node.end_pos)
            return res.success(result)

    def visit_unary_op_node(self, node, context):
        res = RTResult()
        # visit child node
        num = res.register(self.visit(node.node, context))
        if res.err:
            return res
        if node.op.type == MINUS_T:
            num, error = num.mult_to(Number(-1))
        elif node.op.matches(KEYWORD_T, "not"):
            num, error = num.not_()
        if error:
            return res.failure(error)
        else:
            num.set_pos(node.start_pos, node.end_pos)
            return res.success(num)

    def visit_var_access_node(self, node, context):
        res = RTResult()
        var_name = node.var_name.value
        value = context.vars.get_var(var_name)

        if not value:
            return res.failure(RunTimeError(
                node.start_pos, node.end_pos,
                f"'{var_name}' is undefined", context
            ))
        value = value.copy()
        value.set_pos(node.start_pos, node.end_pos)
        return res.success(value)

    def visit_var_assign_node(self, node, context):
        res = RTResult()
        var_name = node.var_name.value
        # define the proper node for value
        var_value = res.register(self.visit(node.value, context))
        if res.err:
            return res
        context.vars.set_var(var_name, var_value)
        return res.success(var_value)

    def visit_if_node(self, node, context):
        res = RTResult()

        for (condition, do) in node.cases:
            cond_val = res.register(self.visit(condition, context))
            if res.err:
                return res
            if cond_val.is_true():
                do_val = res.register(self.visit(do, context))
                if res.err:
                    return res
                return res.success(do_val)
        if node.else_case:
            else_val = res.register(self.visit(node.else_case, context))
            if res.err:
                return res
            return res.success(else_val)

        return res.success(None)

    def visit_while_node(self, node, context):
        res = RTResult()
        elements = []

        while True:
            condition = res.register(self.visit(node.condition, context))
            if res.err:
                return res
            if condition.is_false():
                break
            elements.append(res.register(self.visit(node.body, context)))
            if res.err:
                return res

        return res.success(
            List(elements).set_context(context).set_pos(
                node.start_pos, node.end_pos)
        )

    def visit_for_node(self, node, context):
        res = RTResult()
        elements = []

        start_val = res.register(self.visit(node.start_val, context))
        if res.err:
            return res
        end_val = res.register(self.visit(node.end_val, context))
        if res.err:
            return res
        if node.step_val:
            step_val = res.register(self.visit(node.step_val, context))
            if res.err:
                return res
        else:
            step_val = Number(1)

        i = start_val.value

        if step_val.value >= 0:
            def iter_cond(): return i < end_val.value
        else:
            def iter_cond(): return i > end_val.value

        while iter_cond():
            context.vars.set_var(node.var_name.value, Number(i))
            i += step_val.value

            elements.append(res.register(self.visit(node.body_val, context)))
            if res.err:
                return res

        return res.success(
            List(elements).set_context(context).set_pos(
                node.start_pos, node.end_pos)

        )

    def visit_func_def_node(self, node, context):
        res = RTResult()

        func_name = node.func_name.value if node.func_name else None
        func_body = node.body
        args_name = [arg_name.value for arg_name in node.args_name]
        func_value = Function(func_name, args_name, func_body)
        func_value.set_pos(node.start_pos, node.end_pos)
        func_value.set_context(context)

        if node.func_name:
            context.vars.set_var(func_name, func_value)

        return res.success(func_value)

    def visit_call_func_node(self, node, context):
        res = RTResult()

        args = []
        val_to_call = res.register(self.visit(node.func_to_call, context))
        if res.err:
            return res
        val_to_call = val_to_call.copy()
        val_to_call.set_pos(node.start_pos, node.end_pos)
        # val_to_call.set_context(context)

        for arg_node in node.func_args:
            args.append(res.register(self.visit(arg_node, context)))
            if res.err:
                return res
        value = res.register(val_to_call.execute(args))
        if res.err:
            return res

        return res.success(value)

    def visit_string_node(self, node, context):
        value = String(node.tok.value)
        value.set_context(context)
        value.set_pos(node.start_pos, node.end_pos)
        return RTResult().success(value)

    def visit_list_node(self, node, context):
        res = RTResult()
        elements = []

        for elem_node in node.element_nodes:
            elements.append(res.register(self.visit(elem_node, context)))
            if res.err:
                return res
        ret_list = List(elements)
        ret_list.set_context(context)
        ret_list.set_pos(node.start_pos, node.end_pos)

        return res.success(ret_list)

    def no_visit(self, node, context):
        raise Exception(f"No Visit {type(node).__name__} Undedined")


class Vars:
    def __init__(self, parent=None) -> None:
        self.vars = {}
        self.parent = parent

    def get_var(self, name):
        # key == name , default value if key not exist
        value = self.vars.get(name, None)
        if value == None and self.parent:
            return self.parent.get_var(name)
        return value

    def set_var(self, name, value):
        self.vars[name] = value

    def remove_var(self, name):
        del self.vars[name]


# define default vars
default_vars = Vars()
default_vars.set_var("null", Number(0))
default_vars.set_var("true", Number(1))
default_vars.set_var("false", Number(0))


def run(instruction, file_name="<stdin>"):
    lexer = Lexer(instruction, file_name)
    tokens, error = lexer.get_tokens()
    if error:
        return None, error
    # print(tokens)
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.err:
        return None, ast.err
    # print(ast.node)
    interepter = Interepter()
    context = Context("<Program>")
    context.vars = default_vars
    result = interepter.visit(ast.node, context)

    return result.value, result.err
