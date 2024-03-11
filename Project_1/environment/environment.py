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

    def save_variable(self, ast, identifier, symbol) -> None:
        if identifier in self.table:
            ast.set_errors(f'The variable "{identifier}" already exists.')
            return
        self.table[identifier] = symbol

    def get_variable(self, ast, identifier) -> Symbol:
        temporal_env: Environment = self
        while True:
            if identifier in self.table:
                return self.table[identifier]
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

