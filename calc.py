import sys
import math
import ply.lex as lex
import copy
import ast 

sys.path.insert(0, "../..")

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'define': 'DEFINE',
    'int': 'INT',
    'float': 'FLOAT',
    'boolean': 'BOOLEAN',
    'string': 'STRING',
    'begin': 'BEGIN',
    'end': 'END'
}

tokens = [
            'NAME', 'NATURAL_NUMBER', 'REAL_NUMBER', 'BOOL', 'STR',
            'sin', 'cos', 'exp', 'sqrt', 'log', 'power', 'intToFloat', 'floatToInt',
            'EQ', 'NOTEQ', 'LT', 'GT', 'LTEQ', 'GTEQ', 'print'
         ] + list(reserved.values())

literals = ['=', '+', '-', '*', '/', '(', ')', ';', ',']

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

def t_print(t):
    r'print(?=[0-9() ])'
    return t

t_ignore = " \t"

t_EQ = r'=='
t_NOTEQ = r'!='
t_LT = r'<'
t_GT = r'>'
t_LTEQ = r'<='
t_GTEQ = r'>='


def t_BEGIN(t):
    r'begin'
    return t


def t_END(t):
    r'end'
    return t


def t_IF(t):
    r'if'
    return t


def t_ELSE(t):
    r'else'
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
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('left', 'sin', 'cos', 'log', 'exp', 'sqrt', 'intToFloat', 'floatToInt', 'print'),
    ('right', 'power'),
    ('right', 'UMINUS'),
)
# dictionary of names
functions = {}
expressions = {}
used_names = []

def names(local, name):
    return local[name] # if name in local.keys() else globals[name]

def p_start(p):
    """start : block"""

    def evaluate_blocks(blocks, locals):
        evaluate_block(blocks.block, locals)
        if blocks.has_blocks():
            evaluate_blocks(blocks.blocks, locals)

    def evaluate_block(block, locals):
        if block.has_casual_statement():
            block.casual_statement.operation.fun(locals)
        else:
            new_locals = dict.copy(locals)
            evaluate_blocks(block.blocks, new_locals)
        
    evaluate_block(p[1], {}) 
    
    p[0] = ast.P_start(p[1])
    return p[0]


def p_block(p):
    """block : BEGIN blocks END
             | casual_statement"""
    if len(p) == 2:
        p[0] = ast.P_block(None, p[1])
    else:
        p[0] = ast.P_block(p[2], None)


def p_blocks(p):
    """blocks : block
              | block blocks"""
    if len(p) == 2:
        p[0] = ast.P_blocks(p[1], None)
    else:
        p[0] = ast.P_blocks(p[1], p[2])


def p_casual_statements(p):
    """casual_statement : if_statement ';'
                        | for_statement ';'
                        | while_statement ';'
                        | define ';'
                        | statement ';'"""
    p[0] = ast.P_casual_statements(p[1])


def p_for_statement(p):
    "for_statement : FOR '(' statement ';' expression ';' statement ')' statement"

    initialPr = p[3]
    initial = initialPr.fun

    condPr = p[5]
    cond = condPr.fun

    updatePr = p[7]
    update = updatePr.fun

    actionPr = p[9]
    action = actionPr.fun

    def loop(local):
        initial(local)
        while cond(local)[1]:
            # print(action(local))
            action(local)
            update(local)

    p[0] = ast.P_for_statement(lambda local: loop(local) if loop(local) else ast.P_empty().fun(local), initialPr, condPr, updatePr, actionPr)


def p_if_statement(p):
    "if_statement : IF '(' expression ')' statement ELSE statement"
    resPr = p[3]
    res = resPr.fun
    statementPr = p[5]
    statement = statementPr.fun
    statement2Pr = p[7]
    statement2 = statement2Pr.fun
    p[0] = ast.P_if_statement(lambda local: statement(local) if res(local) == ('boolean', True) else statement2(local), resPr, statementPr, statement2Pr)


def p_while_statement(p):
    """while_statement : WHILE '(' expression ')' statement"""
    condPr = p[3]
    cond = condPr.fun
    statementPr = p[5]
    statement = statementPr.fun

    def res(local):
        while cond(local)[1] if callable(cond) else cond:
            # print(statement(local))
            statement(local)

    p[0] = ast.P_while_statement(lambda local: res(local) if res(local) else ast.P_empty().fun(local), condPr, statementPr)


