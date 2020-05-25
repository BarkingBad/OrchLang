def printNode(optionalNone):
    if optionalNone is None:
        return '"None"'
    elif isinstance(optionalNone, str):
        return '"' + optionalNone + '"'
    else:
        return repr(optionalNone)


class P_empty:
    def __init__(self):
        self.fun = lambda local: ""


class P_start:
    def __init__(self, block):
        self.block = block

    def __str__(self):
        return "P_start(" + str(self.block) + ")"

    def __repr__(self):
        return '{"P_start" :[' + printNode(self.block) + ']}'


class P_statements:
    def __init__(self, statement, statements):
        self.statement = statement
        self.statements = statements

    def has_statements(self):
        if self.statements is None:
            return False
        else:
            return True

    def __str__(self):
        return "P_statements(" + str(self.statement) + "," + str(self.statements) + ")"

    def __repr__(self):
        return '{"P_statements" :[' + printNode(self.statement) + "," + printNode(self.statements) + ']}'


class P_call_function:
    def __init__(self, fun, name, params):
        self.fun = fun
        self.name = name
        self.params = params

    def __str__(self):
        return "P_call_function(" + str(self.name) + "," + str(self.params) + ")"

    def __repr__(self):
        return '{"P_call_function" :[' + printNode(self.name) + "," + printNode(self.params) + ']}'


class P_params:
    def __init__(self, typeo, name, params):
        self.typeo = typeo
        self.name = name
        self.params = params

    def has_params(self):
        if self.params is None:
            return False
        else:
            return True

    def __str__(self):
        return "P_params(" + str(self.typeo) + "," + str(self.name) + "," + str(self.params) + ")"

    def __repr__(self):
        return '{"P_params" :[' + printNode(self.typeo) + "," + printNode(self.name) + "," + printNode(self.params) + ']}'


class P_statement_reassign:
    def __init__(self, fun, name, statement):
        self.fun = fun
        self.name = name
        self.statement = statement

    def __str__(self):
        return "P_statement_reassign(" + str(self.name) + "," + str(self.statement) + ")"

    def __repr__(self):
        return '{"P_statement_reassign" :[' + printNode(self.name) + "," + printNode(self.statement) + ']}'


class P_statement_assign:
    def __init__(self, fun, typeo, name, statement):
        self.fun = fun
        self.typeo = typeo
        self.name = name
        self.statement = statement

    def __str__(self):
        return "P_statement_assign(" + str(self.typeo) + "," + str(self.name) + "," + str(self.statement) + ")"

    def __repr__(self):
        return '{"P_statement_assign" :[' + printNode(self.typeo) + "," + printNode(self.name) + "," + printNode(self.statement) + ']}'


class P_define:
    def __init__(self, fun, name, params, statement):
        self.fun = fun
        self.name = name
        self.params = params
        self.statement = statement

    def __str__(self):
        return "P_define(" + str(self.name) + "," + str(self.params) + "," + str(self.statement) + ")"

    def __repr__(self):
        return '{"P_define" :[' + printNode(self.name) + "," + printNode(self.params) + "," + printNode(self.statement) + ']}'


class P_while_statement:
    def __init__(self, fun, epxression, statement):
        self.fun = fun
        self.epxression = epxression
        self.statement = statement

    def __str__(self):
        return "P_while_statement(" + str(self.epxression) + "," + str(self.statement) + ")"

    def __repr__(self):
        return '{"P_while_statement" :[' + printNode(self.epxression) + "," + printNode(self.statement) + ']}'


class P_if_statement:
    def __init__(self, fun, expression, statement, statement2):
        self.fun = fun
        self.expression = expression
        self.statement = statement
        self.statement2 = statement2

    def __str__(self):
        return "P_if_statement(" + str(self.expression) + "," + str(self.statement) + ")"

    def __repr__(self):
        return '{"P_if_statement" :[' + printNode(self.expression) + "," + printNode(self.statement) + "," + printNode(self.statement) + ']}'


class P_for_statement:
    def __init__(self, fun, init, condition, update, action):
        self.fun = fun
        self.init = init
        self.condition = condition
        self.update = update
        self.action = action

    def __str__(self):
        return "P_for_statement(" + str(self.init) + "," + str(self.condition) + "," + str(self.update) + "," + str(self.action) + ")"

    def __str__(self):
        return '{"P_for_statement" :[' + printNode(self.init) + "," + printNode(self.condition) + "," + printNode(self.update) + "," + printNode(self.action) + ']}'


