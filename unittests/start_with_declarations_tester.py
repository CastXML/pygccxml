# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import unittest

from . import autoconfig
from . import parser_test_case

from pygccxml import parser
from pygccxml import declarations


class Test(parser_test_case.parser_test_case_t):

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.header = 'core_ns_join_1.hpp'
        self.config = autoconfig.cxx_parsers_cfg.config.clone()
        self.config.start_with_declarations.extend(['E11', 'ns::ns12::E13'])

    def __check_result(self, decls):
        E11 = declarations.find_declaration(decls, fullname='::E11')
        self.assertTrue(E11, "unable to find 'E11' enum")
        ns12 = declarations.find_declaration(decls, fullname='::ns::ns12')
        self.assertTrue(ns12, "unable to find 'ns12' namespace")
        E13 = declarations.find_declaration(ns12.declarations, name='E13')
        self.assertTrue(E13, "unable to find 'E13' enum")
        E14 = declarations.find_declaration(decls, name='E14')
        self.assertTrue(
            not E14,
            "enum 'E14' should not be found in declarations")

    def test_simple(self):
        decls = parser.parse([self.header], self.config)
        self.__check_result(decls)

    def test_project_reader_file_by_file(self):
        reader = parser.project_reader_t(self.config)
        decls = reader.read_files(
            [parser.file_configuration_t(
                self.header, self.config.start_with_declarations)],
            parser.COMPILATION_MODE.FILE_BY_FILE)
        self.__check_result(decls)

    def test_project_reader_all_at_once(self):
        reader = parser.project_reader_t(self.config)
        decls = reader.read_files(
            [parser.file_configuration_t(
                self.header, self.config.start_with_declarations)],
            parser.COMPILATION_MODE.ALL_AT_ONCE)
        self.__check_result(decls)


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
