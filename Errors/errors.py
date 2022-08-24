from Tokens_Keywords.toks_keys import *


class Position:
    def __init__(self, index, line, column, filename, filecontent) -> None:
        self.ind = index
        self.ln = line
        self.col = column
        self.fn = filename
        self.ftxt = filecontent

    def __repr__(self) -> str:
        return f"Position({self.ind}, {self.ln}, {self.col}, {self.fn}, {self.ftxt})"

    def next_pos(self, current_char=None):
        self.ind += 1
        self.col += 1
        if current_char == NEWLINE:
            self.ln += 1
            self.col = 0

        return self

    def copy_pos(self):
        return Position(self.ind, self.ln, self.col, self.fn, self.ftxt)

# function for styling how error is showed


def string_with_arrows(text, pos_start, pos_end):
    result = ''

    # Calculate indices
    ind_start = max(text.rfind('\n', 0, pos_start.ind), 0)
    ind_end = text.find('\n', ind_start + 1)
    if ind_end < 0:
        ind_end = len(text)

    # Generate each line
    line_count = pos_end.ln - pos_start.ln + 1
    for i in range(line_count):
        # Calculate line columns
        line = text[ind_start:ind_end]
        col_start = pos_start.col if i == 0 else 0
        col_end = pos_end.col if i == line_count - 1 else len(line) - 1

        # Append to result
        result += line + '\n'
        result += ' ' * col_start + '^' * (col_end - col_start)

        # Re-calculate indices
        ind_start = ind_end
        ind_end = text.find('\n', ind_start + 1)
        if ind_end < 0:
            ind_end = len(text)

    return result.replace('\t', '')

# Error


class Error:
    def __init__(self, start_pos, end_pos,  error_name, error_details) -> None:
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.err_name = error_name
        self.err_details = error_details

    def __repr__(self):
        return f"{self.err_name} : {self.err_details}\nFile {self.start_pos.fn}, line {self.start_pos.ln}\n\n{string_with_arrows(self.start_pos.ftxt, self.start_pos, self.end_pos)} "


class IllegalCharError(Error):
    def __init__(self, start_pos, end_pos, error_details) -> None:
        super().__init__(start_pos, end_pos, "Illegal Character", error_details)


class InvalidSyntaxError(Error):
    def __init__(self, start_pos, end_pos, error_details) -> None:
        super().__init__(start_pos, end_pos, "Invalid Syntax", error_details)


class RunTimeError(Error):
    def __init__(self, start_pos, end_pos, error_details, context) -> None:
        super().__init__(start_pos, end_pos, "RunfTime Error", error_details)
        self.context = context

    def generate_traceback(self):
        ret = ''
        pos = self.start_pos
        ctx = self.context

        while ctx:
            ret = f"  File {pos.fn}, line {str(pos.ln + 1)}, in {ctx.display}\n" + ret
            pos = ctx.parent_pos
            ctx = ctx.parent

        return "Traceback (most recent call last):\n" + ret

    def __repr__(self):
        return f"{self.generate_traceback()}{self.err_name} : {self.err_details}\n\n{string_with_arrows(self.start_pos.ftxt, self.start_pos, self.end_pos)} "


class ExpectedCharError(Error):
    def __init__(self, start_pos, end_pos, error_details) -> None:
        super().__init__(start_pos, end_pos, "Expected Character", error_details)


# more details on run time error , showing line module, def, file
class Context:
    def __init__(self, display_name, parent=None, parent_pos=None) -> None:
        self.display = display_name
        self.parent = parent
        self.parent_pos = parent_pos
        self.vars = None
