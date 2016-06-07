# Copyright 2014-2016 Insight Software Consortium.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import unittest
import parser_test_case

from pygccxml import parser
from pygccxml import utils
from pygccxml import declarations


class tester_t(parser_test_case.parser_test_case_t):

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.header = "test_map_gcc5.hpp"
        self.config.cflags = "-std=c++11"

    def test_map_gcc5(self):
        """
        The code in test_map_gcc5.hpp was breaking pygccxml.

        Test that case (gcc5 + castxml + c++11).

        See issue #45 and #55

        """

        if self.config.xml_generator == "gccxml":
            return

        decls = parser.parse([self.header], self.config)
        global_ns = declarations.get_global_namespace(decls)

        # This calldef is defined with gcc > 4.9 (maybe earlier, not tested)
        # and -std=c++11. Calling create_decl_string is failing with gcc.
        # With clang the calldef does not exist so the matche
        # will just return an empty list, letting the test pass.
        criteria = declarations.calldef_matcher(name="_M_clone_node")
        free_funcs = declarations.matcher.find(criteria, global_ns)
        for free_funcs in free_funcs:
            print(free_funcs.create_decl_string(with_defaults=False))


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(tester_t))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())

if __name__ == "__main__":
    run_suite()
