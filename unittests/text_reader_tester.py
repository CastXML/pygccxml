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

    def test(self):
        fconfig = parser.file_configuration_t(
            data='int i;',
            start_with_declarations=None,
            content_type=parser.file_configuration_t.CONTENT_TYPE.TEXT)

        prj_reader = parser.project_reader_t(self.config)
        decls = prj_reader.read_files(
            [fconfig],
            compilation_mode=parser.COMPILATION_MODE.FILE_BY_FILE)

        var_i = declarations.find_declaration(
            decls, decl_type=declarations.variable_t, name='i')
        self.assertTrue(var_i, "Variable i has not been found.")


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
