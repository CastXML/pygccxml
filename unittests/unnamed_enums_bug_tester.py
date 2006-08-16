# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import unittest
import autoconfig
import parser_test_case

from pygccxml import utils
from pygccxml import parser
from pygccxml import declarations

class source_reader_tester_t( parser_test_case.parser_test_case_t ):
    def __init__(self, *args ):
        parser_test_case.parser_test_case_t.__init__( self, *args )
        self.header = 'unnamed_enums_bug1.hpp'
        self.global_ns = None
        
    def setUp(self):
        if not self.global_ns:
            reader = parser.source_reader_t( self.config )
            decls = reader.read_file( self.header )
            self.global_ns = declarations.get_global_namespace( decls )
            self.global_ns.init_optimizer()
            
    def test( self ):                
        names = []
        enums = self.global_ns.enums()        
        map( lambda enum: names.extend( enum.get_name2value_dict().keys() ), enums )
        self.failUnless( len( names ) == 4 )
        self.failUnless( 'x1' in names )
        self.failUnless( 'x2' in names )
        self.failUnless( 'y1' in names )
        self.failUnless( 'y2' in names )

class project_reader_1_tester_t( parser_test_case.parser_test_case_t ):
    def __init__(self, *args ):
        parser_test_case.parser_test_case_t.__init__( self, *args )
        self.header = 'unnamed_enums_bug1.hpp'
        self.global_ns = None
        
    def setUp(self):
        if not self.global_ns:
            decls = parser.parse( [self.header], self.config )
            self.global_ns = declarations.get_global_namespace( decls )
            self.global_ns.init_optimizer()

    def test( self ):                
        names = []
        enums = self.global_ns.enums()        
        map( lambda enum: names.extend( enum.get_name2value_dict().keys() ), enums )
        self.failUnless( len( names ) == 4 )
        self.failUnless( 'x1' in names )
        self.failUnless( 'x2' in names )
        self.failUnless( 'y1' in names )
        self.failUnless( 'y2' in names )

class project_reader_3_tester_t( parser_test_case.parser_test_case_t ):
    def __init__(self, *args ):
        parser_test_case.parser_test_case_t.__init__( self, *args )
        self.headers = ['unnamed_enums_bug1.hpp', 'unnamed_enums_bug2.hpp', 'unnamed_enums_bug1.hpp' ]
        self.global_ns = None
        
    def setUp(self):
        if not self.global_ns:
            decls = parser.parse( self.headers, self.config )
            self.global_ns = declarations.get_global_namespace( decls )
            self.global_ns.init_optimizer()

    def test( self ):                
        names = []
        enums = self.global_ns.enums()        
        map( lambda enum: names.extend( enum.get_name2value_dict().keys() ), enums )
        self.failUnless( len( names ) == 6 )
        self.failUnless( 'x1' in names )
        self.failUnless( 'x2' in names )
        self.failUnless( 'y1' in names )
        self.failUnless( 'y2' in names )
        self.failUnless( 'z1' in names )
        self.failUnless( 'z2' in names )


def create_suite():
    suite = unittest.TestSuite()        
    suite.addTest( unittest.makeSuite(source_reader_tester_t))
    suite.addTest( unittest.makeSuite(project_reader_1_tester_t))
    suite.addTest( unittest.makeSuite(project_reader_3_tester_t))
    return suite

def run_suite():
    unittest.TextTestRunner(verbosity=2).run( create_suite() )

if __name__ == "__main__":
    run_suite()