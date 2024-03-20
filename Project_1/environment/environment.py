from environment.types import ExpressionType
from environment.symbol import Symbol


class Environment:
    def __init__(self, previous, identifier):
        self.previous = previous
        self.identifier = identifier
        self.table: dict = {}
        self.constants: dict = {}
        self.interfaces: dict = {}
        self.functions: dict = {}

    def save_constant(self, ast, identifier, symbol):
        if identifier in self.constants:
            ast.set_errors(f'The constant "{identifier}" already exists.')
            return
        self.constants[identifier] = symbol

    def get_constant(self, ast, identifier):
        temporal_env: Environment = self
        while True:
            if identifier in self.constants:
                return self.constants[identifier]
            if temporal_env.previous is None:
                break
            else:
                temporal_env = temporal_env.previous
        ast.set_errors(f'The variable "{identifier}" does not exist.')
        return Symbol(0, 0, None, ExpressionType.NULL)

    def save_variable(self, ast, identifier, symbol):
        if identifier in self.table:
            ast.set_errors(f'The variable "{identifier}" already exists.')
            return
        self.table[identifier] = symbol

    def get_variable(self, ast, identifier) -> Symbol:
        temporal_env = self
        while True:
            if identifier in temporal_env.table:
                return temporal_env.table[identifier]
            if temporal_env.previous is None:
                break
            else:
                temporal_env = temporal_env.previous
        ast.set_errors(f'The variable "{identifier}" does not exist.')
        return Symbol(0, 0, None, ExpressionType.NULL)

    def set_variable(self, ast, identifier, symbol_var):
        temp_env = self
        while True:
            if identifier in temp_env.table:
                temp_env.table[identifier] = symbol_var
                return symbol_var
            if temp_env.previous is None:
                break
            else:
                temp_env = temp_env.previous

        ast.set_errors(f"The variable {identifier} doesn't exist.")
        return Symbol(0,0, None, ExpressionType.NULL)

    def increase_variable(self, ast, identifier, symbol_var):
        variable = self.get_variable(ast, identifier)
        variable.value = variable.value + symbol_var.value
        print(variable.value)
        return variable

    def decrease_variable(self, ast, identifier, symbol_var):
        Variable = self.get_variable(ast, identifier)
        if symbol_var.type == ExpressionType.NUMBER or symbol_var.type == ExpressionType.FLOAT:
            if Variable.type == ExpressionType.NULL:
                Variable.type = symbol_var.type
                Variable.value = Variable.value - symbol_var.value
            else:
                Variable.value = Variable.value - symbol_var.value
            print(Variable.value)
            return Variable

    def save_function(self, ast, identifier, function):
        if identifier in self.functions:
            ast.setErrors(f"There is already a function with the name {identifier}")
            return
        self.functions[identifier] = function

    def get_function(self, ast, identifier):
        tmp_env = self
        while True:
            if identifier in tmp_env.functions:
                return tmp_env.functions[identifier]
            if tmp_env.previous is None:
                break
            else:
                tmp_env = tmp_env.previous
        ast.setErrors(f"The function {identifier} does not exist.")
        return {}

    def save_struct(self, ast, identifier, struct):
        if identifier in self.interfaces:
            ast.setErrors(f"There is already a interface with the name {identifier}")
            return
        self.interfaces[identifier] = struct

    def get_struct(self, ast, identifier):
        tmp_env = self
        while True:
            if identifier in tmp_env.interfaces:
                return tmp_env.interfaces[identifier]
            if tmp_env.previous is None:
                break
            else:
                tmp_env = tmp_env.previous
        ast.setErrors(f"The interface {identifier} does not exist.")
        return None

    def loop_validation(self):
        temp_env = self
        while True:
            if temp_env.identifier == "WHILE" or temp_env.identifier == "FOR":
                return True
            if temp_env.previous is None:
                break
            else:
                temp_env = temp_env.previous
        return False

    def FunctionValidation(self):
        temp_env = self
        while True:
            if 'FUNCTION_' in temp_env.identifier:
                return True
            if temp_env.previous is None:
                break
            else:
                temp_env = temp_env.previous
        return False

    def get_global_environment(self):
        tmp_env = self
        while True:
            if tmp_env.previous is None:
                return tmp_env
            else:
                tmp_env = tmp_env.previous
