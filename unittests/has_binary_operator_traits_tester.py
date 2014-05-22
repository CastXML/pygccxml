# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import unittest
import parser_test_case

from pygccxml import parser
from pygccxml import declarations


class tester_t(parser_test_case.parser_test_case_t):
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    global_ns = None

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.header = 'has_public_binary_operator_traits.hpp'
        self.global_ns = None

    def setUp(self):
        if not tester_t.global_ns:
            decls = parser.parse([self.header], self.config)
            tester_t.global_ns = declarations.get_global_namespace(decls)
        self.global_ns = tester_t.global_ns

    def test_yes(self):
        yes_ns = self.global_ns.namespace('yes')
        for typedef in yes_ns.typedefs():
            self.failUnless(
                declarations.has_public_equal(typedef),
                "Class '%s' should have public operator==" %
                typedef.decl_string)

    def test_no(self):
        no_ns = self.global_ns.namespace('no')
        for typedef in no_ns.typedefs():
            self.failUnless(
                not declarations.has_public_equal(typedef),
                "Class '%s' should not have public operator==" %
                typedef.decl_string)


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(tester_t))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())

if __name__ == "__main__":
    run_suite()
