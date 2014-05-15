# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import unittest
import parser_test_case

from pygccxml import parser
from pygccxml import declarations

class tester_t( parser_test_case.parser_test_case_t ):
    global_ns = None
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE    
    def __init__(self, *args ):
        parser_test_case.parser_test_case_t.__init__( self, *args )
        self.header = 'classes.hpp'
        self.global_ns = None
        
    def setUp(self):
        if not tester_t.global_ns:
            decls = parser.parse( [self.header], self.config )
            tester_t.global_ns = declarations.get_global_namespace( decls )
            tester_t.global_ns.init_optimizer()
        self.global_ns = tester_t.global_ns
            
    def test_global( self ):       
        gns = self.global_ns
        gns.class_( 'cls' )
        gns.class_( '::cls' )
        
    def test_ns1( self ):       
        gns = self.global_ns
        ns1 = gns.namespace( 'ns' )
        
        gns.class_( 'nested_cls' )
        self.failUnlessRaises( Exception, lambda: gns.class_( 'ns::nested_cls' ) )
        gns.class_( '::ns::nested_cls' )
        
        self.failUnlessRaises( Exception, lambda: ns1.class_( '::nested_cls' ) )
        ns1.class_( 'nested_cls' )
        ns1.class_( '::ns::nested_cls' )        

def create_suite():
    suite = unittest.TestSuite()        
    suite.addTest( unittest.makeSuite(tester_t))
    return suite

def run_suite():
    unittest.TextTestRunner(verbosity=2).run( create_suite() )

if __name__ == "__main__":
    run_suite()
