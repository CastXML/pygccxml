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
            pass  # utils.remove_file_no_raise( xmlfile, self.config )


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
