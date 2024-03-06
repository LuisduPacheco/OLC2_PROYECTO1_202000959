from environment.types import ExpressionType
from environment.symbol import Symbol
from interfaces.expression import Expression

dominant_table = [
    [ExpressionType.NUMBER, ExpressionType.FLOAT, ExpressionType.STRING, ExpressionType.NULL, ExpressionType.NULL],
    [ExpressionType.FLOAT, ExpressionType.FLOAT, ExpressionType.STRING, ExpressionType.NULL, ExpressionType.NULL],
    [ExpressionType.STRING, ExpressionType.STRING, ExpressionType.STRING, ExpressionType.STRING, ExpressionType.NULL],
    [ExpressionType.NULL, ExpressionType.NULL, ExpressionType.STRING, ExpressionType.BOOLEAN, ExpressionType.NULL],
    [ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL],
]


class Operation(Expression):
    def __init__(self, line, column, operator, op_left, op_right):
        self.line = line
        self.column = column
        self.operator = operator
        self.op_left = op_left
        self.op_right = op_right

    def execute(self, ast, env):
        op1 = self.op_left.execute(ast, env)
        op2 = self.op_right.execute(ast, env)
        dominant_type = dominant_table[op1.type.value][op2.type.value]

        if self.operator == "+":
            if dominant_type == ExpressionType.NUMBER or dominant_type == ExpressionType.FLOAT or dominant_type == ExpressionType.STRING:
                op_symbol = Symbol(self.line, self.column, op1.value + op2.value, dominant_type)
                return op_symbol

        if self.operator == "-":
            if dominant_type == ExpressionType.NUMBER or dominant_type == ExpressionType.FLOAT:
                return Symbol(self.line, self.column, op1.value - op2.value, dominant_type)
            print("Error: incorrect types to subtract.")

        if self.operator == "*":
            if dominant_type == ExpressionType.NUMBER or dominant_type == ExpressionType.FLOAT:
                return Symbol(self.line, self.column, op1.value * op2.value, dominant_type)
            print("Error: incorrect types to multiply.")

        if self.operator == "/":
            if op2.value == 0 or op2.value == 0.0:
                ast.set_errors("Error: Can not divided by 0.")
            if dominant_type == ExpressionType.NUMBER or dominant_type == ExpressionType.FLOAT:
                return Symbol(self.line, self.column, op1.value / op2.value, dominant_type)
            print("Error: incorrect types to multiply.")

        return Symbol(self.line, self.column, None, ExpressionType.NULL)

