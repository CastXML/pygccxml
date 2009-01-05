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
        self.header = 'const_volatile_arg.hpp'
        self.global_ns = None

    def setUp(self):
        if not tester_t.global_ns:
            decls = parser.parse( [self.header], self.config )
            tester_t.global_ns = declarations.get_global_namespace( decls )
            tester_t.global_ns.init_optimizer()
        self.global_ns = tester_t.global_ns

    def test( self ):
        f = self.global_ns.free_fun( 'pygccxml_bug' )
        t = f.arguments[0].type
        self.failUnless( isinstance( t, declarations.pointer_t ) )
        self.failUnless( isinstance( t.base, declarations.volatile_t ) )
        self.failUnless( isinstance( t.base.base, declarations.const_t ) )
        self.failUnless( declarations.is_integral( t.base.base.base ) )


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest( unittest.makeSuite(tester_t))
    return suite

def run_suite():
    unittest.TextTestRunner(verbosity=2).run( create_suite() )

if __name__ == "__main__":
    run_suite()
