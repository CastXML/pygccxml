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

class tester_t( parser_test_case.parser_test_case_t ):
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE    
    global_ns = None
    def __init__(self, *args ):
        parser_test_case.parser_test_case_t.__init__( self, *args )
        self.header = 'vector_traits.hpp'
        self.global_ns = None
        
    def setUp(self):
        if not tester_t.global_ns:
            decls = parser.parse( [self.header], self.config ) 
            tester_t.global_ns = declarations.get_global_namespace( decls )
        self.global_ns = tester_t.global_ns
    
    def validate_yes( self, value_type, container ):
        traits = declarations.vector_traits
        self.failUnless( traits.is_vector( container ) )
        self.failUnless( declarations.is_same( value_type, traits.value_type( container ) ) )
        
    def test_global_ns( self ):
        value_type = self.global_ns.class_( '_0_' )
        container = self.global_ns.typedef( 'container', recursive=False )
        self.validate_yes( value_type, container )
        
    def test_yes( self ):
        yes_ns = self.global_ns.namespace( 'yes' )
        for struct in yes_ns.classes():
            if not struct.name.startswith( '_' ):
                continue
            if not struct.name.endswith( '_' ):
                continue
            self.validate_yes( struct.typedef( 'value_type' )
                               , struct.typedef( 'container' ) ) 
    
    def test_no( self ):
        traits = declarations.vector_traits
        no_ns = self.global_ns.namespace( 'no' )
        for struct in no_ns.classes():
            if not struct.name.startswith( '_' ):
                continue
            if not struct.name.endswith( '_' ):
                continue
            self.failUnless( not traits.is_vector( struct.typedef( 'container' ) ) )
    
def create_suite():
    suite = unittest.TestSuite()        
    suite.addTest( unittest.makeSuite(tester_t))
    return suite

def run_suite():
    unittest.TextTestRunner(verbosity=2).run( create_suite() )

if __name__ == "__main__":
    run_suite()