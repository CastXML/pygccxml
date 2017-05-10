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
        self.header = "test_function_pointer.hpp"

    def test_function_pointer(self):
        """
        Test working with pointers and function pointers.

        """

        decls = parser.parse([self.header], self.config)
        global_ns = declarations.get_global_namespace(decls)

        # Test on a function pointer
        criteria = declarations.variable_matcher(name="func1")
        variables = declarations.matcher.find(criteria, global_ns)

        self.assertTrue(variables[0].name == "func1")
        self.assertTrue(
            isinstance(variables[0].decl_type, declarations.pointer_t))
        self.assertTrue(
            str(variables[0].decl_type) == "void (*)( int,double )")
        self.assertTrue(
            declarations.is_calldef_pointer(variables[0].decl_type))
        self.assertTrue(
            isinstance(declarations.remove_pointer(variables[0].decl_type),
                       declarations.free_function_type_t))

        # Get the function (free_function_type_t) and test the return and
        # argument types
        function = variables[0].decl_type.base
        self.assertTrue(isinstance(function.return_type, declarations.void_t))
        self.assertTrue(
            isinstance(function.arguments_types[0], declarations.int_t))
        self.assertTrue(
            isinstance(function.arguments_types[1], declarations.double_t))

        # Test on a normal pointer
        criteria = declarations.variable_matcher(name="myPointer")
        variables = declarations.matcher.find(criteria, global_ns)

        self.assertTrue(variables[0].name == "myPointer")
        self.assertTrue(
            isinstance(variables[0].decl_type, declarations.pointer_t))
        self.assertFalse(
            declarations.is_calldef_pointer(variables[0].decl_type))
        self.assertTrue(
            isinstance(declarations.remove_pointer(variables[0].decl_type),
                       declarations.volatile_t))

        # Test on function pointer in struct (x8)
        for d in global_ns.declarations:
            if d.name == "x8":
                self.assertTrue(
                    isinstance(d.decl_type, declarations.pointer_t))
                self.assertTrue(declarations.is_calldef_pointer(d.decl_type))
                self.assertTrue(
                    isinstance(
                        declarations.remove_pointer(d.decl_type),
                        declarations.member_function_type_t))
                self.assertTrue(
                    str(declarations.remove_pointer(d.decl_type)) ==
                    "void ( ::some_struct_t::* )(  )")


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
