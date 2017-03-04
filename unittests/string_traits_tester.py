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
        self.header = 'string_traits.hpp'
        self.global_ns = None

    def setUp(self):
        if not Test.global_ns:
            decls = parser.parse([self.header], self.config)
            Test.global_ns = declarations.get_global_namespace(decls)
        self.global_ns = Test.global_ns

    def validate_yes(self, ns, controller):
        for typedef in ns.typedefs():
            self.assertTrue(controller(typedef.decl_type))

    def validate_no(self, ns, controller):
        for typedef in ns.typedefs():
            self.assertTrue(not controller(typedef.decl_type))

    def test_string(self):
        string_traits = self.global_ns.namespace('string_traits')
        self.validate_yes(
            string_traits.namespace('yes'),
            declarations.is_std_string)
        self.validate_no(
            string_traits.namespace('no'),
            declarations.is_std_string)

    def test_wstring(self):
        wstring_traits = self.global_ns.namespace('wstring_traits')
        self.validate_yes(
            wstring_traits.namespace('yes'),
            declarations.is_std_wstring)
        self.validate_no(
            wstring_traits.namespace('no'),
            declarations.is_std_wstring)


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
