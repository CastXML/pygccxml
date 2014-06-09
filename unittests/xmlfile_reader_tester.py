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

import os
import unittest
import autoconfig
import parser_test_case
from pygccxml import parser
from pygccxml import declarations


class tester_t(parser_test_case.parser_test_case_t):

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.__fname = 'core_types.hpp'
        # self.__fname = 'merge_free_functions.hpp'

    def test(self):
        src_reader = parser.source_reader_t(self.config)
        src_decls = src_reader.read_file(self.__fname)

        xmlfile = src_reader.create_xml_file(self.__fname)
        print(xmlfile)
        try:
            conf_t = parser.file_configuration_t
            fconfig = conf_t(
                data=xmlfile,
                start_with_declarations=None,
                content_type=conf_t.CONTENT_TYPE.GCCXML_GENERATED_FILE)

            prj_reader = parser.project_reader_t(self.config)
            prj_decls = prj_reader.read_files(
                [fconfig],
                compilation_mode=parser.COMPILATION_MODE.FILE_BY_FILE)

            declarations.dump_declarations(
                src_decls,
                os.path.join(
                    autoconfig.build_directory,
                    'xmlfile_reader.src.txt'))
            declarations.dump_declarations(
                prj_decls,
                os.path.join(
                    autoconfig.build_directory,
                    'xmlfile_reader.prj.txt'))

            if src_decls != prj_decls:
                self.fail(
                    "There is a difference between declarations in file %s." %
                    self.__fname)
        finally:
            pass  # utils.remove_file_no_raise( xmlfile )


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(tester_t))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())

if __name__ == "__main__":
    run_suite()
