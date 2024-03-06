from environment.types import ExpressionType
from environment.symbol import Symbol


class Environment:
    def __init__(self, previous, identifier):
        self.previous = previous
        self.identifier = identifier
        self.table: dict = {}
        self.interfaces: dict = {}
        self.functions: dict = {}

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


