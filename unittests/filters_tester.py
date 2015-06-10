# Copyright 2014-2015 Insight Software Consortium.
# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import unittest
import parser_test_case

from pygccxml import parser
from pygccxml import declarations


class tester_t(parser_test_case.parser_test_case_t):
    global_ns = None
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.header = 'declarations_calldef.hpp'
        self.global_ns = None

    def setUp(self):
        if not tester_t.global_ns:
            decls = parser.parse([self.header], self.config)
            tester_t.global_ns = declarations.get_global_namespace(decls)
            tester_t.global_ns.init_optimizer()
        self.global_ns = tester_t.global_ns

    def test_regex(self):
        criteria = declarations.regex_matcher_t(
            'oper.*',
            lambda decl: decl.name)
        operators = declarations.matcher.find(criteria, self.global_ns)
        operators = [d for d in operators if not d.is_artificial]
        self.failUnless(6 == len(operators))

    def test_access_type(self):
        criteria = declarations.access_type_matcher_t(
            declarations.ACCESS_TYPES.PUBLIC)
        public_members = declarations.matcher.find(criteria, self.global_ns)
        if '0.9' in public_members[0].compiler or \
                'CastXML' in public_members[0].compiler:
            public_members = [d for d in public_members if not d.is_artificial]
            self.failUnless(17 == len(public_members))
        else:
            self.failUnless(21 == len(public_members))

    def test_or_matcher(self):
        criteria1 = declarations.regex_matcher_t(
            'oper.*',
            lambda decl: decl.name)
        criteria2 = declarations.access_type_matcher_t(
            declarations.ACCESS_TYPES.PUBLIC)
        found = declarations.matcher.find(
            criteria1 | criteria2,
            self.global_ns)

        if '0.9' in found[0].compiler or 'CastXML' in found[0].compiler:
            found = [d for d in found if not d.is_artificial]
            self.failUnless(15 <= len(found) <= 21)
        else:
            self.failUnless(19 <= len(found) <= 25)

    def test_and_matcher(self):
        criteria1 = declarations.regex_matcher_t(
            'oper.*',
            lambda decl: decl.name)
        criteria2 = declarations.access_type_matcher_t(
            declarations.ACCESS_TYPES.PUBLIC)
        found = declarations.matcher.find(
            criteria1 & criteria2,
            self.global_ns)
        found = [d for d in found if not d.is_artificial]
        self.failUnless(len(found) <= 6)

    def test_not_matcher(self):
        criteria1 = declarations.regex_matcher_t(
            'oper.*',
            lambda decl: decl.name)
        found = declarations.matcher.find(~(~criteria1), self.global_ns)
        found = [d for d in found if not d.is_artificial]
        self.failUnless(len(found) == 6)


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(tester_t))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())

if __name__ == "__main__":
    run_suite()
