import sys
import math
import ply.lex as lex

sys.path.insert(0, "../..")

reserved = {
    'if': 'IF',
    'while': 'WHILE',
    'for': 'FOR',
    'define': 'DEFINE',
    'int': 'INT',
    'float': 'FLOAT',
    'boolean': 'BOOLEAN',
    'string': 'STRING'
}

tokens = [
             'NAME', 'NATURAL_NUMBER', 'REAL_NUMBER', 'BOOL', 'STR',
             'sin', 'cos', 'exp', 'sqrt', 'log', 'power', 'intToFloat', 'floatToInt',
             'EQ', 'NOTEQ', 'LT', 'GT', 'LTEQ', 'GTEQ',
         ] + list(reserved.values())

literals = ['=', '+', '-', '*', '/', '(', ')', ',']

# Tokens

t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'


def t_REAL_NUMBER(t):
    r'[-+]?[0-9]+(\.([0-9]+)?([eE][-+]?[0-9]+)?|[eE][-+]?[0-9]+)'
    t.value = float(t.value)
    return t


def t_NATURAL_NUMBER(t):
    r'[-]?\d+'
    t.value = int(t.value)
    return t

def t_BOOL(t):
    r'(True|False)'
    return t

def t_STR(t):
    r'"([^"\n]|(\\"))*"'
    return t

def t_sin(t):
    r'sin(?=[0-9() ])'
    return t

def t_cos(t):
    r'cos(?=[0-9() ])'
    return t

def t_exp(t):
    r'exp(?=[0-9() ])'
    return t

def t_sqrt(t):
    r'sqrt(?=[0-9() ])'
    return t

def t_log(t):
    r'log(?=[0-9() ])'
    return t

def t_power(t):
    r'\*\*'
    return t

def t_intToFloat(t):
    r'intToFloat(?=[0-9() ])'
    return t

def t_floatToInt(t):
    r'floatToInt(?=[0-9() ])'
    return t

t_ignore = " \t"

t_EQ = r'=='
t_NOTEQ = r'!='
t_LT = r'<'
t_GT = r'>'
t_LTEQ = r'<='
t_GTEQ = r'>='


def t_IF(t):
    r'if'
    return t


def t_WHILE(t):
    r'while'
    return t


def t_FOR(t):
    r'for'
    return t

def t_DEFINE(t):
    r'define'
    return t

def t_INT(t):
    r'int'
    return t

def t_FLOAT(t):
    r'float'
    return t

def t_BOOLEAN(t):
    r'boolean'
    return t

def t_STRING(t):
    r'string'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)



# Build the lexer

lexer = lex.lex()

# Parsing rules

precedence = (
    ('left', '+', '-', 'sin', 'cos', 'log', 'exp', 'sqrt', 'intToFloat', 'floatToInt'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),
)

# dictionary of names
globals = {}
functions = {}

def names(local, name):
    return local[name](local) if name in local.keys() else globals[name]

def p_start(p):
    """start : if_statement
             | for_statement
             | while_statement
             | define
             | statement"""
    p[0] = p[1]
    res = p[0]({}) if p[0] is not None else None
    if p[0] is not None and res is not None:
        print(res)


def p_for_statement(p):
    "for_statement : FOR '(' statement ',' expression ',' statement ')' statement"
    cond = p[5]
    initial = p[3]
    update = p[7]
    action = p[9]

    def loop(local):
        initial(local)
        if cond({})[0] != 'boolean':
            return "Error on if condition, boolean required"
        while cond(local)[1]:
            print(action(local))
            update(local)


    p[0] = loop


def p_if_statement(p):
    "if_statement : IF '(' expression ')' statement"
    res = p[3]({})
    if res[0] != 'boolean':
        p[0] = "Error on if condition, boolean required"
    elif res[1]:
        p[0] = p[5]


def p_while_statement(p):
    """while_statement : WHILE '(' expression ')' statement"""
    cond = p[3]
    statement = p[5]

    def res(local):
        if cond({})[0] != 'boolean':
            return "Error on if condition, boolean required"
        while cond(local)[1] if callable(cond) else cond:
            print(statement(local))

    p[0] = res

def p_define(p):
    """define : DEFINE NAME '(' params ')' '=' statement"""
    fun_name = p[2]
    params = p[4]
    statement = p[7]
    def apply(args, local):
        m = dict(zip(params, args))
        return statement(dict(m, **local))
    functions[fun_name] = apply
    print(functions)

def p_statement_assign(p):
    """statement : INT NAME "=" statement
                 | FLOAT NAME "=" statement
                 | BOOLEAN NAME "=" statement
                 | STRING NAME "=" statement """
    typ = p[1]
    name = p[2]
    expr = p[4]


    def assign(local):
        if name not in globals:
            if (typ == expr(local)[0]):
                globals[name] = expr(local)
                return globals[name]  
            else:
                return "Incompatible types!"
        else:
            return "Name already exists!"

    p[0] = assign 

def p_statement_reassign(p):
    """statement : NAME "=" statement"""
    name = p[1]
    expr = p[3]


    def reassign(local):
        if name in globals:
            if (globals[name][0] == expr(local)[0]):
                globals[name] = expr(local)
                return globals[name]  
            else:
                return "Incompatible types!"
        else:
            return "Name doesn't exist!"

    p[0] = reassign 


