from environment.ast import Ast
from environment.environment import Environment
from interfaces.expression import Expression

class Acces(Expression):

    def __init__(self, line: int, column: int, identifier):
        self.line = line
        self.column = column
        self.identifier = identifier
    def execute(self, ast: Ast, env: Environment):
        # Search in the environment
        print(self.identifier)
        return env.get_variable(ast, self.identifier)

