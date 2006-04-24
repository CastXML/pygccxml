# Copyright 2004 Roman Yakovenko.
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

    def __test_correctness_impl(self, file_name ):
        prj_reader = project_reader_t( self.config )
        prj_decls = prj_reader.read_files( [file_name]*2
                                           , compilation_mode=COMPILATION_MODE.FILE_BY_FILE )
        src_reader = source_reader_t( self.config )
        src_decls = src_reader.read_file( file_name )
        self.failUnless( src_decls == prj_decls
                         , "There is a difference between declarations in file %s." % file_name )

    def test_correctness(self):
        for src in self.__files:
            self.__test_correctness_impl( src )
   
def create_suite():
    suite = unittest.TestSuite()        
    suite.addTest( unittest.makeSuite(tester_t))    
    return suite

def run_suite():
    unittest.TextTestRunner(verbosity=2).run( create_suite() )

if __name__ == "__main__":
    run_suite()
