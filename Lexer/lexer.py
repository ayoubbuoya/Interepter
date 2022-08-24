from Tokens_Keywords.toks_keys import *
from Errors.errors import *


class Token:
    def __init__(self, type, value=None, start_pos=None, end_pos=None) -> None:
        self.type = type
        self.value = value

        if start_pos:
            self.start_pos = start_pos.copy_pos()
            self.end_pos = start_pos.copy_pos()
            self.end_pos.next_pos()
        if end_pos:
            self.end_pos = end_pos

    # function to check are the given type and value equals to token .. or not
    def matches(self, type, value):
        return self.type == type and self.value == value

    def __repr__(self) -> str:
        if self.value:
            return f"{self.type}:{self.value}"
        # else
        return self.type

# The Tokenizer


class Lexer:
    def __init__(self, text, filename) -> None:
        self.fn = filename
        self.txt = text
        # position of current characte
        self.pos = Position(-1, 0, -1, filename, text)
        self.last_pos = len(self.txt) - 1
        self.current = None
        self.next()

    def next(self):
        if self.pos.ind < self.last_pos:
            self.pos.next_pos(self.current)
            self.current = self.txt[self.pos.ind]
        else:
            self.current = None

    def get_tokens(self):
        tokens = []

        while self.current != None:
            # Ignore whitespaces,tabs,..
            if self.current == TAB:
                self.next()
            elif self.current == WHITESPACE:
                self.next()
            # Basic Math Operations
            elif self.current == "+":
                tokens.append(Token(PLUS_T, start_pos=self.pos))
                self.next()
            elif self.current == "-":
                tokens.append(Token(MINUS_T, start_pos=self.pos))
                self.next()
            elif self.current == "*":
                tokens.append(Token(MULT_T, start_pos=self.pos))
                self.next()
            elif self.current == "/":
                tokens.append(Token(DIV_T, start_pos=self.pos))
                self.next()
            elif self.current == "^":
                tokens.append(Token(POWER_T, start_pos=self.pos))
                self.next()
            # Parenthesis
            elif self.current == "(":
                tokens.append(Token(LPAREN_T, start_pos=self.pos))
                self.next()
            elif self.current == ")":
                tokens.append(Token(RPAREN_T, start_pos=self.pos))
                self.next()
            # Numbers
            elif self.current in DIGITS:
                tokens.append(self.get_number_tok())
            # variables related stuff

            elif self.current in LETTERS:
                tokens.append(self.get_identifier())
            # comparisons tokens
            elif self.current == "!":
                tok, err = self.get_not_equal_tok()
                if err:
                    return [], err
                tokens.append(tok)
            elif self.current == "=":
                tokens.append(self.get_equal_tok())
            elif self.current == "<":
                tokens.append(self.get_less_than_tok())
            elif self.current == ">":
                tokens.append(self.get_great_than_tok())
            else:
                # raise char error
                err_start_pos = self.pos.copy_pos()
                char = self.current
                self.next()
                return [], IllegalCharError(err_start_pos, self.pos, f"' {char} '")

        # add the end of file token
        tokens.append(Token(EOF_T, start_pos=self.pos))

        return tokens, None

    def get_great_than_tok(self):
        start_pos = self.pos.copy_pos()
        self.next()
        if self.current == "=":
            self.next()
            return Token(GREAT_EQUAL_T, start_pos=start_pos, end_pos=self.pos)
        else:
            return Token(GREAT_THAN_T, start_pos=start_pos, end_pos=self.pos)

    def get_less_than_tok(self):
        start_pos = self.pos.copy_pos()
        self.next()
        if self.current == "=":
            self.next()
            return Token(LESS_EQUAL_T, start_pos=start_pos, end_pos=self.pos)
        else:
            return Token(LESS_THAN_T, start_pos=start_pos, end_pos=self.pos)

    def get_equal_tok(self):
        start_pos = self.pos.copy_pos()
        self.next()
        if self.current == "=":
            self.next()
            return Token(DOUBLE_EQUAL_T, start_pos=start_pos, end_pos=self.pos)
        else:
            return Token(EQUAL_T, start_pos=start_pos, end_pos=self.pos)

    def get_not_equal_tok(self):
        start_pos = self.pos.copy_pos()
        self.next()

        if self.current == "=":
            self.next()
            return Token(NOT_EQUAL_T, start_pos=start_pos, end_pos=self.pos), None
        else:
            return None, ExpectedCharError(
                start_pos, self.pos,
                "'=' (after '!')"
            )

    def get_identifier(self):
        idn = ""
        start_pos = self.pos.copy_pos()

        while self.current != None and self.current in LETTERS_DIGITS + "_":
            idn += self.current
            self.next()

        if idn in KEYWORDS:
            return Token(KEYWORD_T, idn, start_pos, self.pos)
        else:
            return Token(IDENTIFIER_T, idn, start_pos, self.pos)

    def get_number_tok(self):

        num = ""  # complete number
        dot = False
        Float = False
        start_pos = self.pos.copy_pos()

        while self.current != None and self.current in DIGITS + ".":

            # Find a dot ==> Float type
            if self.current == ".":
                if dot:
                    break
                else:
                    dot = True
                    Float = True
                    num += self.current
                    self.next()
            else:
                num += self.current
                self.next()

        # return token
        if Float:
            return Token(FLOAT_T, float(num), start_pos, self.pos)

        return Token(INT_T, int(num), start_pos, self.pos)
