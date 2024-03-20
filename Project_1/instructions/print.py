from environment.types import ExpressionType
from interfaces.instruction import Instruction
from expressions.primitive import Primitive
from interfaces.expression import Expression


class Print(Instruction):

    def __init__(self, line: int, column: int, exp):
        self.line = line
        self.column = column
        self.exp = exp

    def execute(self, ast, env):
        out_text = ""
        for expression in self.exp:
            sym = expression.execute(ast, env)
            if sym.type == ExpressionType.ARRAY:
                out_text += "["
                for arr in sym.value:
                    out_text += " " + str(arr.value) + ", "
                out_text += "]"
            else:
                out_text += " " + str(sym.value)
        ast.set_console(out_text)

    def PrintMatrix(self, array, out_value):
        for arr in array:
            if arr == ExpressionType.ARRAY:
                return self.PrintMatrix(arr, out_value)
            else:
                out_value += str(arr)
        return out_value

