# =============================================================================
#
#  Copyright 2014 Insight Software Consortium
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0.txt
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
# =============================================================================

# Copyright 2004-2013 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import os
import unittest
import autoconfig
import parser_test_case

from pygccxml import parser
from pygccxml import declarations


class tester_t(parser_test_case.parser_test_case_t):

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
            sr = open(
                os.path.join(
                    autoconfig.build_directory, file_name + '.sr.txt'), 'w+')
            pr = open(
                os.path.join(
                    autoconfig.build_directory, file_name + '.pr.txt'), 'w+')
            declarations.print_declarations(
                s, writer=lambda l: sr.write(l + os.linesep))
            declarations.print_declarations(
                p, writer=lambda l: pr.write(l + os.linesep))
            sr.close()
            pr.close()
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

        self.failUnless(
            src_decls == prj_decls,
            "There is a difference between declarations")


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(tester_t))
    suite.addTest(unittest.makeSuite(tester2_t))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())

if __name__ == "__main__":
    run_suite()
