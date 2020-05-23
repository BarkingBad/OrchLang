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
        assertThose(self, "begin if(True) print(3); end", "3\n")
        assertThose(self, "begin if(True)print(3); end", "3\n")


    def test_5_2_while(self):
        assertThose(self, "begin int i = 0; while(i < 1) i = i + 1; end", "")


    def test_5_3_for(self):
        assertThose(self, "begin for(int i = 0; i < 3; i = i + 1) print(i); end", "0\n1\n2\n")
