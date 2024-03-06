from interfaces.expression import Expression
from environment.symbol import Symbol
from environment.types import ExpressionType


class Primitive(Expression):
    def __init__(self, line, column, value, type_primitive: ExpressionType):
        self.line = line
        self.column = column
        self.value = value
        self.type_primitive = type_primitive

    def execute(self, ast, env):
        return Symbol(self.line, self.column, self.value, self.type_primitive)
