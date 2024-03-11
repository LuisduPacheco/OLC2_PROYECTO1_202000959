from environment.types import ExpressionType
from interfaces.instruction import Instruction
class Constants(Instruction):
    def __init__(self, line, column, identifier, type_exp, expression):
        self.line = line
        self.column = column
        self.identifier = identifier
        self.type_exp = type_exp
        self.expression = expression

    def execute(self, ast, env):
        if self.type_exp is None:
            result = self.expression.execute(ast, env)
            if result.type == ExpressionType.STRING:
                self.type_exp = ExpressionType.STRING
            elif result.type == ExpressionType.NUMBER:
                self.type_exp = ExpressionType.NUMBER
            elif result.type == ExpressionType.FLOAT:
                self.type_exp = ExpressionType.FLOAT
            elif result.type == ExpressionType.BOOLEAN:
                self.type_exp = ExpressionType.BOOLEAN

            if result.type != self.type_exp:
                ast.set_errors(f"Error: Type incorrect{self.type_exp}")
                return
            env.save_constant(ast, self.identifier, result)
        else:
            # Get symbol
            print(self.expression)
            result = self.expression.execute(ast, env)
            # Validate type
            if result.type != self.type_exp:
                ast.set_errors("Error: Type incorrect.")
                return

            # Add to the environment
            env.save_constant(ast, self.identifier, result)
