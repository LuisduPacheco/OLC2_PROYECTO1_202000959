from environment.ast import Ast
from environment.environment import Environment
from interfaces.expression import Expression


class InterfaceAccess(Expression):
    def __init__(self, line, column, expression, identifier):
        self.line = line
        self.column = column
        self.expression = expression
        self.identifier = identifier

    def execute(self, ast: Ast, env: Environment):
        env_interface = self.expression.execute(ast, env)

        sym = env_interface.get_variable(ast, self.identifier)
        return sym
