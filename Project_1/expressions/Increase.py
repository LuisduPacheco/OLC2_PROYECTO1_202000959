from interfaces.expression import Expression
from environment.environment import Environment
from environment.ast import Ast


class Increase(Expression):
    def __init__(self, line, column, identifier, expression):
        self.line = line
        self.column = column
        self.identifier = identifier
        self.expression = expression

    def execute(self, ast, env):
        result = self.expression.execute(ast, env)
        env.increase_variable(ast, self.identifier, result)

