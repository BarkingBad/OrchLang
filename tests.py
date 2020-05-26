from contextlib import contextmanager
from io import StringIO
import unittest
import ast
import calc 
import sys


@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


class test_2_1(unittest.TestCase):


    # obsługa tokenów dla liczb całkowitych
    def test_1_1_real_token_number(self):
        token_input = "begin 2; end"
        ast_output = """{"P_expression_number" :["int",2]}"""

        with captured_output() as (out, err):
            x, _, _ = calc.parse(token_input)
            self.assertEqual(repr(x.block.blocks.block.casual_statement.operation.expression), ast_output)
        
        self.assertEqual(out.getvalue(), '')


    # obsługa tokenów dla liczb rzeczywistych
    def test_1_2_float_token_number(self):
        token_input = "begin 2.0; end"
        ast_output = """{"P_expression_number" :["float",2.0]}"""

        with captured_output() as (out, err):
            x, _, _ = calc.parse(token_input)
            self.assertEqual(repr(x.block.blocks.block.casual_statement.operation.expression), ast_output)
        
        self.assertEqual(out.getvalue(), '')


    # obsługa tokenów dla funkcji specjalnych sin, cos, itd
    def test_2_1_sin(self):
        token_suite = {
            "begin sin(2); end" : "sin",
            "begin sin2; end" : "sin",
            "begin sin(2.0); end" : "sin",
            "begin sin 2; end" : "sin"
            }

        for expected_input, expected_output in token_suite.items():
            with captured_output() as (out, err):
                x, _, _ = calc.parse(expected_input)
                self.assertEqual(x.block.blocks.block.casual_statement.operation.expression.op, expected_output)
                self.assertEqual(out.getvalue(), '')


    def test_2_2_cos(self):
        token_suite = {
            "begin cos(2); end" : "cos",
            "begin cos2; end" : "cos",
            "begin cos(2.0); end" : "cos",
            "begin cos 2; end" : "cos"
            }

        for expected_input, expected_output in token_suite.items():
            with captured_output() as (out, err):
                x, _, _ = calc.parse(expected_input)
                self.assertEqual(x.block.blocks.block.casual_statement.operation.expression.op, expected_output)
                self.assertEqual(out.getvalue(), '')


    def test_2_3_unary_operations(self):
        token_suite = {
            "begin exp(2); end" : "exp",
            "begin log(2); end" : "log",
            "begin sqrt(2); end" : "sqrt"
            }

        for expected_input, expected_output in token_suite.items():
            with captured_output() as (out, err):
                x, _, _ = calc.parse(expected_input)
                self.assertEqual(x.block.blocks.block.casual_statement.operation.expression.op, expected_output)
                self.assertEqual(out.getvalue(), '')


    # obsługa tokenów dla operatora potęgowania, itd
    def test_3_1_power(self):
        token_suite = {
            "begin 2 ** 4; end" : "**",
            "begin 3**3; end" : "**",
            "begin 2 **3; end" : "**",
            "begin 2** 3; end" : "**"
            }

        for expected_input, expected_output in token_suite.items():
            with captured_output() as (out, err):
                x, _, _ = calc.parse(expected_input)
                self.assertEqual(x.block.blocks.block.casual_statement.operation.expression.op, expected_output)
                self.assertEqual(out.getvalue(), '')


    def test_3_2_addition(self):
        token_suite = {
            "begin 2 + 4; end" : "+",
            "begin 3+3; end" : "+",
            "begin 2 +3; end" : "+",
            "begin 2+ 3; end" : "+"
            }

        for expected_input, expected_output in token_suite.items():
            with captured_output() as (out, err):
                x, _, _ = calc.parse(expected_input)
                self.assertEqual(x.block.blocks.block.casual_statement.operation.expression.op, expected_output)
                self.assertEqual(out.getvalue(), '')

    
    def test_3_3_binary_operations(self):
        token_suite = {
            "begin 2 - 4; end" : "-",
            "begin 2- 4; end" : "-",
            "begin 2 + -4; end" : "+",
            "begin 2 * 4; end" : "*",
            "begin 2* 4; end" : "*",
            "begin 2 *4; end" : "*",
            "begin 2 / 4; end" : "/",
            "begin 2/ 4; end" : "/",
            "begin 2 /4; end" : "/",
            }

        for expected_input, expected_output in token_suite.items():
            with captured_output() as (out, err):
                x, _, _ = calc.parse(expected_input)
                self.assertEqual(x.block.blocks.block.casual_statement.operation.expression.op, expected_output)
                self.assertEqual(out.getvalue(), '')

    # automatyczna koretka błędów w tokenach
    def test_4_1_auto_token_correction(self):
        # not implemented
        pass


