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
    def __init__(self, *args ):
        parser_test_case.parser_test_case_t.__init__( self, *args )
        self.header = 'demangled.hpp'
        self.global_ns = None
        
    def setUp(self):
        if not self.global_ns:
            decls = parser.parse( [self.header], self.config )
            self.global_ns = declarations.get_global_namespace( decls )
            self.global_ns.init_optimizer()
            
    def test( self ):                
        demangled = self.global_ns.namespace( 'demangled' )
        cls = demangled.class_( 'item_t<3740067437l, 11l, 2147483648l>' )
        self.failUnless( cls._name == 'item_t<0deece66d,11,080000000>' )
        
def create_suite():
    suite = unittest.TestSuite()        
    suite.addTest( unittest.makeSuite(tester_t))
    return suite

def run_suite():
    unittest.TextTestRunner(verbosity=2).run( create_suite() )

if __name__ == "__main__":
    run_suite()