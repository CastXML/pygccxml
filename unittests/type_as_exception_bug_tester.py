# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import unittest

from . import parser_test_case

from pygccxml import parser
from pygccxml import declarations


class Test(parser_test_case.parser_test_case_t):
    global_ns = None

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.header = 'type_as_exception_bug.h'

    def setUp(self):
        if not Test.global_ns:
            decls = parser.parse([self.header], self.config)
            Test.global_ns = declarations.get_global_namespace(decls)
            Test.global_ns.init_optimizer()

    def test(self):
        buggy = self.global_ns.member_function('buggy')
        expression_error = self.global_ns.class_('ExpressionError')
        self.assertTrue(len(buggy.exceptions) == 1)
        err = buggy.exceptions[0]
        self.assertTrue(declarations.is_reference(err))
        err = declarations.remove_declarated(
            declarations.remove_reference(err))
        self.assertTrue(err is expression_error)


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
