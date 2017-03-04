# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import os
import unittest

from . import autoconfig
from . import parser_test_case

from pygccxml import parser
from pygccxml import declarations


class Test(parser_test_case.parser_test_case_t):

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.__files = [
            'core_types.hpp',
            'core_ns_join_1.hpp',
            'core_ns_join_2.hpp',
            'core_ns_join_3.hpp',
            'core_membership.hpp',
            'core_class_hierarchy.hpp',
            'core_diamand_hierarchy_base.hpp',
            'core_diamand_hierarchy_derived1.hpp',
            'core_diamand_hierarchy_derived2.hpp',
            'core_diamand_hierarchy_final_derived.hpp',
            'core_overloads_1.hpp',
            'core_overloads_2.hpp']

    def __test_correctness_impl(self, file_name):
        prj_reader = parser.project_reader_t(self.config)
        prj_decls = prj_reader.read_files(
            [file_name] * 2,
            compilation_mode=parser.COMPILATION_MODE.FILE_BY_FILE)
        src_reader = parser.source_reader_t(self.config)
        src_decls = src_reader.read_file(file_name)
        if src_decls != prj_decls:
            s = src_decls[0]
            p = prj_decls[0]
            bdir = autoconfig.build_directory
            with open(os.path.join(bdir, file_name + '.sr.txt'), 'w+') as sr:
                with open(
                        os.path.join(bdir, file_name + '.pr.txt'), 'w+') as pr:

                    declarations.print_declarations(
                        s, writer=lambda l: sr.write(l + os.linesep))
                    declarations.print_declarations(
                        p, writer=lambda l: pr.write(l + os.linesep))

            self.fail(
                "There is a difference between declarations in file %s." %
                file_name)

    def test_correctness(self):
        for src in self.__files:
            self.__test_correctness_impl(src)


class tester2_t(parser_test_case.parser_test_case_t):

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.__files = [
            'separate_compilation/data.h',
            'separate_compilation/base.h',
            'separate_compilation/derived.h']

    def test(self):
        prj_reader = parser.project_reader_t(self.config)
        prj_decls = prj_reader.read_files(
            self.__files,
            compilation_mode=parser.COMPILATION_MODE.FILE_BY_FILE)
        src_reader = parser.source_reader_t(self.config)
        src_decls = src_reader.read_file('separate_compilation/all.h')

        declarations.dump_declarations(
            src_decls,
            os.path.join(
                autoconfig.build_directory, 'separate_compilation.sr.txt'))

        declarations.dump_declarations(
            prj_decls,
            os.path.join(
                autoconfig.build_directory, 'separate_compilation.pr.txt'))

        self.assertTrue(
            src_decls == prj_decls,
            "There is a difference between declarations")


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    suite.addTest(unittest.makeSuite(tester2_t))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
