# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import unittest
import os

from . import parser_test_case

from pygccxml import parser
from pygccxml import declarations


class Test(parser_test_case.parser_test_case_t):
    global_ns = None

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.header = 'declarations_calldef.hpp'
        self.global_ns = None

    def setUp(self):
        if not Test.global_ns:
            decls = parser.parse([self.header], self.config)
            Test.global_ns = declarations.get_global_namespace(decls)
            Test.global_ns.init_optimizer()
        self.global_ns = Test.global_ns

    def test_compound_argument_type(self):
        do_smth = self.global_ns.calldefs('do_smth')
        self.assertTrue(do_smth, "unable to find do_smth")
        do_smth.function_type()

    def test_stderr_present_and_readable(self):
        with open(os.path.join('unittests', 'data', self.header), 'r') as f:
            source_str = f.read()

        err_str = "add some stuff that should not compile"
        source_str += err_str
        with self.assertRaises(RuntimeError) as e_context:
            decls = parser.parse_string(source_str, self.config)

        self.assertIn(err_str, e_context.exception.args[0])


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(
        unittest.TestLoader().loadTestsFromTestCase(testCaseClass=Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
