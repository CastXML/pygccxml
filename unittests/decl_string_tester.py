# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import os
import unittest

from . import autoconfig
from . import parser_test_case

from pygccxml import parser
from pygccxml import declarations


class Test(parser_test_case.parser_test_case_t):
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    global_ns = None

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.header = os.path.join(
            autoconfig.data_directory,
            'declarations_calldef.hpp')
        self.template = """
        //test generated declaration string using gcc(xml) compiler
        #include "declarations_calldef.hpp"
        void test_generated_decl_string( %s );
        """

    def setUp(self):
        if not Test.global_ns:
            decls = parser.parse([self.header], self.config)
            Test.global_ns = declarations.get_global_namespace(decls)
            Test.global_ns.init_optimizer()

    def test_member_function(self):
        member_inline_call = \
            self.global_ns.member_function('member_inline_call')
        decls = parser.parse_string(
            self.template %
            member_inline_call.decl_string,
            self.config)
        self.assertTrue(
            decls,
            "Created decl_string for member function contains mistake")

    def test_free_function(self):
        return_default_args = \
            self.global_ns.free_function('return_default_args')
        decls = parser.parse_string(
            self.template %
            return_default_args.decl_string,
            self.config)
        self.assertTrue(
            decls,
            "Created decl_string for global function contains mistake")

    def test_all_mem_and_free_funs(self):
        ns = self.global_ns.namespace('::declarations::calldef')
        for f in ns.member_functions():
            decls = parser.parse_string(
                self.template % f.decl_string, self.config)
            self.assertTrue(
                decls,
                "Created decl_string for member function contains mistake")
        for f in ns.free_functions():
            decls = parser.parse_string(
                self.template % f.decl_string, self.config)
            self.assertTrue(
                decls,
                "Created decl_string for member function contains mistake")


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
