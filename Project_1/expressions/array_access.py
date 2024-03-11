from environment.ast import Ast
from environment.environment import Environment
from interfaces.expression import Expression
from environment.types import ExpressionType


class ArrayAccess(Expression):

    def __init__(self, line: int, column: int, array, index):
        self.line = line
        self.column = column
        self.array = array
        self.index = index

    def execute(self, ast: Ast, env: Environment):
        # Bring the array
        sym = self.array.execute(ast, env)

        if sym.type != ExpressionType.ARRAY:
            ast.set_errors("The variables isn't an array.")
            return

        index_value = self.index.execute(ast, env)
        if index_value.type != ExpressionType.NUMBER:
            ast.set_errors('Index must be an integer, incorrect value.')
            return
        return sym.value[index_value]


