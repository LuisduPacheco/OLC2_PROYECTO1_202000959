from environment.types import ExpressionType


def root_executor(instruction_list, ast, env):
    for instruction in instruction_list:
        instruction.execute(ast, env)


def statement_executor(instruction_list, ast, env):
    for instruction in instruction_list:
        result = instruction.execute(ast, env)
        if result is not None:
            if result.type == ExpressionType.RETURN:
                return result.value
            return result

