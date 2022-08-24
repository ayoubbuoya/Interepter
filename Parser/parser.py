from Nodes.nodes import *
from Tokens_Keywords.toks_keys import *
from Errors.errors import *


class ParseResult:
    def __init__(self) -> None:
        self.err = None
        self.node = None
        # track how many times we advance in a specific function that have a parse result
        self.next_counter = 0

    # takes another parse result or node

    def register(self, res):
        self.next_counter += res.next_counter
        if res.err:
            self.err = res.err
        return res.node

    def register_next(self):
        self.next_counter += 1

    def success(self, node):
        self.node = node
        return self

    def failure(self, err):
        if not self.err or self.next_counter == 0:
            self.err = err
        return self


# Parser
class Parser:
    def __init__(self, tokens) -> None:
        self.toks = tokens
        self.tok_ind = -1
        self.current = None
        self.next()

    def next(self):
        if self.tok_ind < len(self.toks) - 1:
            self.tok_ind += 1
            self.current = self.toks[self.tok_ind]
        # need it for register function
        return self.current

    def parse(self):
        res = self.expr()
        if not res.err and self.current.type != EOF_T:
            return res.failure(InvalidSyntaxError(
                self.current.start_pos, self.current.end_pos,
                "Expected int, float, identifier, '+', '*', '/', '-'"
            ))
        return res

    # Begin The Gram
    def while_expr(self):
        res = ParseResult()

        res.register_next()
        self.next()
        condition = res.register(self.expr())
        if res.err:
            return res
        if not self.current.matches(KEYWORD_T, "do"):
            return res.failure(InvalidSyntaxError(
                self.current.pos_start, self.current.pos_end,
                "Expected 'do'"
            ))
        res.register_next()
        self.next()
        do = res.register(self.expr())
        if res.err:
            return res

        return res.success(WhileNode(condition, do))

    def for_expr(self):
        res = ParseResult()

        res.register_next()
        self.next()

        if self.current.type != IDENTIFIER_T:
            return res.failure(InvalidSyntaxError(
                self.current.start_pos, self.current.end_pos,
                "Expected identfier!"
            ))
        var_name = self.current
        res.register_next()
        self.next()
        if self.current.type != EQUAL_T:
            return res.failure(InvalidSyntaxError(
                self.current.start_pos, self.current.end_pos,
                "Expected Equal Sign '='"
            ))
        res.register_next()
        self.next()
        start_val = res.register(self.expr())
        if res.err:
            return res

        if not self.current.matches(KEYWORD_T, "to"):
            return res.failure(InvalidSyntaxError(
                self.current.start_pos, self.current.end_pos,
                "Expected 'to'"
            ))
        res.register_next()
        self.next()
        end_val = res.register(self.expr())
        if res.err:
            return res

        if self.current.matches(KEYWORD_T, "step"):
            res.register_next()
            self.next()
            step_val = res.register(self.expr())
            if res.err:
                return res
        else:
            step_val = None
        if not self.current.matches(KEYWORD_T, "do"):
            return res.failure(InvalidSyntaxError(
                self.current.start_pos, self.current.end_pos,
                "Expected 'do'"
            ))
        res.register_next()
        self.next()

        do = res.register(self.expr())
        if res.err:
            return res

        return res.success(ForNode(var_name, start_val, end_val, step_val, do))

    def if_expr(self):
        res = ParseResult()
        cases = []
        else_case = None

        res.register_next()
        self.next()
        condition = res.register(self.expr())
        if res.err:
            return res
        if not self.current.matches(KEYWORD_T, "then"):
            return res.failure(InvalidSyntaxError(
                self.current.pos_start, self.current.pos_end,
                "Expected 'THEN'"
            ))
        else:
            res.register_next()
            self.next()

            do = res.register(self.expr())
            if res.err:
                return res
            cases.append((condition, do))

            while self.current.matches(KEYWORD_T, "elif"):
                res.register_next()
                self.next()

                condition = res.register(self.expr())
                if res.err:
                    return res
                if not self.current.matches(KEYWORD_T, "then"):
                    return res.failure(InvalidSyntaxError(
                        self.current.pos_start, self.current.pos_end,
                        "Expected 'THEN'"
                    ))
                else:
                    res.register_next()
                    self.next()
                    do = res.register(self.expr())
                if res.err:
                    return res
                cases.append((condition, do))

            if self.current.matches(KEYWORD_T, "else"):
                res.register_next()
                self.next()
                else_case = res.register(self.expr())
                if res.err:
                    return res

        return res.success(IFNode(cases, else_case))

    def atom(self):
        res = ParseResult()
        tok = self.current

        if tok.type in (INT_T, FLOAT_T):
            res.register_next()
            self.next()
            return res.success(NumberNode(tok))
        elif tok.type == LPAREN_T:
            res.register_next()
            self.next()
            expr = res.register(self.expr())
            if res.err:
                return res
            if self.current.type == RPAREN_T:
                res.register_next()
                self.next()
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    self.current.start_pos, self.current.end_pos,
                    "Expected ' ) '"
                ))
        elif tok.type == IDENTIFIER_T:
            res.register_next()
            self.next()
            return res.success(VarAccessNode(tok))
        elif tok.matches(KEYWORD_T, "if"):
            if_expr = res.register(self.if_expr())
            if res.err:
                return res
            return res.success(if_expr)
        elif tok.matches(KEYWORD_T, "for"):
            for_expr = res.register(self.for_expr())
            if res.err:
                return res
            return res.success(for_expr)
        elif tok.matches(KEYWORD_T, "while"):
            while_expr = res.register(self.while_expr())
            if res.err:
                return res
            return res.success(while_expr)

        return res.failure(InvalidSyntaxError(
            tok.start_pos, tok.end_pos,
            "Expected  int, float, '+', '*', '/', '-'"
        ))

    def power(self):
        return self.bin_op(self.atom, (POWER_T, ), self.factor)

    def factor(self):
        res = ParseResult()
        tok = self.current

        if tok.type in (MINUS_T, PLUS_T):
            res.register_next()
            self.next()
            factor = res.register(self.factor())
            if res.err:
                return res
            return res.success(UnaryOpNode(tok, factor))

        return self.power()

    def bin_op(self, func1, ops, func2=None):
        if func2 == None:
            func2 = func1
        res = ParseResult()
        left = res.register(func1())  # contains first number value
        if res.err:
            return res
        # check for the operation when we finich
        # the after or added to make function supports keywords
        while self.current.type in ops or (self.current.type, self.current.value) in ops:
            tok_op = self.current
            res.register_next()
            self.next()
            right = res.register(func2())
            if res.err:
                return res
            # result and the left in the next loop if there is * or /
            left = BinOpNode(left, tok_op, right)

        return res.success(left)

    def term(self):
        return self.bin_op(self.factor, (MULT_T, DIV_T))

    def arithm_expr(self):
        return self.bin_op(self.term, (PLUS_T, MINUS_T))

    def compare_expr(self):
        res = ParseResult()
        if self.current.matches(KEYWORD_T, "not"):
            op_tok = self.current
            res.register_next()
            self.next()
            node = res.register(self.compare_expr())
            if res.err:
                return res
            return res.success(UnaryOpNode(op_tok, node))
        else:
            ops = (
                DOUBLE_EQUAL_T, NOT_EQUAL_T, LESS_EQUAL_T,
                GREAT_EQUAL_T, LESS_THAN_T, GREAT_THAN_T
            )
            node = res.register(self.bin_op(self.arithm_expr, ops))
            if res.err:
                # Overwrite err message
                return res.failure(InvalidSyntaxError(
                    self.current.start_pos, self.current.end_pos,
                    "Expected  int, float, '+', '*', '/', '-', 'not'"
                ))

            return res.success(node)

    def expr(self):
        res = ParseResult()

        # skip var and identidier and equals
        if self.current.matches(KEYWORD_T, "var"):
            res.register_next()
            self.next()

            if self.current.type != IDENTIFIER_T:

                return res.failure(InvalidSyntaxError(
                    self.current.start_pos, self.current.end_pos,
                    "Expected Identifier"
                ))
            else:
                var_name = self.current
                res.register_next()
                self.next()

                if self.current.type != EQUAL_T:
                    return res.failure(InvalidSyntaxError(
                        self.current.start_pos, self.current.end_pos,
                        "Expected Equal Sign ' = '"
                    ))
                else:
                    res.register_next()
                    self.next()
                    expr = res.register(self.expr())
                    if res.err:
                        return res
                    return res.success(VarAssignNode(var_name, expr))
        else:
            # node = res.register(self.bin_op(self.term, (PLUS_T, MINUS_T)))
            node = res.register(self.bin_op(
                self.compare_expr, ((KEYWORD_T, "and"), (KEYWORD_T, "or"))))
            # overwriting the err msg
            if res.err:
                return res.failure(InvalidSyntaxError(
                    self.current.start_pos, self.current.end_pos,
                    "Expected 'var', int, float, identifier, '+', '*', '/', '-'"
                ))
            return res.success(node)
