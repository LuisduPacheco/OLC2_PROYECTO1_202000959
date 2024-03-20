from environment.ast import Ast
from environment.environment import Environment
from interfaces.instruction import Instruction


class FunctionStatement(Instruction):
    def __init__(self, line, column, identifier, params, type_expression, block):
        self.line = line
        self.column = column
        self.identifier = identifier
        self.params = params
        self.type_expression = type_expression
        self.block = block

    def execute(self, ast: Ast, env: Environment):
        function_data = {
            'params': self.params,
            'type': self.type_expression,
            'block': self.block
        }

        env.save_function(ast, self.identifier, function_data)
