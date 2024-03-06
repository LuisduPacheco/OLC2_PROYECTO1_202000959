from interfaces.instruction import Instruction
from environment.types import ExpressionType


class Declaration(Instruction):

    def __init__(self, line: int, column: int, identifier, type_exp, expression):
        self.line = line
        self.column = column
        self.identifier = identifier
        self.type_exp = type_exp
        self.expression = expression

    def execute(self, ast, env):
        # Get symbol
        result = self.expression.execute(ast, env)

        # Validate type
        if result.type_exp != self.type_exp:
            ast.set_errors("Error: Type incorrect.")
            return

        # Add to the environment
        env.save_variable(ast, self.identifier, result)

