# Copyright 2014-2016 Insight Software Consortium.
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
        self.header = "test_non_copyable_recursive.hpp"

    def test_infinite_recursion_base_classes(self):
        """
        Test find_noncopyable_vars

        See #71

        find_noncopyable_vars was throwing:
        RuntimeError: maximum recursion depth exceeded while
        calling a Python object
        """
        decls = parser.parse([self.header], self.config)
        global_ns = declarations.get_global_namespace(decls)

        # Description of the problem (before the fix):
        # find_noncopyable_vars (on Child class) looks up the variables,
        # and finds aBasePtr2 (a pointer to the Base2 class).
        # Then it looks recursively at the base classes of Base2, and finds
        # Base1. Then, it looks up the variables from Base, to check if Base1
        # is non copyable. It finds another aBasePtr2 variable, which leads to
        # a new check of Base2; this recurses infinitely.
        test_ns = global_ns.namespace('Test1')
        cls = test_ns.class_('Child')
        declarations.type_traits_classes.find_noncopyable_vars(cls)
        self.assertTrue(declarations.type_traits_classes.is_noncopyable(cls))

    def test_infinite_recursion_sstream(self):
        """
        Test find_noncopyable_vars

        See #71

        find_noncopyable_vars was throwing:
        RuntimeError: maximum recursion depth exceeded while
        calling a Python object
        """
        decls = parser.parse([self.header], self.config)
        global_ns = declarations.get_global_namespace(decls)

        # Real life example of the bug. This leads to a similar error,
        # but the situation is more complex as there are multiple
        # classes that are related the one to the others
        # (basic_istream, basic_ios, ios_base, ...)
        test_ns = global_ns.namespace('Test2')
        cls = test_ns.class_('FileStreamDataStream')
        declarations.type_traits_classes.find_noncopyable_vars(cls)
        self.assertFalse(declarations.type_traits_classes.is_noncopyable(cls))


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