def p_params(p):
    """params : NAME
              | NAME ',' params"""
    if(len(p) > 3):
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_call_function(p):
    """statement : NAME '(' statements ')' """
    func = functions[p[1]]
    params = p[3]
    p[0] = lambda local: func(params, local)

def p_statements(p):
    """statements : statement
                  | statement ',' statements"""
    if(len(p) > 3):
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]


def p_statement_expr(p):
    'statement : expression'
    expr = p[1]
    p[0] = lambda local: expr(local)


def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | expression EQ expression
                  | expression NOTEQ expression
                  | expression LTEQ expression
                  | expression GTEQ expression
                  | expression LT expression
                  | expression GT expression
                  | expression power expression'''
    expr1 = p[1]
    op = p[2]
    expr2 = p[3]
    if op == '+':
        p[0] = lambda local: (expr1(local)[0], expr1(local)[1] + expr2(local)[1]) if expr1(local)[0] == expr2(local)[0] else 'Error, incomatbile types'
    elif op == '-':
        p[0] = lambda local: (expr1(local)[0], expr1(local)[1] - expr2(local)[1]) if expr1(local)[0] == expr2(local)[0] else 'Error, incomatbile types' 
    elif op == '*':
        p[0] = lambda local: (expr1(local)[0], expr1(local)[1] * expr2(local)[1]) if expr1(local)[0] == expr2(local)[0] else 'Error, incomatbile types'
    elif op == '/':
        p[0] = lambda local: (expr1(local)[0], expr1(local)[1] / expr2(local)[1]) if expr1(local)[0] == expr2(local)[0] else 'Error, incomatbile types'
    elif op == "==":
        p[0] = lambda local: ('boolean', True if expr1(local)[1] == expr2(local)[1] else False) if expr1(local)[0] == expr2(local)[0] else 'Error, incomatbile types'
    elif op == "!=":
        p[0] = lambda local: ('boolean', True if expr1(local)[1] != expr2(local)[1] else False) if expr1(local)[0] == expr2(local)[0] else 'Error, incomatbile types'
    elif op == ">=":
        p[0] = lambda local: ('boolean', True if expr1(local)[1] >= expr2(local)[1] else False) if expr1(local)[0] == expr2(local)[0] else 'Error, incomatbile types'
    elif op == "<=":
        p[0] = lambda local: ('boolean', True if expr1(local)[1] <= expr2(local)[1] else False) if expr1(local)[0] == expr2(local)[0] else 'Error, incomatbile types'
    elif op == ">":
        p[0] = lambda local: ('boolean', True if expr1(local)[1] > expr2(local)[1] else False) if expr1(local)[0] == expr2(local)[0] else 'Error, incomatbile types'
    elif op == "<":
        p[0] = lambda local: ('boolean', True if expr1(local)[1] < expr2(local)[1] else False) if expr1(local)[0] == expr2(local)[0] else 'Error, incomatbile types'
    elif op == "**":
        p[0] = lambda local: (str(type(expr1(local)[1] ** expr2(local)[1]))[8:-2], expr1(local)[1] ** expr2(local)[1])


def p_expression_unop(p):
    '''expression : sin expression
                  | cos expression
                  | exp expression
                  | sqrt expression
                  | log expression
                  | intToFloat expression
                  | floatToInt expression'''
    op = p[1]
    expr = p[2]
    if op == 'sin':
        p[0] = lambda local: ('float', math.sin(expr(local)[1]))
    elif op == 'cos':
        p[0] = lambda local: ('float', math.cos(expr(local)[1]))
    elif op == 'exp':
        p[0] = lambda local: ('float', math.exp(expr(local)[1]))
    elif op == 'sqrt':
        p[0] = lambda local: ('float', math.sqrt(expr(local)[1]))
    elif op == 'log':
        p[0] = lambda local: ('float', math.log(expr(local)[1]))
    elif op == 'intToFloat':
        p[0] = lambda local: ('float', float(expr(local)[1])) if expr(local)[0] == 'int' else "Error, int required"
    elif op == 'floatToInt':
        p[0] = lambda local: ('int', int(expr(local)[1])) if expr(local)[0] == 'float' else "Error, float required"


def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    uminus = -p[2]
    p[0] = lambda local: uminus(local)


def p_expression_group(p):
    "expression : '(' expression ')'"
    group = p[2]
    p[0] = lambda local: group(local)


def p_expression_number(p):
    '''expression : REAL_NUMBER
                  | NATURAL_NUMBER
                  | BOOL
                  | STR'''
    number = p[1]
    if (isinstance(number, int)):
        p[0] = lambda local: ('int', number)
    elif (isinstance(number, float)):
        p[0] = lambda local: ('float', number)
    elif (number == "True"):
        p[0] = lambda local: ('boolean', True)
    elif (number == "False"):
        p[0] = lambda local: ('boolean', False)
    else:
        p[0] = lambda local: ('string', number[1:-1])

def p_expression_name(p):
    """expression : NAME"""
    name = p[1]
    def do_nothing(local):
        print("Undefined name '%s'" % name)
        pass
    def parseName(local):
        try:
            if name in list(globals.keys()) + list(local.keys()):
                return names(local, name)
            else:
                return do_nothing(local)
        except LookupError:
            return do_nothing(local)
    p[0] = parseName

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")


import ply.yacc as yacc

parser = yacc.yacc()

def parse(input_str):
    return yacc.parse(input_str)