def assertThose(testcase, text_input, expect):
    with captured_output() as (out, err):
        x, _, _ = calc.parse(text_input)
    return testcase.assertEqual(out.getvalue(), expect)


class test_2_2(unittest.TestCase):


    # potegowanie
    def test_1_1_power(self):
        assertThose(self, "begin print(2 ** 4); end", "16\n")
        assertThose(self, "begin print(2**4); end", "16\n")
        

    # sin
    def test_1_2_sin(self):
        assertThose(self, "begin print(sin(3.1415926535)); end", "8.979318433952318e-11\n")
        assertThose(self, "begin print(sin3.1415926535); end", "8.979318433952318e-11\n")


    # cos
    def test_1_3_cos(self):
        assertThose(self, "begin print(cos(3.1415926535)); end", "-1.0\n")
        assertThose(self, "begin print(cos3.1415926535); end", "-1.0\n")


    # equality_true
    def test_1_4_equality_true(self):
        assertThose(self, "begin print(1 == 1); end", "True\n")
        assertThose(self, "begin print(1==1); end", "True\n")


    # equality_false
    def test_1_5_equality_false(self):
        assertThose(self, "begin print(1 == 4); end", "False\n")
        assertThose(self, "begin print(1==4); end", "False\n")


    def test_1_6_unequality_true(self):
        assertThose(self, "begin print(1 != 4); end", "True\n")
        assertThose(self, "begin print(1!=4); end", "True\n")


    def test_1_7_unequality_false(self):
        assertThose(self, "begin print(1 != 1); end", "False\n")
        assertThose(self, "begin print(1!=1); end", "False\n")


    def test_1_8_greater_true(self):
        assertThose(self, "begin print(3 > 1); end", "True\n")
        assertThose(self, "begin print(3>1); end", "True\n")


    def test_1_9_greater_false(self):
        assertThose(self, "begin print(1 > 3); end", "False\n")
        assertThose(self, "begin print(1>3); end", "False\n")


    def test_1_10_lesser_true(self):
        assertThose(self, "begin print(1 < 3); end", "True\n")
        assertThose(self, "begin print(1<3); end", "True\n")


    def test_1_11_lesser_false(self):
        assertThose(self, "begin print(3 < 1); end", "False\n")
        assertThose(self, "begin print(3<1); end", "False\n")


    def test_1_12_greater_or_equal_true(self):
        assertThose(self, "begin print(3 >= 1); end", "True\n")
        assertThose(self, "begin print(3>=1); end", "True\n")


    def test_1_13_greater_or_equal_false(self):
        assertThose(self, "begin print(1 >= 3); end", "False\n")
        assertThose(self, "begin print(1>=3); end", "False\n")


    def test_1_14_lesser_or_equal_true(self):
        assertThose(self, "begin print(1 <= 3); end", "True\n")
        assertThose(self, "begin print(1<=3); end", "True\n")


    def test_1_15_lesser_or_equal_false(self):
        assertThose(self, "begin print(3 <= 1); end", "False\n")
        assertThose(self, "begin print(3<=1); end", "False\n")


    def test_1_16_negative_sign(self):
        assertThose(self, "begin print(-3); end", "-3\n")
        assertThose(self, "begin print(-3 - -3); end", "0\n")


    def test_2_1_negative_sign(self):
        assertThose(self, "begin print(1); print(2); print(3); end", "1\n2\n3\n")
        assertThose(self, "begin print(1);print(2);print(3); end", "1\n2\n3\n")


    def test_3_1_continue_evalutaion(self):
        assertThose(self, "begin print(1); asdfaerasdf; print(3); end", "1\nUndefined name 'asdfaerasdf'\nUndefined name 'asdfaerasdf'\n3\n")


    def test_4_1_continue_evalutaion(self):
        pass


    def test_5_1_if(self):
        assertThose(self, "begin if(True) print(3) else print(4); end", "3\n")
        assertThose(self, "begin if(1 == 1) print(3) else print(4); end", "3\n")
        assertThose(self, "begin if(1 == 2) print(3) else print(4); end", "4\n")
        assertThose(self, "begin if(False) print(3) else print(4); end", "4\n")


    def test_5_2_while(self):
        assertThose(self, "begin int i = 0; while(i < 1) i = i + 1; end", "")


    def test_5_3_for(self):
        assertThose(self, "begin for(int i = 0; i < 3; i = i + 1) print(i); end", "0\n1\n2\n")
        