def p_define(p):
    """define : DEFINE NAME '(' params ')' '=' statement
              | DEFINE NAME '(' params ')' '=' if_statement"""
    fun_name = p[2]
    params = p[4]
    statementPr = p[7]
    statement = statementPr.fun

    def apply(args, local):
        def compatible_types(params, args):
            if(params is None and args is None):
                return True
            elif(params is not None and params is not None):                
                return (params.typeo == args.statement.fun(local)[0]) and compatible_types(params.params, args.statements)
            else:
                return False

        if(not compatible_types(params, args)):
            print("Error")
        else:
            def zzip(params, args):
                return [(params.name, args.statement.fun(local))] + (zzip(params.params, args.statements) if params.params is not None else [])
            m = dict(zzip(params, args))
            return statement(dict(local, **m))

    functions[fun_name] = apply
    p[0] = ast.P_define(ast.P_empty().fun, fun_name, params, statementPr)


def p_statement_assign(p):
    """statement : INT NAME "=" statement
                 | FLOAT NAME "=" statement
                 | BOOLEAN NAME "=" statement
                 | STRING NAME "=" statement
                 | INT NAME "=" if_statement
                 | FLOAT NAME "=" if_statement
                 | BOOLEAN NAME "=" if_statement
                 | STRING NAME "=" if_statement """
    typ = p[1]
    name = p[2]
    exprPr = p[4]
    expr = exprPr.fun
    

    def assign(local):
        if (typ == expr(local)[0]):
            if name in used_names:
                local[name] = expr(local)
                return local[name]  
            else:
                return None
        else:
            return "Incompatible types!"

    p[0] = ast.P_statement_assign(assign, typ, name, exprPr) 


def p_statement_reassign(p):
    """statement : NAME "=" statement"""
    name = p[1]
    exprPr = p[3]
    expr = exprPr.fun

    used_names.append(name)

    def reassign(local):
        if local[name][0] == expr(local)[0]:
            local[name] = expr(local)
            return local[name]  
        else:
            return "Incompatible types!"


    p[0] = ast.P_statement_reassign(reassign, name, exprPr) 


def p_params(p):
    """params : INT NAME
              | FLOAT NAME
              | BOOLEAN NAME
              | STRING NAME
              | INT NAME ',' params
              | FLOAT NAME ',' params
              | BOOLEAN NAME ',' params
              | STRING NAME ',' params"""
    
    if(len(p) > 3):
        p[0] = ast.P_params(p[1], p[2], p[4])
    else:
        p[0] = ast.P_params(p[1], p[2], None)


def p_call_function(p):
    """expression : NAME '(' statements ')' """
    
    def funForName(name):
        return functions[name]
    
    name = p[1]
    params = p[3]
    p[0] = ast.P_call_function(lambda local: funForName(name)(params, local), p[1], params)


def p_statements(p):
    """statements : statement
                  | statement ',' statements"""
    if(len(p) > 3):
        p[0] = ast.P_statements(p[1], p[3])
    else:
        p[0] = ast.P_statements(p[1], None)


def p_statement_expr(p):
    'statement : expression'
    expr = p[1]

    def evaluate(expr, local):
        if repr(expr) in expressions:
            result = expressions[repr(expr)]
            return expr.fun 
        else:
            expressions[repr(expr)] = expr.fun(local)
            return expr.fun 

    p[0] = ast.P_statement_expr(lambda local: evaluate(expr, local)(local), expr)


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
    expr1 = p[1].fun
    expr1pr = p[1]
    op = p[2]
    expr2 = p[3].fun
    expr2pr = p[3]

    def typef(s1, s2):
        x = {
            'boolean': 1,
            'int': 2,
            'float': 3,
            'string': 4
        }
        return list(x.keys())[max(x[s1], x[s2])-1]

    if op == '+':
        p[0] = ast.P_expression_binop(lambda local: (typef(expr1(local)[0], expr2(local)[0]), sumOpt(expr1(local)[1], expr2(local)[1])), expr1pr, op, expr2pr)
    elif op == '-':
        p[0] = ast.P_expression_binop(lambda local: (typef(expr1(local)[0], expr2(local)[0]), subOpt(expr1(local)[1], expr2(local)[1])), expr1pr, op, expr2pr)
    elif op == '*':
        p[0] = ast.P_expression_binop(lambda local: (typef(expr1(local)[0], expr2(local)[0]), mulOpt(expr1(local)[1], expr2(local)[1])), expr1pr, op, expr2pr)
    elif op == '/':
        p[0] = ast.P_expression_binop(lambda local: ('float', divOpt(expr1(local)[1], expr2(local)[1])), expr1pr, op, expr2pr)
    elif op == "==":
        p[0] = ast.P_expression_binop(lambda local: ('boolean', True if expr1(local)[1] == expr2(local)[1] else False), expr1pr, op, expr2pr)
    elif op == "!=":
        p[0] = ast.P_expression_binop(lambda local: ('boolean', True if expr1(local)[1] != expr2(local)[1] else False), expr1pr, op, expr2pr)
    elif op == ">=":
        p[0] = ast.P_expression_binop(lambda local: ('boolean', True if expr1(local)[1] >= expr2(local)[1] else False), expr1pr, op, expr2pr)
    elif op == "<=":
        p[0] = ast.P_expression_binop(lambda local: ('boolean', True if expr1(local)[1] <= expr2(local)[1] else False), expr1pr, op, expr2pr)
    elif op == ">":
        p[0] = ast.P_expression_binop(lambda local: ('boolean', True if expr1(local)[1] > expr2(local)[1] else False), expr1pr, op, expr2pr)
    elif op == "<":
        p[0] = ast.P_expression_binop(lambda local: ('boolean', True if expr1(local)[1] < expr2(local)[1] else False), expr1pr, op, expr2pr)
    elif op == "**":
        p[0] = ast.P_expression_binop(lambda local: (str(type(expr1(local)[1] ** expr2(local)[1]))[8:-2], expr1(local)[1] ** expr2(local)[1]), expr1pr, op, expr2pr)


