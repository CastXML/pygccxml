# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import unittest

from . import parser_test_case

from pygccxml import parser
from pygccxml import declarations


class Test(parser_test_case.parser_test_case_t):

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.header = "declaration_string.hpp"
        self.global_ns = None

    def setUp(self):
        if not self.global_ns:
            decls = parser.parse([self.header], self.config)
            self.global_ns = declarations.get_global_namespace(decls)
            self.global_ns.init_optimizer()

    def test(self):
        """
        Test the create_decl_string method.

        """

        myfunc = self.global_ns.free_function("myfunc")

        decl = declarations.free_function_type_t.create_decl_string(
            myfunc.return_type, myfunc.argument_types)

        self.assertTrue(decl != "('int (*)( int,int )', 'int (*)( int,int )')")

        box = self.global_ns.class_("Box")
        myinternfunc = box.member_function("myinternfunc")
        decl = declarations.member_function_type_t.create_decl_string(
            myinternfunc.return_type,
            box.decl_string,
            myinternfunc.argument_types,
            myinternfunc.has_const)

        self.assertTrue(decl != "short int ( ::Box::* )(  ) ")


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
