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
        self.header = "test_smart_pointer.hpp"
        self.config.cflags = "-std=c++11"
        self.global_ns = None

    def setUp(self):
        if self.config.xml_generator == "gccxml":
            return
        decls = parser.parse([self.header], self.config)
        self.global_ns = declarations.get_global_namespace(decls)

    def test_is_smart_pointer(self):
        """
        Test smart_pointer_traits.is_smart_pointer method.

        """

        if self.config.xml_generator == "gccxml":
            return

        criteria = declarations.declaration_matcher(name="yes1")
        decls = declarations.matcher.find(criteria, self.global_ns)
        self.assertTrue(
            declarations.smart_pointer_traits.is_smart_pointer(
                decls[0].decl_type))

        criteria = declarations.declaration_matcher(name="no1")
        decls = declarations.matcher.find(criteria, self.global_ns)
        self.assertFalse(
            declarations.smart_pointer_traits.is_smart_pointer(
                decls[0].decl_type))

        criteria = declarations.declaration_matcher(name="no2")
        decls = declarations.matcher.find(criteria, self.global_ns)
        self.assertFalse(
            declarations.smart_pointer_traits.is_smart_pointer(
                decls[0].decl_type))

    def test_is_auto_pointer(self):
        """
        Test auto_ptr_traits.is_smart_pointer method.

        """

        if self.config.xml_generator == "gccxml":
            return

        criteria = declarations.declaration_matcher(name="yes2")
        decls = declarations.matcher.find(criteria, self.global_ns)
        self.assertTrue(
            declarations.auto_ptr_traits.is_smart_pointer(decls[0].decl_type))

        criteria = declarations.declaration_matcher(name="no1")
        decls = declarations.matcher.find(criteria, self.global_ns)
        self.assertFalse(
            declarations.auto_ptr_traits.is_smart_pointer(decls[0].decl_type))

        criteria = declarations.declaration_matcher(name="no2")
        decls = declarations.matcher.find(criteria, self.global_ns)
        self.assertFalse(
            declarations.auto_ptr_traits.is_smart_pointer(decls[0].decl_type))

    def test_smart_pointer_value_type(self):
        """
        Test smart_pointer_traits.value_type method.

        """

        if self.config.xml_generator == "gccxml":
            return

        criteria = declarations.declaration_matcher(name="yes1")
        decls = declarations.matcher.find(criteria, self.global_ns)
        vt = declarations.smart_pointer_traits.value_type(decls[0].decl_type)
        self.assertIsInstance(vt, declarations.int_t)

    def test_auto_pointer_value_type(self):
        """
        Test auto_pointer_traits.value_type method.

        """

        if self.config.xml_generator == "gccxml":
            return

        criteria = declarations.declaration_matcher(name="yes2")
        decls = declarations.matcher.find(criteria, self.global_ns)
        vt = declarations.auto_ptr_traits.value_type(decls[0].decl_type)
        self.assertIsInstance(vt, declarations.double_t)


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
