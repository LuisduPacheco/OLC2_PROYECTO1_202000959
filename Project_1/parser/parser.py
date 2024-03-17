from expressions.Increase import Increase
from expressions.decrease import Decrease
from instructions.assignment import Assignment
from ply import lex as Lex
from ply import yacc as yacc


from expressions.access import Access
from expressions.primitive import Primitive
from expressions.operation import Operation
from expressions.array_access import ArrayAccess
from expressions.array import Array
from environment.types import ExpressionType

from instructions.print import Print
from instructions.declaration import Declaration
from instructions.declare_constants import Constants

class codeParams:
    def __init__(self, line, column):
        self.line = line
        self.column = column


# Lexico
reserved_words: dict[str, str] = {
    'console': 'CONSOLE',
    'log': 'LOG',
    'var': 'VAR',
    'const': 'CONST',
    'float': 'FLOAT',
    'number': 'NUMBER',
    'string': 'STRING',
    'char': 'CHAR',
    'boolean': 'BOOLEAN',
    'if': 'IF',
    'while': 'WHILE',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN'
}

tokens: list[str] = [
                        'ADD_ASSIGN',
                        'DOT',
                        'L_PAR',
                        'R_PAR',
                        'PLUS',
                        'MINUS',
                        'BY',
                        'DIVISION',
                        'COLON',
                        'SEMICOLON',
                        'COMMA',
                        'INT',
                        'DECIMAL',
                        'EQUAL',
                        'EQEQUAL',
                        'DIF',
                        'L_BRACKET',
                        'R_BRACKET',
                        'L_KEY',
                        'R_KEY',
                        'GREATER',
                        'LESS',
                        'GREATER_E',
                        'LESS_E',
                        'AND',
                        'OR',
                        'ID',
                        'MODULO',
                        'SUB_ASSIGN',
                        'NEGATE'
                    ] + list(reserved_words.values())

t_ADD_ASSIGN = r'[+][=]'
t_DOT = r'\.'
t_L_PAR = r'\('
t_R_PAR = r'\)'
t_PLUS = r'\+'
t_MINUS = r'-'
t_BY = r'\*'
t_DIVISION = r'/'
t_COLON = r':'
t_COMMA = r','
t_SEMICOLON = r';'
t_EQUAL = r'='
t_EQEQUAL = r'=='
t_DIF = r'!='
t_L_BRACKET = r'\['
t_R_BRACKET = r'\]'
t_L_KEY = r'\{'
t_R_KEY = r'\}'
t_GREATER = r'>'
t_LESS = r'<'
t_GREATER_E = r'>='
t_LESS_E = r'<='
t_AND = r'&&'
t_OR = r'\|\|'
t_MODULO = r'%'
t_SUB_ASSIGN = r'\-='
t_NEGATE = r'\!'

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


def t_CHAR(t):
    r"""\'(.)\'"""
    try:
        char_value = str(t.value)[1]  # Obtener el carácter entre comillas simples
        line = t.lexer.lexdata.rfind('\n', 0, t.lexpos) + 1
        column = t.lexpos - line
        t.value = Primitive(line, column, char_value.replace("'", ""), ExpressionType.CHAR)
    except ValueError:
        print(f"Error al convertir el carácter: {t.value}")
        t.value = Primitive(0, 0, None, ExpressionType.NULL)
    return t


def t_BOOLEAN(t):
    r"""(true|false)"""
    try:
        bool_value = eval(str(t.value).capitalize())  # Evaluar la cadena como un booleano
        line = t.lexer.lexdata.rfind('\n', 0, t.lexpos) + 1
        column = t.lexpos - line
        t.value = Primitive(line, column, bool_value, ExpressionType.BOOLEAN)
    except ValueError:
        print(f"Error al convertir el booleano: {t.value}")
        t.value = Primitive(0, 0, None, ExpressionType.NULL)
    return t


def t_NUMBER(t):
    r"""\d+(\.\d+)?"""
    try:
        if '.' in t.value:
            float_value = float(t.value)
            line: int = t.lexer.lexdata.rfind('\n', 0, t.lexpos) + 1
            column: int = t.lexpos - line
            t.value = Primitive(line, column, float_value, ExpressionType.FLOAT)
        else:
            int_value: int = int(t.value)
            line: int = t.lexer.lexdata.rfind('\n', 0, t.lexpos) + 1
            column: int = t.lexpos - line
            t.value = Primitive(line, column, int_value, ExpressionType.NUMBER)
    except ValueError:
        print(f"Error to convert number: {t.value}")
        t.value = Primitive(0, 0, None, ExpressionType.NULL)
    return t


def t_FLOAT(t):
    r"""\d+\.\d+"""
    try:
        float_value = float(t.value)
        line: int = t.lexer.lexdata.rfind('\n', 0, t.lexpos) + 1
        column: int = t.lexpos - line
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
    ('left', 'GREATER', 'LESS'),
    ('left', 'GREATER_E', 'LESS_E'),
    ('left', 'AND'),
    ('left', 'OR'),
    ('left', 'ADD_ASSIGN', 'SUB_ASSIGN')
)


#START
def p_start(t):
    """s : block"""
    t[0] = t[1]


def p_instruction_block(t):
    """block : block instruction
            | instruction"""
    if len(t) > 2:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]