def sumOpt(a, b):
    if a == 0:
        return b
    if b == 0:
        return a
    return a + b
    
def subOpt(a, b):
    return a if b == 0 else a - b


def mulOpt(a, b):
    (a, b) = (a, b) if a is int and b is int and a > b else (b, a)
    return a if b == 1 else a * b


def divOpt(a, b):
    return a if b == 1 else a/b


def p_expression_unop(p):
    '''expression : sin expression
                  | cos expression
                  | exp expression
                  | sqrt expression
                  | log expression
                  | intToFloat expression
                  | floatToInt expression'''

    op = p[1]
    exprPr = p[2]
    expr = exprPr.fun
    if op == 'sin':
        p[0] = ast.P_expression_unop(lambda local: ('float', math.sin(expr(local)[1])), op, exprPr)
    elif op == 'cos':
        p[0] = ast.P_expression_unop(lambda local: ('float', math.cos(expr(local)[1])), op, exprPr)
    elif op == 'exp':
        p[0] = ast.P_expression_unop(lambda local: ('float', math.exp(expr(local)[1])), op, exprPr)
    elif op == 'sqrt':
        p[0] = ast.P_expression_unop(lambda local: ('float', math.sqrt(expr(local)[1])), op, exprPr)
    elif op == 'log':
        p[0] = ast.P_expression_unop(lambda local: ('float', math.log(expr(local)[1])), op, exprPr)
    elif op == 'intToFloat':
        p[0] = ast.P_expression_unop(lambda local: ('float', float(expr(local)[1])), op, exprPr)
    elif op == 'floatToInt':
        p[0] = ast.P_expression_unop(lambda local: ('int', int(expr(local)[1])), op, exprPr)

def p_print(p):
    '''statement : print expression'''
    expr = p[2].fun
    p[0] = ast.P_print(lambda local: (print(expr(local)[1])))

def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    uminusPr = -p[2]
    uminus = uminus.fun
    p[0] = ast.P_expression_uminus(lambda local: uminus(local), uminusPr)


def p_expression_group(p):
    "expression : '(' expression ')'"
    groupPr = p[2]
    group = groupPr.fun
    p[0] = ast.P_expression_group(lambda local: group(local), groupPr)


def p_expression_number(p):
    '''expression : REAL_NUMBER
                  | NATURAL_NUMBER
                  | BOOL
                  | STR'''
    number = p[1]
    if (isinstance(number, int)):
        p[0] = ast.P_expression_number(lambda local: ('int', number), 'int', number)
    elif (isinstance(number, float)):
        p[0] = ast.P_expression_number(lambda local: ('float', number), 'float', number)
    elif (number == "True"):
        p[0] = ast.P_expression_number(lambda local: ('boolean', True), 'boolean', number)
    elif (number == "False"):
        p[0] = ast.P_expression_number(lambda local: ('boolean', False), 'boolean', number)
    else:
        p[0] = ast.P_expression_number(lambda local: ('string', number[1:-1]), 'string', number)

def p_expression_name(p):
    """expression : NAME"""
    name = p[1]

    used_names.append(name)

    def do_nothing(local):
        print("Undefined name '%s'" % name)
        pass
    def parseName(local):
        try:
            if name in list(local.keys()):
                return names(local, name)
            else:
                return do_nothing(local)
        except LookupError:
            return do_nothing(local)
    p[0] = ast.P_expression_name(parseName, name)

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")


import ply.yacc as yacc

parser = yacc.yacc()


def parse(input_str):
    return yacc.parse(input_str), used_names, expressions


# while True:
#    try:
#        s = input('calc > ')
#    except EOFError:
#        break
#    if not s:
#        continue
#    yacc.parse(s)