class P_casual_statements:
    def __init__(self, operation):
        self.operation = operation

    def __str__(self):
        return "P_casual_statements(" + str(self.operation) + ")"

    def __repr__(self):
        return '{"P_casual_statements" :[' + printNode(self.operation) + ']}'


class P_blocks:
    def __init__(self, block, blocks):
        self.block = block
        self.blocks = blocks

    def has_blocks(self):
        if self.blocks is None:
            return False
        else:
            return True

    def __str__(self):
        return "P_blocks(" + str(self.block) + "," + str(self.blocks) + ")"

    def __repr__(self):
        return '{"P_blocks" :[' + printNode(self.block) + "," + printNode(self.blocks) + ']}'


class P_block:
    def __init__(self, blocks, casual_statement):
        self.blocks = blocks
        self.casual_statement = casual_statement

    def has_blocks(self):
        if self.blocks is None:
            return False
        else:
            return True

    def has_casual_statement(self):
        if self.casual_statement is None:
            return False
        else:
            return True

    def __str__(self):
        return "P_block(" + str(self.blocks) + "," + str(self.casual_statement) + ")"

    def __repr__(self):
        return '{"P_block" :[' + printNode(self.blocks) + "," + printNode(self.casual_statement) + ']}'


class P_statement_expr:
    def __init__(self, fun, expression):
        self.fun = fun
        self.expression = expression

    def __str__(self):
        return "P_statement_expr(" + str(self.expression) + ")"

    def __repr__(self):
        return '{"P_statement_expr" :[' + printNode(self.expression) + ']}'


class P_expression_binop:
    def __init__(self, fun, expr1, op, expr2):
        self.fun = fun
        self.expr1 = expr1
        self.op = op
        self.expr2 = expr2

    def __str__(self):
        return "P_expression_binop(" + str(self.expr1) + "," + str(self.op) + "," + str(self.expr2) + ")"

    def __repr__(self):
        return '{"P_expression_binop" :[' + printNode(self.expr1) + "," + printNode(self.op) + "," + printNode(self.expr2) + ']}'

    def __eq__(self, other):
        return self.expr1 == other.expr1 and self.op == other.op and self.expr2 == other.expr2

    def __hash__(self):
        return self.expr1.__hash__() * 2137 + self.op.__hash__() * 420 + self.expr2.__hash__() * 69


class P_expression_unop:
    def __init__(self, fun, op, expr):
        self.fun = fun
        self.expr = expr
        self.op = op

    def __str__(self):
        return "P_expression_unop(" + str(self.op) + "," + str(self.expr) + ")"

    def __repr__(self):
        return '{"P_expression_unop" :[' + printNode(self.op) + "," + printNode(self.expr) + ']}'

    def __eq__(self, other):
        return self.expr == other.expr and self.op == other.op

class P_expression_group:
    def __init__(self, fun, expr):
        self.fun = fun
        self.expr = expr

    def __str__(self):
        return "P_expression_group(" + str(self.expr) + ")"

    def __repr__(self):
        return '{"P_expression_group" :[' + printNode(self.expr) + ']}'


class P_expression_uminus:
    def __init__(self, fun, expr):
        self.fun = fun
        self.expr = expr

    def __str__(self):
        return "P_expression_uminus(" + str(self.expr) + ")"

    def __repr__(self):
        return '{"P_expression_uminus" :[' + printNode(self.expr) + ']}'


class P_expression_number:
    def __init__(self, fun, typeo, val):
        self.fun = fun
        self.typeo = typeo
        self.val = val

    def __str__(self):
        return "P_expression_number(" + str(self.typeo) + "," + str(self.val) + ")"

    def __repr__(self):
        return '{"P_expression_number" :[' + printNode(self.typeo) + ',' + printNode(self.val) + ']}'


class P_expression_name:
    def __init__(self, fun, name):
        self.fun = fun
        self.expr = name

    def __str__(self):
        return "P_expression_name(" + str(self.expr) + ")"

    def __repr__(self):
        return '{"P_expression_name" :[' + printNode(self.expr) + ']}'

class P_print:
    def __init__(self, fun):
        self.fun = fun

    def __str__(self):
        return "P_print()"

    def __repr__(self):
        return '{"P_print"}'