# =============================================================================
#
#  Copyright Insight Software Consortium
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

# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import unittest
import parser_test_case

from pygccxml import parser
from pygccxml import declarations


class tester_t(parser_test_case.parser_test_case_t):

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.__files = [
            'core_ns_join_1.hpp',
            'core_ns_join_2.hpp',
            'core_ns_join_3.hpp',
            'core_membership.hpp',
            'core_class_hierarchy.hpp',
            'core_types.hpp',
            'core_diamand_hierarchy_base.hpp',
            'core_diamand_hierarchy_derived1.hpp',
            'core_diamand_hierarchy_derived2.hpp',
            'core_diamand_hierarchy_final_derived.hpp',
            'core_overloads_1.hpp',
            'core_overloads_2.hpp',
            'typedefs_base.hpp']

        # for i, f in enumerate(self.__files):
        # f = parser.create_cached_source_fc(
        #   os.path.join( autoconfig.data_directory, f)
        # , os.path.join( autoconfig.data_directory, f + '.xml') )
        # self.__files[i] = f
        prj_reader = parser.project_reader_t(self.config)
        self.decls = prj_reader.read_files(
            self.__files,
            compilation_mode=parser.COMPILATION_MODE.FILE_BY_FILE)

    def test_printer(self):
        writer = lambda decl: None
        declarations.print_declarations(self.decls, writer=writer)
        # declarations.print_declarations( self.decls )

    def test__str__(self):
        decls = declarations.make_flatten(self.decls)
        for decl in decls:
            str(decl)


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(tester_t))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())

if __name__ == "__main__":
    run_suite()