class test_2_3(unittest.TestCase):


    # wizualizacja drzewa składniowego
    def test_1_1_ast_simple_addition(self):
        token_input = "begin print(2+2); end"
        pass_function = lambda : "dummy function"
        ast_output = ast.P_start(
            # block
            ast.P_block(
                # blocks
                ast.P_blocks(
                    # block
                    ast.P_block(
                        # blocks
                        None,
                        # casual_statements
                        ast.P_casual_statements(
                            # operation
                            ast.P_print(
                                # fun
                                ast.P_statement_expr(
                                    # fun
                                    pass_function(),
                                    # expression
                                    ast.P_expression_binop(
                                        # fun
                                        pass_function(),
                                        # expr1
                                        ast.P_expression_number(
                                            # fun
                                            pass_function(),
                                            # typeo
                                            "int",
                                            # val
                                            2
                                        ),
                                        # op
                                        "+",
                                        # expr2
                                        ast.P_expression_number(
                                            # fun
                                            pass_function(),
                                            # typeo
                                            "int",
                                            # val
                                            2
                                        )
                                    )
                                )
                            )
                        )
                    ),
                    # blocks
                    None
                ),
                # casual_statements
                None
            )
        )
        ast_repr = """{"P_start" :[{"P_block" :[{"P_blocks" :[{"P_block" :["None",{"P_casual_statements" :[{"P_print"}]}]},"None"]},"None"]}]}"""

        with captured_output() as (out, err):
            x, _, _ = calc.parse(token_input)
            self.assertEqual(repr(x), repr(ast_output))
            self.assertEqual(repr(x), ast_repr)
        
        
    def test_1_2_ast_complex_addition(self):
        token_input = "begin int i = 2; define add(int a) = a + 5; add(i); end"
        ast_repr = ('' +
            '{"P_start" :[' +
                '{"P_block" :[' +
                    '{"P_blocks" :[' +
                        '{"P_block" :[' +
                            '"None",' +
                            '{"P_casual_statements" :[' +
                                '{"P_statement_assign" :[' +
                                    '"int",' +
                                    '"i",' +
                                    '{"P_statement_expr" :[' +
                                        '{"P_expression_number" :[' +
                                            '"int",' +
                                            '2]}' +
                                        ']}' +
                                    ']}' +
                                ']}' +
                            ']},' +
                            '{"P_blocks" :[' +
                                '{"P_block" :[' +
                                    '"None",' +
                                    '{"P_casual_statements" :[' +
                                        '{"P_define" :[' +
                                            '"add",' +
                                            '{"P_params" :[' +
                                                '"int",' +
                                                '"a",' +
                                                '"None"' +
                                            ']},' +
                                            '{"P_statement_expr" :[' +
                                                '{"P_expression_binop" :[' +
                                                    '{"P_expression_name" :[' +
                                                        '"a"' +
                                                    ']},' +
                                                    '"+",' +
                                                    '{"P_expression_number" :[' +
                                                        '"int",' +
                                                        '5' +
                                                    ']}' +
                                                ']}' +
                                            ']}' +
                                        ']}' +
                                    ']}' +
                                ']},' +
                                '{"P_blocks" :[' +
                                    '{"P_block" :[' +
                                        '"None",' +
                                        '{"P_casual_statements" :[' +
                                            '{"P_statement_expr" :[' +
                                                '{"P_call_function" :[' +
                                                    '"add",' +
                                                    '{"P_statements" :[' +
                                                        '{"P_statement_expr" :[' +
                                                            '{"P_expression_name" :[' +
                                                                '"i"' +
                                                            ']}' +
                                                        ']},' +
                                                        '"None"' +
                                                    ']}' +
                                                ']}' +
                                            ']}' +
                                        ']}' +
                                    ']},' +
                                    '"None"' +
                                ']}' +
                            ']}' +
                        ']},' +
                        '"None"' +
                    ']}' +
                ']}' +
            '')

        with captured_output() as (out, err):
            x, _, _ = calc.parse(token_input)
            self.assertEqual(repr(x), ast_repr)


    # deklarowanie typów dla zmiennyc
    def test_2_1_real_types(self):
        token_suite = {
            "begin int i = 2; print(i); end" : "int",
            "begin int i =2; print(i); end" : "int",
            "begin int i=2; print(i); end" : "int",
            "begin int  i=2; print(i); end" : "int",
            "begin int i= 2; print(i); end" : "int",
            }

        for expected_input, expected_output in token_suite.items():
            with captured_output() as (out, err):
                x, _, _ = calc.parse(expected_input)
                self.assertEqual(x.block.blocks.block.casual_statement.operation.typeo, expected_output)
                self.assertEqual(out.getvalue(), '2\n')


    def test_2_2_float_types(self):
        token_suite = {
            "begin float i = 2.0; print(i); end" : "float",
            "begin float i =2.0; print(i); end" : "float",
            "begin float i=2.0; print(i); end" : "float",
            "begin float  i=2.0; print(i); end" : "float",
            "begin float i= 2.0; print(i); end" : "float"
            }

        for expected_input, expected_output in token_suite.items():
            with captured_output() as (out, err):
                x, _, _ = calc.parse(expected_input)
                self.assertEqual(x.block.blocks.block.casual_statement.operation.typeo, expected_output)
                self.assertEqual(out.getvalue(), '2.0\n')


    def test_2_3_dynamic_types(self):
        token_suite = {
            "begin float i = 2.0; print(i); end" : "float",
            "begin int i = 2; print(i); end" : "int",
            "begin boolean i = True; print(i); end" : "boolean",
            "begin boolean i = False; print(i); end" : "boolean"
            }

        for expected_input, expected_output in token_suite.items():
            with captured_output() as (out, err):
                x, _, _ = calc.parse(expected_input)
                self.assertEqual(x.block.blocks.block.casual_statement.operation.typeo, expected_output)


    def test_4_1_assign_statement(self):
        token_type_suite = {
            "begin int i = 20; print(i); end" : "int",
            "begin int i = 2; end" : "int",
            "begin int abecadlo = 220; end" : "int",
            }
            
        values_suite = {
            "begin int i = 2; print(i); end" : "2\n",
            "begin float i = 2.0; print(i); end" : "2.0\n",
            "begin boolean i = True; print(i); end" : "True\n",
            }

        for expected_input, expected_output in token_type_suite.items():
            with captured_output() as (out, err):
                x, _, _ = calc.parse(expected_input)
                self.assertEqual(x.block.blocks.block.casual_statement.operation.typeo, expected_output)

        for expected_input, expected_output in values_suite.items():
            with captured_output() as (out, err):
                x, _, _ = calc.parse(expected_input)
                self.assertEqual(out.getvalue(), expected_output)


    def test_4_2_assign_statement(self):
        token_type_suite = {
            "begin int i = 20; i = 21; print(i); end" : "int",
            "begin int i = 2; i = 3; end" : "int",
            "begin int abecadlo = 220; abecadlo = 221; end" : "int",
            }
            
        values_suite = {
            "begin int i = 2; i = 3; print(i); end" : "3\n",
            "begin float i = 2.0; i = 3.0; print(i); end" : "3.0\n",
            "begin boolean i = True; i = False; print(i); end" : "False\n",
            }

        for expected_input, expected_output in token_type_suite.items():
            with captured_output() as (out, err):
                x, _, _ = calc.parse(expected_input)
                self.assertEqual(x.block.blocks.block.casual_statement.operation.typeo, expected_output)

        for expected_input, expected_output in values_suite.items():
            with captured_output() as (out, err):
                x, _, _ = calc.parse(expected_input)
                self.assertEqual(out.getvalue(), expected_output)


    # konwersja typów za pomocą dodatkowego operatora
    def test_8_1_intToFloat(self):
            assertThose(self, "begin int i = 6; print(intToFloat(i)); end", "6.0\n")
            assertThose(self, "begin int i = 6; float j = intToFloat(i); print(j); end", "6.0\n")
            assertThose(self, "begin int i = 6; float j = 15 + intToFloat(i); print(j); end", "21.0\n")
            assertThose(self, "begin int i = 6; float j = sin 2 + intToFloat(i); print(j); end", "6.909297426825682\n")

    
    def test_8_2_floatToInt(self):
            assertThose(self, "begin float i = 6.0; print(floatToInt(i)); end", "6\n")
            assertThose(self, "begin float i = 6.0; int j = floatToInt(i); print(j); end", "6\n")
            assertThose(self, "begin float i = 6.0; int j = 15 + floatToInt(i); print(j); end", "21\n")
            assertThose(self, "begin float i = 6.0; int j = 2 * 2 + floatToInt(i); print(j); end", "10\n")


