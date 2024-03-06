from environment.types import ExpressionType


class Symbol:
    def __init__(self, line: int, column: int, value, type_expression: ExpressionType):
        self.line = line
        self.column = column
        self.value = value
        self.type = type_expression
