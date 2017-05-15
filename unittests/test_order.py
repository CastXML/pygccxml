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
        self.header = "test_order.hpp"

    def test_order(self):
        """
        Test order of const, volatile, etc... in decl_string.

        The convention in pygccxml is that const and volatile qualifiers
        are placed on the right of their `base` type.

        """

        decls = parser.parse([self.header], self.config)
        global_ns = declarations.get_global_namespace(decls)

        c1 = global_ns.variable("c1")
        c2 = global_ns.variable("c2")
        self.assertEqual(c1.decl_type.decl_string, "int const")
        self.assertEqual(c2.decl_type.decl_string, "int const")

        cptr1 = global_ns.variable("cptr1")
        cptr2 = global_ns.variable("cptr2")
        self.assertEqual(cptr1.decl_type.decl_string, "int const * const")
        self.assertEqual(cptr2.decl_type.decl_string, "int const * const")

        v1 = global_ns.variable("v1")
        v2 = global_ns.variable("v2")
        self.assertEqual(v1.decl_type.decl_string, "int volatile")
        self.assertEqual(v2.decl_type.decl_string, "int volatile")

        vptr1 = global_ns.variable("vptr1")
        vptr2 = global_ns.variable("vptr2")
        decl_string = "int volatile * volatile"
        self.assertEqual(vptr1.decl_type.decl_string, decl_string)
        self.assertEqual(vptr2.decl_type.decl_string, decl_string)

        cv1 = global_ns.variable("cv1")
        cv2 = global_ns.variable("cv2")
        cv3 = global_ns.variable("cv3")
        cv4 = global_ns.variable("cv4")
        self.assertEqual(cv1.decl_type.decl_string, "int const volatile")
        self.assertEqual(cv2.decl_type.decl_string, "int const volatile")
        self.assertEqual(cv3.decl_type.decl_string, "int const volatile")
        self.assertEqual(cv4.decl_type.decl_string, "int const volatile")

        cvptr1 = global_ns.variable("cvptr1")
        cvptr2 = global_ns.variable("cvptr2")
        cvptr3 = global_ns.variable("cvptr3")
        cvptr4 = global_ns.variable("cvptr4")
        decl_string = "int const volatile * const volatile"
        self.assertEqual(cvptr1.decl_type.decl_string, decl_string)
        self.assertEqual(cvptr2.decl_type.decl_string, decl_string)
        self.assertEqual(cvptr3.decl_type.decl_string, decl_string)
        self.assertEqual(cvptr4.decl_type.decl_string, decl_string)

        ac1 = global_ns.variable("ac1")
        ac2 = global_ns.variable("ac2")
        self.assertEqual(ac1.decl_type.decl_string, "int const [2]")
        self.assertEqual(ac2.decl_type.decl_string, "int const [2]")

        acptr1 = global_ns.variable("acptr1")
        acptr2 = global_ns.variable("acptr2")
        self.assertEqual(acptr1.decl_type.decl_string, "int const * const [2]")
        self.assertEqual(acptr2.decl_type.decl_string, "int const * const [2]")

        class_a = global_ns.variable("classA")
        if self.config.xml_generator_from_xml_file.is_castxml1:
            # The elaborated type specifier (class) is on the left
            self.assertEqual(class_a.decl_type.decl_string, "class ::A const")
        else:
            self.assertEqual(class_a.decl_type.decl_string, "::A const")


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
