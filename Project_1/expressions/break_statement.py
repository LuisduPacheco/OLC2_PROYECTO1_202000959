from environment.ast import Ast
from environment.environment import Environment
from interfaces.expression import Expression
from environment.symbol import Symbol
from environment.types import ExpressionType


class BreakStatement(Expression):

    def __init__(self, line, column):
        self.line = line
        self.column = column

    def execute(self, ast: Ast, env: Environment):
        if env.loop_validation():
            return Symbol(self.line, self.column, None, ExpressionType.BREAK)
        ast.set_errors('The transfer statement is not inside the cycle.')
        return Symbol(self.line, self.column, None, ExpressionType.NULL)