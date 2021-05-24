# Copyright 2014-2021 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import unittest

from . import parser_test_case

from pygccxml import parser
from pygccxml import declarations


class Test(parser_test_case.parser_test_case_t):
    global_ns = None

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.header = "test_ccflags.hpp"
        self.global_ns = None
        self.config.castxml_epic_version = 1
        self.config.append_cflags("-fopenmp")

    def _parse_src(self):
        decls = parser.parse([self.header], self.config)
        Test.global_ns = declarations.get_global_namespace(decls)
        Test.xml_generator_from_xml_file = (
            self.config.xml_generator_from_xml_file
        )
        self.xml_generator_from_xml_file = Test.xml_generator_from_xml_file

        self.global_ns = Test.global_ns

    def _add_ccflags(self):
        if "clang++" in self.config.compiler_path:
            self.config.append_ccflags("-Xpreprocessor")

        self.config.append_ccflags("-fopenmp")

    def test(self):
        # First check that macro is not defined.
        self._parse_src()
        namespace_names = [
            n.name for n in self.global_ns.namespaces(allow_empty=True)
        ]
        self.assertNotIn("ccflags_test_namespace", namespace_names)

        # Next check that macro is defined when passed directly as ccflag
        self._add_ccflags()
        self._parse_src()
        namespace_names = [n.name for n in self.global_ns.namespaces()]
        self.assertIn("ccflags_test_namespace", namespace_names)


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
