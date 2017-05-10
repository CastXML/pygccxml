# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import sys
import unittest

from . import parser_test_case

from pygccxml import parser
from pygccxml import declarations


class Test(parser_test_case.parser_test_case_t):

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

        # Redirect sys.stdout to a class with a writer doing nothing
        # This greatly reduces the size of the test output and makes
        # test log files readable.
        # Note: flush needs to be defined; because if not this will
        # result in an AttributeError on call.
        class DontPrint(object):
            def write(*args):
                pass

            def flush(*args):
                pass
        sys.stdout = DontPrint()

        declarations.print_declarations(self.decls)

    def test__str__(self):
        decls = declarations.make_flatten(self.decls)
        for decl in decls:
            str(decl)


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