class test_2_4(unittest.TestCase):


    def test_1_1_define(self):
        assertThose(self, "begin define fun(int a, int b) = a + b; end", "")


    def test_1_2_define(self):
        assertThose(self, "begin define fun(float a, string b) = a; end", "")


    def test_1_3_define(self):
        assertThose(self, "begin define fun(boolean a, boolean b) = b; end", "")


    def test_2_1_block(self):
        assertThose(self, "begin print(2); end", "2\n")


    def test_2_2_block(self):
        assertThose(self, "begin print(2); begin print(3); end end", "2\n3\n")


    def test_3_1_block(self):
        assertThose(self, "begin int i = 0; begin int i = 1; print(i); end end", "1\n")


    def test_3_2_block(self):
        assertThose(self, "begin int i = 0; begin int i = 1; print(i); end print(i); end", "1\n0\n")


    def test_4_1_define(self):
        assertThose(self, "begin define fun(int a, int b) = a + b; fun(1, 2); end", "")


    def test_4_2_define(self):
        assertThose(self, "begin define fun(int a, int b) = a + b; print(fun(1, 2)); end", "3\n")


    def test_5_1_conversion(self):
        assertThose(self, """begin print(3 * "test"); end""", "testtesttest\n")


    def test_5_2_conversion(self):
        assertThose(self, """begin print(3 * 4.5); end""", "13.5\n")


    def test_5_3_conversion(self):
        assertThose(self, """begin print(True * 4); end""", "4\n")


    def test_5_4_conversion(self):
        assertThose(self, """begin print(True + 1.137); end""", "2.137\n")


