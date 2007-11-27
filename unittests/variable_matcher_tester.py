# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import os
import unittest
import autoconfig
import parser_test_case

from pygccxml import utils
from pygccxml import parser
from pygccxml import declarations

class tester_1_t( parser_test_case.parser_test_case_t ):
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    declarations  = None
    def __init__(self, *args ):
        parser_test_case.parser_test_case_t.__init__( self, *args )
        self.header = 'bit_fields.hpp'
        self.declarations = None

    def setUp(self):
        if not self.declarations:
            self.declarations = parser.parse( [self.header], self.config )

    def test( self ):
        criteria = declarations.variable_matcher_t( name='x', type='unsigned int' )
        x = declarations.matcher.get_single( criteria, self.declarations )

        self.failUnless( str(criteria) == '(decl type==variable_t) and (name==x) and (value type==unsigned int)' )

        criteria = declarations.variable_matcher_t(
            name='::bit_fields::fields_t::x'
            , type=declarations.unsigned_int_t()
            , header_dir=os.path.dirname(x.location.file_name)
            , header_file=x.location.file_name)

        x = declarations.matcher.get_single( criteria, self.declarations )
        self.failUnless( x, "Variable was not found." )

        self.failUnless( 'public' == x.access_type )

class tester_2_t( parser_test_case.parser_test_case_t ):
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    global_ns = None
    def __init__(self, *args ):
        parser_test_case.parser_test_case_t.__init__( self, *args )
        self.header = 'vector_traits.hpp'
        self.global_ns = None

    def setUp(self):
        if not self.global_ns:
            self.global_ns = declarations.get_global_namespace( parser.parse( [self.header], self.config ) )

    def test_no_defaults( self ):
        vectors = self.global_ns.decls( lambda decl: 'vector<' in decl.name )
        self.global_ns.decl( 'vector< _0_ >' )
        self.global_ns.class_( 'vector< std::vector< int > >' )
        self.global_ns.class_( 'vector< std::string >' )
        self.global_ns.decl( 'vector< const int >' )
    
def create_suite():
    suite = unittest.TestSuite()
    suite.addTest( unittest.makeSuite(tester_1_t))
    suite.addTest( unittest.makeSuite(tester_2_t))
    return suite

def run_suite():
    unittest.TextTestRunner(verbosity=2).run( create_suite() )

if __name__ == "__main__":
    run_suite()
