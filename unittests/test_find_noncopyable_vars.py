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
        self.header = "find_noncopyable_vars.hpp"
        decls = parser.parse([self.header], self.config)
        self.global_ns = declarations.get_global_namespace(decls)

    def test(self):
        """
        Test the find_noncopyable_vars function

        """

        # The ptr1 variable in the holder struct can be copied,
        # but not the ptr2 variable
        holder = self.global_ns.class_("holder")
        nc_vars = declarations.find_noncopyable_vars(holder)
        self.assertEqual(len(nc_vars), 1)
        self.assertEqual(nc_vars[0].name, "ptr2")
        self.assertTrue(declarations.is_pointer(nc_vars[0].decl_type))
        self.assertTrue(declarations.is_const(nc_vars[0].decl_type))


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
