from interfaces.instruction import Instruction


class Assignment(Instruction):
    def __init__(self, line, column, identifier, expression):
        self.line = line
        self.column = column
        self.identifier = identifier
        self.expression = expression

    def execute(self, ast, env):
        result = self.expression.execute(ast, env)
        env.set_variable(ast, self.identifier, result)

