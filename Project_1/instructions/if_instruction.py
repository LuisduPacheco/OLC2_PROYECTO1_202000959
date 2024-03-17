from environment.ast import Ast
from environment.environment import Environment
from environment.execute import statement_executor
from interfaces.instruction import Instruction


class IfInstruction(Instruction):
    def __init__(self, line, column, expression, block, else_block = None):
        self.line = line
        self.column = column
        self.expression = expression
        self.block = block
        self.else_block = else_block

    def execute(self, ast: Ast, env: Environment):
        # Get the symbol
        result_symbol = self.expression.execute(ast, env)
        if result_symbol.value:
            # Create env of the IF
            if_env = Environment(env, "IF")
            return_value = statement_executor(self.block, ast, if_env)
            if return_value is not None:
                return return_value
        elif self.else_block:  # Check if else block exists for else if
            # Create env of the ELSE IF
            else_if_env = Environment(env, "ELSE IF")
            return_value = statement_executor(self.else_block, ast, else_if_env)
            if return_value is not None:
                return return_value
        return None
