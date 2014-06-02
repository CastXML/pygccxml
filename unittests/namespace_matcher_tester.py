# Copyright 2004-2013 Roman Yakovenko
# Copyright 2014 Insight Software Consortium
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import unittest
import parser_test_case
from pygccxml import parser
from pygccxml import declarations


class tester_t(parser_test_case.parser_test_case_t):
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.header = 'bit_fields.hpp'
        self.declarations = None

    def setUp(self):
        if not self.declarations:
            self.declarations = parser.parse([self.header], self.config)

    def test(self):
        criteria = declarations.namespace_matcher_t(name='bit_fields')
        declarations.matcher.get_single(criteria, self.declarations)
        self.failUnless(
            str(criteria) == '(decl type==namespace_t) and (name==bit_fields)')

    def test_allow_empty(self):
        global_ns = declarations.get_global_namespace(self.declarations)
        global_ns.init_optimizer()
        self.failUnless(
            0 == len(global_ns.namespaces('does not exist', allow_empty=True)))


class unnamed_ns_tester_t(parser_test_case.parser_test_case_t):
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.header = 'unnamed_ns_bug.hpp'
        self.declarations = None

    def setUp(self):
        if not self.declarations:
            self.declarations = parser.parse([self.header], self.config)

    def test(self):
        declarations.matcher.get_single(
            declarations.namespace_matcher_t(name='::'), self.declarations)


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(tester_t))
    suite.addTest(unittest.makeSuite(unnamed_ns_tester_t))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())

if __name__ == "__main__":
    run_suite()
