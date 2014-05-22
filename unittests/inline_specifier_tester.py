# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import unittest
import parser_test_case
from pygccxml import parser
from pygccxml import declarations


class tester_t(parser_test_case.parser_test_case_t):

    global_ns = None

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.header = 'inline_specifier.hpp'

    def setUp(self):
        if not tester_t.global_ns:
            decls = parser.parse([self.header], self.config)
            tester_t.global_ns = declarations.get_global_namespace(decls)
            tester_t.global_ns.init_optimizer()

    def test(self):
        inlined_funcs = self.global_ns.calldefs('inlined')
        self.failUnless(len(inlined_funcs))
        for f in inlined_funcs:
            self.failUnless(f.has_inline)

        not_inlined_funcs = self.global_ns.calldefs('not_inlined')
        self.failUnless(len(not_inlined_funcs))
        for f in not_inlined_funcs:
            self.failUnless(f.has_inline is False)

    def test2(self):
        pass


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(tester_t))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())

if __name__ == "__main__":
    run_suite()
