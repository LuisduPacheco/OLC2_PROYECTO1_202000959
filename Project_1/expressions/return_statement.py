from environment.ast import Ast
from environment.environment import Environment
from interfaces.expression import Expression
from environment.symbol import Symbol
from environment.types import ExpressionType


class ReturnStatement(Expression):

    def __init__(self, line, column, expression):
        self.line = line
        self.column = column
        self.expression = expression

    def execute(self, ast: Ast, env: Environment):
        if env.FunctionValidation():
            if self.expression is None:
                return Symbol(self.line, self.column, None, ExpressionType.RETURN)
            sym = self.expression.execute(ast, env)
            return Symbol(self.line, self.column, sym, ExpressionType.RETURN)
        ast.set_errors('The transfer statement is not inside a function')
        return Symbol(self.line, self.column, None, ExpressionType.NULL)