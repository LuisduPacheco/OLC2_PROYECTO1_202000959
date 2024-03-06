from ply import lex as Lex
from ply import yacc as yacc


from expressions.access import Acces
from expressions.primitive import Primitive
from expressions.operation import Operation
from environment.types import ExpressionType
from instructions.print import Print
from instructions.declaration import Declaration


class codeParams:
    def __init__(self, line, column):
        self.line = line
        self.column = column


# Lexico
reserved_words: dict[str, str] = {
    'console': 'CONSOLE',
    'log': 'LOG',
    'var': 'VAR',
    'float': 'FLOAT',
    'number': 'NUMBER',
    'string': 'STRING',
    'bool': 'BOOL'
}

tokens: list[str] = [
                        'L_PAR',
                        'R_PAR',
                        'PLUS',
                        'MINUS',
                        'BY',
                        'DIVISION',
                        'DOT',
                        'COLON',
                        'SEMICOLON',
                        'COMMA',
                        'INT',
                        'DECIMAL',
                        'EQUAL',
                        'ID',
                        'L_BRACKET',
                        'R_BRACKET',
                    ] + list(reserved_words.values())

t_L_PAR = r'\('
t_R_PAR = r'\)'
t_PLUS = r'\+'
t_MINUS = r'-'
t_BY = r'\*'
t_DIVISION = r'/'
t_DOT = r'\.'
t_COLON = r':'
t_COMMA = r','
t_SEMICOLON = r';'
t_EQUAL = r'='
t_L_BRACKET = r'\['
t_R_BRACKET = r'\]'


def t_STRING(t):
    r"""\"(.+?)\""""
    try:
        str_value: str = str(t.value)
        line = t.lexer.lexdata.rfind('\n', 0, t.lexpos) + 1
        column = t.lexpos - line
        t.value = Primitive(line, column, str_value.replace('"', ''), ExpressionType.STRING)
    except ValueError:
        print(f"Error to convert string: {t.value}")
        t.value = Primitive(0, 0, None, ExpressionType.NULL)
    return t


def t_NUMBER(t):
    r"""\d+"""
    try:
        int_value: int = int(t.value)
        line = t.lexer.lexdata.rfind('\n', 0, t.lexpos) + 1
        column = t.lexpos - line
        t.value = Primitive(line, column, int_value, ExpressionType.NUMBER)
    except ValueError:
        print(f"Error to convert int: {t.value}")
        t.value = Primitive(0, 0, None, ExpressionType.NULL)
    return t


def t_FLOAT(t):
    r"""\d+\.\d+"""
    try:
        float_value: float = float(t.value)
        line = t.lexer.lexdata.rfind('\n', 0, t.lexpos) + 1
        column = t.lexpos - line
        t.value = Primitive(line, column, float_value, ExpressionType.FLOAT)
    except ValueError:
        print(f"Error to convert float: {t.value}")
        t.value = Primitive(0, 0, None, ExpressionType.NULL)
    return t


def t_ID(t):
    r"""[a-zA-Z_][a-zA-Z_0-9]*"""
    t.type = reserved_words.get(t.value.lower(), 'ID')
    return t


t_ignore = " \t"
t_ignore_COMMENTLINE = r'\/\/.*'


def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += t.value.count("\n")


def t_ignore_COMMENTBLOCK(t):
    r"""\/\*[^*]*\*+(?:[^/*][^*]*\*+)*\/"""
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Error Lex '%s'" % t.value[0])
    t.lexer.skip(1)


# SYNTACTIC
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'BY', 'DIVISION'),
)


#START
def p_instructions_list(t):
    """instructions : instructions instruction
                    | instruction"""
    if 2 < len(t):
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]


def p_instruction_console(t):
    """instruction : CONSOLE DOT LOG L_PAR expressionList R_PAR SEMICOLON"""
    params = get_params(t)
    t[0] = Print(params.line, params.column, t[5])


def p_instruction_declaration(t):
    """instruction : VAR ID COLON type EQUAL expression SEMICOLON"""
    params = get_params(t)
    t[0] = Declaration(params.line, params.column, t[2], t[4], t[6])


def p_type_production(t):
    """type : NUMBER
            | FLOAT
            | STRING
            | BOOL"""
    if t[1] == 'number':
        t[0] = ExpressionType.NUMBER
    if t[1] == 'float':
        t[0] = ExpressionType.FLOAT
    if t[1] == 'string':
        t[0] = ExpressionType.STRING
    if t[1] == 'bool':
        t[0] = ExpressionType.BOOLEAN

    print(f"-----------------------")
    print(t[1])


# Expressions
def p_expression_list(t):
    """expressionList : expressionList COMMA expression
                    | expression"""
    exp_list = []
    if len(t) > 2:
        exp_list = t[1] + [t[3]]
    else:
        exp_list.append(t[1])
    t[0] = exp_list


def p_expression_add(t):
    """expression : expression PLUS expression"""
    params = get_params(t)
    t[0] = Operation(params.line, params.column, "+", t[1], t[3])


def p_expression_sub(t):
    """expression : expression MINUS expression"""
    params = get_params(t)
    t[0] = Operation(params.line, params.column, "-", t[1], t[3])


def p_expression_mult(t):
    """expression : expression BY expression"""
    params = get_params(t)
    t[0] = Operation(params.line, params.column, "*", t[1], t[3])


def p_expression_div(t):
    """expression : expression DIVISION expression"""
    params = get_params(t)
    t[0] = Operation(params.line, params.column, "/", t[1], t[3])


def p_expression_group(t):
    """expression : L_PAR expression R_PAR"""
    t[0] = t[2]


def p_expression_primitive(t):
    """expression : NUMBER
                | STRING
                | listArray"""
    t[0] = t[1]


def p_expression_list_array(t):
    """listArray : listArray DOT ID
                | listArray listAccessArray
                | ID"""
    params = get_params(t)
    if len(t) > 3:
        print("ToDo: ArrayAccess")
    elif len(t) > 2:
        print("ToDo: ArrayAccess")
    else:
        t[0] = Acces(params.line, params.column, t[1])


def p_expression_list_access_array(t):
    """listAccessArray : listAccessArray L_BRACKET expression R_BRACKET
                    | L_BRACKET expression R_BRACKET"""
    t[0] = t[1]


def p_error(p):
    if p:
        print(f"Syntax error, line: {p.lineno}, column: {p.lexpos}\nt expected: '{p.value}'")
    else:
        print("Syntax Error.")

def get_params(t):
    line = t.lexer.lineno
    lex_pos = t.lexpos if isinstance(t.lexpos, int) else 0
    column = lex_pos - t.lexer.lexdata.rfind('\n', 0, lex_pos)
    return codeParams(line, column)


class Parser:
    def __init__(self):
        pass

    def interpreter(self, entry):
        lexer = Lex.lex()
        parser = yacc.yacc()
        result = parser.parse(entry)
        return result


