# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import unittest

from . import parser_test_case

from pygccxml import parser
from pygccxml import declarations


class Test(parser_test_case.parser_test_case_t):
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    global_ns = None

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.header = 'has_public_binary_operator_traits.hpp'
        self.global_ns = None

    def setUp(self):
        if not Test.global_ns:
            decls = parser.parse([self.header], self.config)
            Test.global_ns = declarations.get_global_namespace(decls)
        self.global_ns = Test.global_ns

    def test_yes_equal(self):
        yes_ns = self.global_ns.namespace('yesequal')
        for typedef in yes_ns.typedefs():
            self.assertTrue(
                declarations.has_public_equal(typedef),
                "Class '%s' should have public operator==" %
                typedef.decl_string)

    def test_no_equal(self):
        no_ns = self.global_ns.namespace('noequal')
        for typedef in no_ns.typedefs():
            self.assertTrue(
                not declarations.has_public_equal(typedef),
                "Class '%s' should not have public operator==" %
                typedef.decl_string)

    def test_yes_less(self):
        yes_ns = self.global_ns.namespace('yesless')
        for typedef in yes_ns.typedefs():
            self.assertTrue(
                declarations.has_public_less(typedef),
                "Class '%s' should have public operator<" %
                typedef.decl_string)

    def test_no_less(self):
        no_ns = self.global_ns.namespace('noless')
        for typedef in no_ns.typedefs():
            self.assertTrue(
                not declarations.has_public_less(typedef),
                "Class '%s' should not have public operator<" %
                typedef.decl_string)


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
