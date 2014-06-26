# Copyright 2014 Insight Software Consortium.
# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import unittest
import autoconfig
import parser_test_case

from pygccxml import parser
from pygccxml import declarations


class tester_t(parser_test_case.parser_test_case_t):

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.header = 'core_ns_join_1.hpp'
        self.config = autoconfig.cxx_parsers_cfg.gccxml.clone()
        self.config.start_with_declarations.extend(['E11', 'ns::ns12::E13'])

    def __check_result(self, decls):
        E11 = declarations.find_declaration(decls, fullname='::E11')
        self.failUnless(E11, "unable to find 'E11' enum")
        ns12 = declarations.find_declaration(decls, fullname='::ns::ns12')
        self.failUnless(ns12, "unable to find 'ns12' namespace")
        E13 = declarations.find_declaration(ns12.declarations, name='E13')
        self.failUnless(E13, "unable to find 'E13' enum")
        E14 = declarations.find_declaration(decls, name='E14')
        self.failUnless(
            not E14,
            "enum 'E14' should not be found in declarations")

    def test_simple(self):
        decls = parser.parse([self.header], self.config)
        self.__check_result(decls)

    def test_project_reader(self):
        reader = parser.project_reader_t(self.config)
        decls = reader.read_files(
            [parser.file_configuration_t(self.header,
                                         self.config.start_with_declarations)],
            parser.COMPILATION_MODE.FILE_BY_FILE)
        self.__check_result(decls)
        decls = reader.read_files(
            [parser.file_configuration_t(self.header,
                                         self.config.start_with_declarations)],
            parser.COMPILATION_MODE.ALL_AT_ONCE)
        self.__check_result(decls)


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(tester_t))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())

if __name__ == "__main__":
    run_suite()
