from environment.ast import Ast
from environment.environment import Environment
from environment.execute import statement_executor
from environment.types import ExpressionType
from interfaces.instruction import Instruction


class WhileInstruction(Instruction):
    def __init__(self, line, column, expression, block):
        self.line = line
        self.column = column
        self.expression = expression
        self.block = block

    def execute(self, ast: Ast, env: Environment):
        safe_count = 0
        Flag = None
        Result = None

        while True:
            safe_count += 1
            result = self.expression.execute(ast, env)

            if result.value:
                while_env = Environment(env, "WHILE")
                Flag = statement_executor(self.block, ast, while_env)

                # is a transfer sentence ?
                if Flag is not None:
                    if Flag.type == ExpressionType.BREAK:
                        break
                    if Flag.type == ExpressionType.CONTINUE:
                        continue
                    if Flag.type == ExpressionType.RETURN:
                        return Flag
                else:
                    break

            # Security limit
            if safe_count >= 500:
                ast.set_errors('The cycle limit has been exceeded.')
                break
        return None
