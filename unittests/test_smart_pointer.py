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

    def test_smart_pointer(self):
        """
        Test code in the smart_pointer_traits module.

        """

        if self.config.xml_generator == "gccxml":
            return

        decls = parser.parse([self.header], self.config)
        global_ns = declarations.get_global_namespace(decls)

        criteria = declarations.declaration_matcher(name="yes1")
        decls = declarations.matcher.find(criteria, global_ns)
        self.assertTrue(
            declarations.smart_pointer_traits.is_smart_pointer(
                decls[0].decl_type))

        criteria = declarations.declaration_matcher(name="yes2")
        decls = declarations.matcher.find(criteria, global_ns)
        self.assertTrue(
            declarations.auto_ptr_traits.is_smart_pointer(decls[0].decl_type))

        criteria = declarations.declaration_matcher(name="no1")
        decls = declarations.matcher.find(criteria, global_ns)
        self.assertFalse(
            declarations.auto_ptr_traits.is_smart_pointer(decls[0].decl_type))

        criteria = declarations.declaration_matcher(name="no2")
        decls = declarations.matcher.find(criteria, global_ns)
        self.assertFalse(
            declarations.auto_ptr_traits.is_smart_pointer(decls[0].decl_type))


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
