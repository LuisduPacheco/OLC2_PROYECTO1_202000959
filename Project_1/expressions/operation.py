from environment.types import ExpressionType
from environment.symbol import Symbol
from interfaces.expression import Expression

dominant_table = [
    [ExpressionType.NUMBER, ExpressionType.FLOAT,  ExpressionType.STRING, ExpressionType.NULL,    ExpressionType.NULL],
    [ExpressionType.FLOAT,   ExpressionType.FLOAT,  ExpressionType.STRING, ExpressionType.NULL,    ExpressionType.NULL],
    [ExpressionType.STRING,  ExpressionType.STRING, ExpressionType.STRING, ExpressionType.STRING,  ExpressionType.NULL],
    [ExpressionType.NULL,    ExpressionType.NULL,   ExpressionType.STRING, ExpressionType.BOOLEAN, ExpressionType.NULL],
    [ExpressionType.NULL,    ExpressionType.NULL,   ExpressionType.NULL,   ExpressionType.NULL,    ExpressionType.NULL],
    [ExpressionType.NULL,    ExpressionType.NULL,   ExpressionType.NULL,   ExpressionType.NULL,    ExpressionType.NULL],
    [ExpressionType.NULL,    ExpressionType.NULL,   ExpressionType.NULL,   ExpressionType.NULL,    ExpressionType.NULL],
    [ExpressionType.NULL,    ExpressionType.NULL,   ExpressionType.NULL,   ExpressionType.NULL,    ExpressionType.NULL],
    [ExpressionType.NULL,    ExpressionType.NULL,   ExpressionType.NULL,   ExpressionType.NULL,    ExpressionType.NULL],
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
        op2 = None
        dominant_type = ExpressionType.NULL
        if self.op_right is not None:
            op2 = self.op_right.execute(ast, env)
            dominant_type = dominant_table[op1.type.value][op2.type.value]
        elif self.operator == '!':
            dominant_type = ExpressionType.BOOLEAN

        if self.operator == "+":
            op_symbol = Symbol(self.line, self.column, op1.value + op2.value, dominant_type)
            return op_symbol

        if self.operator == "-":
            if dominant_type == ExpressionType.NUMBER or dominant_type == ExpressionType.FLOAT:
                return Symbol(self.line, self.column, op1.value - op2.value, dominant_type)
            print("Error: incorrect types to subtract.")
            ast.set_errors("Error: incorrect types to subtract.")

        if self.operator == "*":
            if dominant_type == ExpressionType.NUMBER or dominant_type == ExpressionType.FLOAT:
                return Symbol(self.line, self.column, op1.value * op2.value, dominant_type)
            print("Error: incorrect types to multiply.")
            ast.set_errors("Error: incorrect types to multiply.")

        if self.operator == "/":
            if op2.value == 0 or op2.value == 0.0:
                ast.set_errors("Error: Can not divided by 0.")
                return
            if dominant_type == ExpressionType.NUMBER or dominant_type == ExpressionType.FLOAT:
                return Symbol(self.line, self.column, op1.value / op2.value, dominant_type)
            print("Error: incorrect types to divide.")
            ast.set_errors("Error: incorrect types to divide.")

        if self.operator == "%":
            if dominant_type == ExpressionType.NUMBER:
                return Symbol(self.line, self.column, op1.value % op2.value, dominant_type)
            print("Error: incorrect types to modulo operation.")

        if self.operator == "==":
            return Symbol(self.line, self.column, op1.value == op2.value, ExpressionType.BOOLEAN)

        if self.operator == "!=":
            return Symbol(self.line, self.column, op1.value != op2.value, ExpressionType.BOOLEAN)

        if self.operator == ">":
            return Symbol(self.line, self.column, op1.value > op2.value, ExpressionType.BOOLEAN)

        if self.operator == "<":
            return Symbol(self.line, self.column, op1.value < op2.value, ExpressionType.BOOLEAN)

        if self.operator == ">=":
            return Symbol(self.line, self.column, op1.value >= op2.value, ExpressionType.BOOLEAN)

        if self.operator == "&&":
            if op1.type == ExpressionType.BOOLEAN and op2.type == ExpressionType.BOOLEAN:
                print("Boolean and")
                return Symbol(self.line, self.column, op1.value and op2.value, dominant_type)
            else:
                print(f"The types to compare should be 'boolean'")
                ast.set_errors(f"The types to compare should be 'boolean'")

        if self.operator == "||":
            if op1.type == ExpressionType.BOOLEAN and op2.type == ExpressionType.BOOLEAN:
                print("Boolean OR")
                return Symbol(self.line, self.column, op1.value or op2.value, ExpressionType.BOOLEAN)
            else:
                print(f"The types to compare should be 'boolean'")
                ast.set_errors(f"The types to compare should be 'boolean'")

        if self.operator == "!":
            if op1.type == ExpressionType.BOOLEAN:
                print("Boolean negate")
                return Symbol(self.line, self.column, not op1.value, ExpressionType.BOOLEAN)
            else:
                print(f"The type should be 'boolean'.")
                ast.set_errors(f"The types to compare should be 'boolean'")

        return Symbol(self.line, self.column, None, ExpressionType.NULL)

