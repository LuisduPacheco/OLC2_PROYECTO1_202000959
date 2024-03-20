from environment.ast import Ast
from interfaces.instruction import Instruction
from environment.environment import Environment


class InterfaceDeclaration(Instruction):
    def __init__(self, line, column, id_1, id_2, content):
        self.line = line
        self.column = column
        self.id_1 = id_1
        self.id_2 = id_2
        self.content = content

    def execute(self, ast: Ast, env: Environment):
        interface_value = env.get_struct(ast, self.id_2)

        if interface_value is None:
            return

        # Env for the new interface
        new_env = Environment(None, 'INTERFACE_' + self.id_1)

        for i in range(len(self.content)):
            # Save values of the interface
            id_param = list(interface_value[i].keys())[0]
            type_param = list(interface_value[i].values())[0]

            # Save expression values
            id_expression = list(self.content[i].keys())[0]
            value_expression = list(self.content[i].values())[0].execute(ast, env)

            if type_param == value_expression.type and id_param == id_expression:
                # A new variable is saved with the name of the interface.
                # as value an environment is saved with the saved variables
                new_env.save_variable(ast, id_param, value_expression)
            else:
                ast.set_errors("Type or ID of the interface is incorrect.")
                return None

            env.save_variable(ast, self.id_1, new_env)


















