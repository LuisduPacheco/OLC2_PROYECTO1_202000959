from environment.ast import Ast
from environment.environment import Environment
from interfaces.expression import Expression


class Access(Expression):
    def __init__(self, line: int, column: int, identifier):
        self.line = line
        self.column = column
        self.identifier = identifier

    def execute(self, ast: Ast, env: Environment):
        # Search in the environment
        print(self.identifier)
        if self.identifier in env.table:
            return env.get_variable(ast, self.identifier)
        if self.identifier in env.constants:
            return env.get_constant(ast, self.identifier)

