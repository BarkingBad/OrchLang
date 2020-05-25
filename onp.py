import sys
import math
import ply.yacc as yacc
sys.path.insert(0, "../..")

tokens = (
    'NAME', 'NATURAL_NUMBER', 'REAL_NUMBER', 
    'sin', 'cos', 'exp', 'sqrt', 'log', 'power', 
    'EQ', 'NOTEQ', 'LT', 'GT', 'LTEQ', 'GTEQ',
)

literals = ['=', '+', '-', '*', '/', '(', ')']

# Tokens

t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

def t_REAL_NUMBER(t):
    r'[-+]?[0-9]+(\.([0-9]+)?([eE][-+]?[0-9]+)?|[eE][-+]?[0-9]+)'
    t.value = float(t.value)
    return t


def t_NATURAL_NUMBER(t):
    r'[-+]?\d+'
    t.value = int(t.value)
    return t

def t_sin(t):
    r'sin'
    return t

def t_cos(t):
    r'cos'
    return t

def t_exp(t):
    r'exp'
    return t

def t_sqrt(t):
    r'sqrt'
    return t

def t_log(t):
    r'log'
    return t

def t_power(t):
    r'\*\*'
    return t

t_ignore = " \t"

t_EQ = r'=='
t_NOTEQ = r'!='
t_LT = r'<'
t_GT = r'>'
t_LTEQ = r'<='
t_GTEQ = r'>='

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Parsing rules

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),
)

# dictionary of names
names = {}

def p_statement_assign(p):
    'statement : NAME "=" expression'
    names[p[1]] = p[3]


def p_statement_expr(p):
    'statement : expression'
    print(p[1])


def p_expression_binop(p):
    '''expression : expression expression '+' 
                  | expression expression '-' 
                  | expression expression '*' 
                  | expression expression '/' 
                  | expression expression EQ 
                  | expression expression NOTEQ 
                  | expression expression LTEQ 
                  | expression expression GTEQ 
                  | expression expression LT 
                  | expression expression GT 
                  | expression expression power '''
    if p[3] == '+':
        p[0] = p[1] + p[2]
    elif p[3] == '-':
        p[0] = p[1] - p[2]
    elif p[3] == '*':
        p[0] = p[1] * p[2]
    elif p[3] == '/':
        p[0] = p[1] / p[2]
    elif p[3] == "==":
        p[0] = 1 if p[1] == p[2] else 0
    elif p[3] == "!=":
        p[0] = 1 if p[1] != p[2] else 0
    elif p[3] == ">=":
        p[0] = 1 if p[1] >= p[2] else 0
    elif p[3] == "<=":
        p[0] = 1 if p[1] <= p[2] else 0
    elif p[3] == ">":
        p[0] = 1 if p[1] > p[2] else 0
    elif p[3] == "<":
        p[0] = 1 if p[1] < p[2] else 0
    elif p[3] == "**":
        p[0] = p[1] ** p[2]

def p_expression_unop(p):
    '''expression : expression sin 
                  | expression cos 
                  | expression exp 
                  | expression sqrt 
                  | expression log '''
    if p[2] == 'sin':
        p[0] = math.sin(p[1])
    elif p[2] == 'cos':
        p[0] = math.cos(p[1])
    elif p[2] == 'exp':
        p[0] = math.exp(p[1])
    elif p[2] == 'sqrt':
        p[0] = math.sqrt(p[1])
    elif p[2] == 'log':
        p[0] = math.log(p[1])

def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = -p[1]

def p_expression_number(p):
    '''expression : REAL_NUMBER
                  | NATURAL_NUMBER'''
    p[0] = p[1]

def p_expression_name(p):
    "expression : NAME"
    try:
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")


yacc.yacc()

def parseONP(input_str):
    return yacc.parse(input_str)
