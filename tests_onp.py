from contextlib import contextmanager
from io import StringIO
import unittest
import ast
import onp 
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

def assertThose(testcase, text_input, expect):
    with captured_output() as (out, err):
        x = onp.parseONP(text_input)
    return testcase.assertEqual(out.getvalue(), expect)

class test_2_2(unittest.TestCase):

    def test_4_1_addition(self):
        assertThose(self, "2 2 +", "4\n")

        
    def test_4_2_subtraction(self):
        assertThose(self, "2 2 -", "0\n")

        
    def test_4_3_multiplication(self):
        assertThose(self, "2 2 *", "4\n")

        
    def test_4_4_division(self):
        assertThose(self, "2 2 /", "1.0\n")

        
    def test_4_5_cos(self):
        assertThose(self, "3.1415926535 cos", "-1.0\n")     

        
    def test_4_6_sqrt(self):
        assertThose(self, "16 sqrt", "4.0\n")   

        
    def test_4_7_advanced(self):
        assertThose(self, "12 2 3 4 * 10 5 / + * +", "40.0\n")  

        
    def test_4_8_advanced(self):
        assertThose(self, "5 1 2 + 4 * + 3 -", "14\n")  
        
        
if __name__ == '__main__':
    unittest.main()
 
