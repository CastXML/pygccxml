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

class tester_t( parser_test_case.parser_test_case_t ):
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE    
    def __init__(self, *args ):
        parser_test_case.parser_test_case_t.__init__( self, *args )
        self.header = 'declarations_calldef.hpp'
        self.declarations = None
        
    def setUp(self):
        if not self.declarations:
            self.declarations = parser.parse( [self.header], self.config )
            
    def test_regex( self ):       
        criteria = declarations.regex_matcher_t( 'oper.*'
                                                 ,  lambda decl: decl.name )
        operators = declarations.matcher.find( criteria, self.declarations )
        self.failUnless( 6 == len(operators) )

    def test_access_type( self ):       
        criteria = declarations.access_type_matcher_t( declarations.ACCESS_TYPES.PUBLIC )
        public_members = declarations.matcher.find( criteria, self.declarations )
        if '0.9' in public_members[0].compiler:
            #2 empty classes, this compiler doesn't generate constructor and copy constructor
            self.failUnless( 16 == len( public_members ) ) 
        else:
            self.failUnless( 20 == len( public_members ) )
        
    def test_or_matcher( self ):
        criteria1 = declarations.regex_matcher_t( 'oper.*'
                                                   , lambda decl: decl.name )
        criteria2 = declarations.access_type_matcher_t( declarations.ACCESS_TYPES.PUBLIC )
        found = declarations.matcher.find( criteria1 | criteria2, self.declarations )

        if '0.9' in found[0].compiler:
            #2 empty classes, this compiler doesn't generate constructor and copy constructor
            self.failUnless( 15 <= len( found ) <= 21) 
        else:
            self.failUnless( 19 <= len( found ) <= 25)

    def test_and_matcher( self ):
        criteria1 = declarations.regex_matcher_t( 'oper.*'
                                                   , lambda decl: decl.name )
        criteria2 = declarations.access_type_matcher_t( declarations.ACCESS_TYPES.PUBLIC )
        found = declarations.matcher.find( criteria1 & criteria2, self.declarations )
        self.failUnless( len( found ) <= 6 )

    def test_not_matcher( self ):
        criteria1 = declarations.regex_matcher_t( 'oper.*'
                                                   , lambda decl: decl.name )
        found = declarations.matcher.find( ~( ~criteria1 ), self.declarations )
        self.failUnless( len( found ) == 6 )

def create_suite():
    suite = unittest.TestSuite()        
    suite.addTest( unittest.makeSuite(tester_t))
    return suite

def run_suite():
    unittest.TextTestRunner(verbosity=2).run( create_suite() )

if __name__ == "__main__":
    run_suite()
