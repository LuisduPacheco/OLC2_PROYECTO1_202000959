from environment.ast import Ast
from environment.environment import Environment
from interfaces.instruction import Instruction
from environment.types import ExpressionType


class ArrayDeclaration(Instruction):
    def __init__(self, line, column, identifier, type_expression, expression):
        self.line = line
        self.column = column
        self.identifier = identifier
        self.type_expression = type_expression
        self.expression = expression

    def execute(self, ast: Ast, env: Environment):

        symbol_array = self.expression.execute(ast, env)

        if symbol_array.type != ExpressionType.ARRAY:
            ast.set_errors("The expression is not an array.")
            return

        for sym in symbol_array.value:
            if sym.type != self.type_expression and sym.type != ExpressionType.ARRAY:
                ast.set_errors("The array contains incorrect types.")
                return

        env.save_variable(ast, self.identifier, symbol_array)
