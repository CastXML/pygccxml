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
        self.header = "test_array_argument.hpp"
        self.config.cflags = "-std=c++11"

    def test_array_argument(self):

        """
        Test to ensure that function arguments' array size are kept intact
        rather than presented as pointers.

        """

        decls = parser.parse([self.header], self.config)
        global_ns = declarations.get_global_namespace(decls)

        criteria = declarations.calldef_matcher(name="function")
        free_funcs = declarations.matcher.find(criteria, global_ns)
        for free_func in free_funcs:
            decl_string = free_func.create_decl_string(with_defaults=False)
            self.assertEqual(
                decl_string,
                "void ( ::test::* )( int [1024],int [512] )"
            )
            arg1 = free_func.arguments[0]
            arg2 = free_func.arguments[1]
            self.assertEqual(arg1.decl_type.decl_string, "int [1024]")
            self.assertEqual(arg1.name, "arg1")
            self.assertEqual(
                declarations.type_traits.array_size(arg1.decl_type),
                1024
            )
            self.assertIsInstance(
                declarations.type_traits.array_item_type(arg1.decl_type),
                declarations.cpptypes.int_t
            )
            self.assertEqual(arg2.decl_type.decl_string, "int [512]")
            self.assertEqual(arg2.name, "arg2")
            self.assertEqual(
                declarations.type_traits.array_size(arg2.decl_type),
                512
            )
            self.assertIsInstance(
                declarations.type_traits.array_item_type(arg2.decl_type),
                declarations.cpptypes.int_t
            )


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(
        unittest.TestLoader().loadTestsFromTestCase(testCaseClass=Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
