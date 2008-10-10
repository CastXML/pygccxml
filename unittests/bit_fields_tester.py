# Copyright 2004-2008 Roman Yakovenko.
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
    
    global_ns = None
    
    def __init__(self, *args ):
        parser_test_case.parser_test_case_t.__init__( self, *args )
        self.header = 'bit_fields.hpp'
        
    def setUp(self):
        if not tester_t.global_ns:
            decls = parser.parse( [self.header], self.config )
            tester_t.global_ns = declarations.get_global_namespace( decls )
            tester_t.global_ns.init_optimizer()
            
    def test( self ):                
        bf_x = self.global_ns.variable( 'x' )        
        self.failUnless( bf_x.bits == 1 )

        bf_y = self.global_ns.variable( 'y' )        
        self.failUnless( bf_y.bits == 7 )

        mv_z = self.global_ns.variable( 'z' )        
        self.failUnless( mv_z.bits == None )
        
    def test2( self ):
        pass

def create_suite():
    suite = unittest.TestSuite()        
    suite.addTest( unittest.makeSuite(tester_t))
    return suite

def run_suite():
    unittest.TextTestRunner(verbosity=2).run( create_suite() )

if __name__ == "__main__":
    run_suite()