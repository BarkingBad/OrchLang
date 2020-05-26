from contextlib import contextmanager
from io import StringIO
import unittest
import ast
import calc_snapshot_3 
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
        x = calc_snapshot_3.parse(text_input)
    return testcase.assertEqual(out.getvalue(), expect)

class test_2_3(unittest.TestCase):

    def test_3_1_ints(self):
        assertThose(self, "2 + 2", "('int', 4)\n")
        
    def test_3_2_floats(self):
        assertThose(self, "2.0 + 2.0", "('float', 4.0)\n")

    def test_3_3_incompatible_types(self):
        assertThose(self, "2 + 2.0", "Error, incomatbile types\n")

    def test_6_1_is_declard(self):
        calc_snapshot_3.parse("int i = 0")
        assertThose(self, "i", "('int', 0)\n")

    def test_6_2_should_fail(self):
        assertThose(self, "int if = 0", "Syntax error at 'if'\n('int', 0)\n")

    def test_6_3_should_fail(self):
        assertThose(self, "j", "Undefined name 'j'\n") 

if __name__ == '__main__':
    unittest.main()
 
