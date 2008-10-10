# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import os
import unittest
import autoconfig
import parser_test_case

from pygccxml import parser 
from pygccxml import declarations

class tester_t( parser_test_case.parser_test_case_t ):
    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.__fname = 'declarations_for_filtering.hpp'
        self.__fpath = declarations.filtering.normalize_path( 
                            os.path.join( autoconfig.data_directory, self.__fname ) ) 
        
    def test_by_location(self):
        reader = parser.source_reader_t( self.config )
        decls = reader.read_file( self.__fname )
        decls_count = len( declarations.make_flatten( decls ) )
        filtered = declarations.filtering.by_location( decls, [autoconfig.data_directory] )
        flatten_filtered = declarations.make_flatten( filtered )
        self.failUnless( len( flatten_filtered  ) != decls_count )
        for decl in flatten_filtered:
            if decl.location:
                self.failUnless( declarations.filtering.normalize_path( decl.location.file_name )
                                 , self.__fpath )
        self.failUnless( declarations.find_declaration( filtered
                                                        , name='color'
                                                        , type=declarations.enumeration_t
                                                        , recursive=False) )
        
def create_suite():
    suite = unittest.TestSuite()        
    suite.addTest( unittest.makeSuite(tester_t))
    return suite

def run_suite():
    unittest.TextTestRunner(verbosity=2).run( create_suite() )

if __name__ == "__main__":
    run_suite()