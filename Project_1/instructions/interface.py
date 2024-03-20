from environment.ast import Ast
from environment.environment import Environment
from interfaces.instruction import Instruction


class Interface(Instruction):
    def __init__(self, line, column, identifier, attribute):
        self.line = line
        self.column = column
        self.identifier = identifier
        self.attribute = attribute

    def execute(self, ast: Ast, env: Environment):
        # The struct is stored in a dictionary
        # The id is the key name
        # The value is the list of attributes that consists of dictionaries.
        env.save_struct(ast, self.identifier, self.attribute)