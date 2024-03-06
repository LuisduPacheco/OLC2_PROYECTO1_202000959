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
        for exp in self.exp:
            sym = exp.execute(ast, env)
            out_text += " " + str(sym.value)
        ast.set_console(out_text)

