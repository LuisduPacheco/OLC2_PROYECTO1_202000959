from abc import ABC, abstractmethod
from environment.environment import Environment
from environment.ast import Ast


class Instruction(ABC):

    @abstractmethod
    def execute(self, ast: Ast, env: Environment):
        pass
