from environment.ast import Ast
from interfaces.expression import Expression
from environment.symbol import Symbol
from environment.types import ExpressionType
from environment.environment import Environment
from environment.execute import statement_executor
from expressions.continue_statement import ContinueStatement


class Call(Expression):
    def __init__(self, line, column, identifier, params):
        self.line = line
        self.column = column
        self.identifier = identifier
        self.params = params

    def execute(self, ast: Ast, env: Environment):
        func = env.get_function(ast, self.identifier)
        if func == {}:
            return

        if len(self.params) != len(func['params']):
            ast.set_errors(f"The function was expected {len(func['params'])} params, but {len(self.params)} params "
                           f"were obtained.")
            return Symbol(self.line, self.column, None, ExpressionType.NULL)

        function_env = Environment(env.get_global_environment(), 'FUNCTION_'+self.identifier)

        if len(self.params) > 0:
            symbol_list = []
            for i in range(len(self.params)):
                sym_param = self.params[i].execute(ast, env)
                symbol_list.append(sym_param)

                # Save values of the function.
                id_param = list(func['params'][i].keys())[0]
                type_param = list(func['params'][i].values())[0]

                # Validate types
                if type_param != sym_param.type:
                    ast.set_errors('Parameter types are incorrect.')
                    return Symbol(self.line, self.column, None, ExpressionType.NULL)

                # Add to the environment
                function_env.save_variable(ast, id_param, sym_param)

        # Execute block
        return_value = statement_executor(func['block'], ast, function_env)
        if return_value is not None:
            if return_value.type != func['type']:
                ast.set_errors('Return type is incorrect.')
                return Symbol(self.line, self.column, None, ExpressionType.NULL)
            return return_value
        return None

