class test_2_5(unittest.TestCase):


    def test_1_1_inner_functions(self):
        assertThose(self, "begin define sum(int a, int b) = a + b; define mul(int a, int b) = a * b; print(sum(1, mul(2, 3))); end", "7\n")


    def test_1_2_inner_functions(self):
        assertThose(self, "begin define sum(int a, int b) = a + b; define add(int a, int b) = sum(a, b) + b; print(add(2, 3)); end", "8\n")


    def test_1_3_fibonacci(self):
        assertThose(self, "begin define fib(int n) = if (n < 2) n else fib(n - 1) + fib(n - 2); print(fib(10)); end", "55\n")

    def test_2_1_omit_declarations(self):
        with captured_output() as (out, err):
            x, used_names, _ = calc.parse("begin int thisNameShouldNotExist = 1; print(2); end")
            self.assertTrue("thisNameShouldNotExist" not in used_names)


    def test_2_2_dont_omit(self):
        with captured_output() as (out, err):
            x, used_names, _ = calc.parse("begin int thisNameShouldExist = 1; print(thisNameShouldExist); end")
            self.assertTrue("thisNameShouldExist" in used_names)


    def test_3_1_save_the_evaluation_for_later(self):
        with captured_output() as (out, err):
            x, _, expressions = calc.parse("begin 2 + 3; end")
            self.assertTrue(repr(ast.P_expression_binop(_, ast.P_expression_number(_, 'int', 2), '+', ast.P_expression_number(_, 'int', 3))) in expressions.keys())

    

if __name__ == '__main__':
    unittest.main()
