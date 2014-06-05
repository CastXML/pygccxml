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
        self.header = 'covariant_returns.hpp'

    def setUp(self):
        if not tester_t.global_ns:
            decls = parser.parse([self.header], self.config)
            tester_t.global_ns = declarations.get_global_namespace(decls)
            tester_t.global_ns.init_optimizer()

    def test_is_same_function(self):
        d = self.global_ns.class_('better_algorithm_t')
        b = self.global_ns.class_('algorithm_t')

        df = d.mem_fun('f')
        bf = b.mem_fun('f')

        self.failUnless(
            id(df) != id(bf) and declarations.is_same_function(df, bf))


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(tester_t))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())

if __name__ == "__main__":
    run_suite()
