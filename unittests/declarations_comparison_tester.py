# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import copy
import unittest

from . import parser_test_case

from pygccxml import parser
from pygccxml import declarations


class Test(parser_test_case.parser_test_case_t):
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.header = 'declarations_comparison.hpp'

    def test_comparison_declaration_by_declaration(self):
        parsed = parser.parse([self.header], self.config)
        copied = copy.deepcopy(parsed)
        parsed = declarations.make_flatten(parsed)
        copied = declarations.make_flatten(copied)
        parsed.sort()
        copied.sort()
        failuers = []
        for parsed_decl, copied_decl, index in \
                zip(parsed, copied, list(range(len(copied)))):

            if parsed_decl != copied_decl:
                failuers.append(
                    ("__lt__ and/or __qe__ does not working " +
                        "properly in case of %s, %s, index %d") %
                    (parsed_decl.__class__.__name__,
                        copied_decl.__class__.__name__, index))
        self.assertTrue(not failuers, 'Failures: ' + '\n\t'.join(failuers))

    def test_comparison_from_reverse(self):
        parsed = parser.parse([self.header], self.config)
        copied = copy.deepcopy(parsed)
        parsed.sort()
        copied.reverse()
        copied.sort()
        x = parsed[4:6]
        x.sort()
        y = copied[4:6]
        y.sort()
        self.assertTrue(
            parsed == copied,
            "__lt__ and/or __qe__ does not working properly")

    def test___lt__transitivnost(self):
        ns_std = declarations.namespace_t(name='std')
        ns_global = declarations.namespace_t(name='::')
        ns_internal = declarations.namespace_t(name='ns')
        ns_internal.parent = ns_global
        ns_global.declarations.append(ns_internal)
        left2right = [ns_std, ns_global]
        right2left = [ns_global, ns_std]
        left2right.sort()
        right2left.sort()
        self.assertTrue(left2right == right2left, "bug: find me")

    def test_same_declarations_different_intances(self):
        parsed = parser.parse([self.header], self.config)
        copied = copy.deepcopy(parsed)
        self.assertTrue(
            parsed == copied,
            "__lt__ and/or __qe__ does not working properly")


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
