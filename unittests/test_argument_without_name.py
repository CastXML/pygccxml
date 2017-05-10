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
        self.header = "test_argument_without_name.hpp"
        self.config.cflags = "-std=c++11"

    def test_argument_without_name(self):

        """
        Test passing an object without name to a templated function.

        The test was failing when building the declaration string.
        The declaration string will be 'void (*)(  & )'. If the passed
        object had a name the result would then be 'void (*)(Name & )'.

        See bug #55

        """

        if self.config.xml_generator == "gccxml":
            return

        decls = parser.parse([self.header], self.config)
        global_ns = declarations.get_global_namespace(decls)

        criteria = declarations.calldef_matcher(name="function")
        free_funcs = declarations.matcher.find(criteria, global_ns)
        for free_func in free_funcs:
            decl_string = free_func.create_decl_string(with_defaults=False)
            self.assertEqual(decl_string, "void (*)(  & )")


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
