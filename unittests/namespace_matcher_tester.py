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
        self.assertTrue(
            str(criteria) == '(decl type==namespace_t) and (name==bit_fields)')

    def test_allow_empty(self):
        global_ns = declarations.get_global_namespace(self.declarations)
        global_ns.init_optimizer()
        self.assertTrue(
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
    suite.addTest(unittest.makeSuite(Test))
    suite.addTest(unittest.makeSuite(unnamed_ns_tester_t))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