def p_instruction_list(t):
    """instruction : print
                | declaration
                | assignment"""
    t[0] = t[1]


def p_instruction_console(t):
    """print : CONSOLE DOT LOG L_PAR expressionList R_PAR SEMICOLON"""
    params = get_params(t)
    t[0] = Print(params.line, params.column, t[5])


def p_instruction_declaration(t):
    """declaration : VAR ID COLON type EQUAL expression SEMICOLON
                    | VAR ID EQUAL expression SEMICOLON
                    """
    if len(t) == 8:
        params = get_params(t)
        t[0] = Declaration(params.line, params.column, t[2], t[4], t[6])
    elif len(t) == 6:
        params = get_params(t)
        t[0] = Declaration(params.line, params.column, t[2], None, t[4])


def p_instruction_declaration_type(t):
    """declaration : VAR ID COLON type SEMICOLON"""
    params = get_params(t)
    t[0] = Declaration(params.line, params.column, t[2], t[4], None)


def p_instruction_declare_constants(t):
    """declaration : CONST ID COLON type EQUAL expression SEMICOLON
                    | CONST ID EQUAL expression SEMICOLON
                    """
    if len(t) == 8:
        params = get_params(t)
        t[0] = Constants(params.line, params.column, t[2], t[4], t[6])
    elif len(t) == 6:
        params = get_params(t)
        t[0] = Constants(params.line, params.column, t[2], None, t[4])


def p_instruction_assignment(t):
    """assignment : ID EQUAL expression SEMICOLON
                | ID ADD_ASSIGN expression SEMICOLON
                | ID SUB_ASSIGN expression SEMICOLON"""
    params = get_params(t)
    if t[2] == "=":
        t[0] = Assignment(params.line, params.column, t[1], t[3])
    elif t[2] == "+=":
        t[0] = Increase(params.line, params.column, t[1], t[3])
    elif t[2] == "-=":
        t[0] = Decrease(params.line, params.column, t[1], t[3])

def p_type_production(t):
    """type : NUMBER
            | FLOAT
            | STRING
            | BOOLEAN
            | CHAR"""
    if t[1] == 'number':
        t[0] = ExpressionType.NUMBER
    if t[1] == 'float':
        t[0] = ExpressionType.FLOAT
    if t[1] == 'string':
        t[0] = ExpressionType.STRING
    if t[1] == 'bool':
        t[0] = ExpressionType.BOOLEAN
    if t[1] == 'char':
        t[0] = ExpressionType.CHAR

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


def p_expression_mod(t):
    """expression : expression MODULO expression"""
    params = get_params(t)
    t[0] = Operation(params.line, params.column, "%", t[1], t[3])


def p_expression_equal(t):
    """expression : expression EQEQUAL expression"""
    params = get_params(t)
    t[0] = Operation(params.line, params.column, "==", t[1], t[3])


def p_expression_different(t):
    """expression : expression DIF expression"""
    params = get_params(t)
    t[0] = Operation(params.line, params.column, "!=", t[1], t[3])


def p_expression_different(t):
    """expression : expression DIF expression"""
    params = get_params(t)
    t[0] = Operation(params.line, params.column, "!=", t[1], t[3])


def p_expression_greater(t):
    """expression : expression GREATER expression"""
    params = get_params(t)
    t[0] = Operation(params.line, params.column, ">", t[1], t[3])


def p_expression_greater_equal(t):
    """expression : expression GREATER_E expression"""
    params = get_params(t)
    t[0] = Operation(params.line, params.column, ">=", t[1], t[3])


def p_expression_less(t):
    """expression : expression LESS expression"""
    params = get_params(t)
    t[0] = Operation(params.line, params.column, "<", t[1], t[3])


def p_expression_less_equal(t):
    """expression : expression LESS_E expression"""
    params = get_params(t)
    t[0] = Operation(params.line, params.column, "<=", t[1], t[3])


def p_expression_and(t):
    """expression : expression AND expression"""
    params = get_params(t)
    t[0] = Operation(params.line, params.column, "&&", t[1], t[3])


def p_expression_or(t):
    """expression : expression OR expression"""
    params = get_params(t)
    t[0] = Operation(params.line, params.column, "||", t[1], t[3])


def p_expression_negate(t):
    """expression : NEGATE expression"""
    params = get_params(t)
    t[0] = Operation(params.line, params.column, "!", t[2], None)


def p_expression_group(t):
    """expression : L_PAR expression R_PAR"""
    t[0] = t[2]


def p_expression_primitive(t):
    """expression : NUMBER
                | STRING
                | FLOAT
                | CHAR
                | BOOLEAN
                | listArray"""
    t[0] = t[1]


def p_expression_array_primitive(t):
    """expression : L_BRACKET expressionList R_BRACKET"""
    params = get_params(t)
    t[0] = Array(params.line, params.column, t[2])


def p_expression_list_array(t):
    """listArray : listArray L_BRACKET expression R_BRACKET
                | listArray DOT ID
                | ID"""
    params = get_params(t)
    if len(t) > 4:
        t[0] = ArrayAccess(params.line, params.column, t[1], t[3])
    elif len(t) > 3:
        print("ToDo: Interface Access")
    else:
        t[0] = Access(params.line, params.column, t[1])


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


