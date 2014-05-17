# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import unittest
import autoconfig
import parser_test_case

import pygccxml
from pygccxml.utils import *
from pygccxml.parser import *
from pygccxml.declarations import *

class tester_t( parser_test_case.parser_test_case_t ):
    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.__files = [
            'core_ns_join_1.hpp'
            , 'core_ns_join_2.hpp'
            , 'core_ns_join_3.hpp'
            , 'core_membership.hpp'
            , 'core_class_hierarchy.hpp'
            , 'core_types.hpp'
            , 'core_diamand_hierarchy_base.hpp'
            , 'core_diamand_hierarchy_derived1.hpp'
            , 'core_diamand_hierarchy_derived2.hpp'
            , 'core_diamand_hierarchy_final_derived.hpp'
            , 'core_overloads_1.hpp'
            , 'core_overloads_2.hpp'
        ]

    def test(self):
        prj_reader = project_reader_t( self.config )
        decls = prj_reader.read_files( self.__files
                                           , compilation_mode=COMPILATION_MODE.ALL_AT_ONCE )
        files = declaration_files( decls )
        result = set()
        for fn in files:
            result.add( os.path.split( fn )[1] )
        self.failUnless( set( self.__files ).issubset( result ) )


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest( unittest.makeSuite(tester_t))
    return suite

def run_suite():
    unittest.TextTestRunner(verbosity=2).run( create_suite() )

if __name__ == "__main__":
    run_suite()
