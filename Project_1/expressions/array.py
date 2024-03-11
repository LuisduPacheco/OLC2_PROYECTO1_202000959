from environment.ast import Ast
from environment.environment import Environment
from environment.symbol import Symbol
from environment.types import ExpressionType
from interfaces.instruction import Instruction


class Array(Instruction):
    def __init__(self, line, column, list_exp):
        self.line = line
        self.column = column
        self.list_exp = list_exp

    def execute(self, ast: Ast, env: Environment):
        value_arr: list = []
        for exp in self.list_exp:
            index_exp = exp.execute(ast, env)
            value_arr.append(index_exp)
        return Symbol(self.line, self.column, value_arr, ExpressionType.ARRAY)
