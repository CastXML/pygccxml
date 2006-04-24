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
    COMPILATION_MODE = COMPILATION_MODE.ALL_AT_ONCE
    def __init__(self, *args ):
        parser_test_case.parser_test_case_t.__init__( self, *args )
        self.header = os.path.join( autoconfig.data_directory, 'declarations_calldef.hpp' )
        self.template = """
        //test generated declaration string using gcc(xml) compiler
        #include "declarations_calldef.hpp"
        void test_generated_decl_string( %s );
        """

    def test_member_function(self):
        declarations = parse( [self.header], self.config )
        member_inline_call = find_declaration( declarations, type=member_function_t, name='member_inline_call' )
        self.failUnless( member_inline_call, "unable to find 'member_inline_call' function" )
        decls = parse_string( self.template % member_inline_call.decl_string, self.config )
        self.failUnless( decls, "Created decl_string for member function containes mistake" )

    def test_free_function(self):
        declarations = parse( [self.header], self.config )
        return_default_args = find_declaration( declarations, type=free_function_t, name='return_default_args' )
        self.failUnless( return_default_args, "unable to find 'return_default_args' function" )
        decls = parse_string( self.template % return_default_args.decl_string, self.config )
        self.failUnless( decls, "Created decl_string for global function containes mistake" )

def create_suite():
    suite = unittest.TestSuite()        
    suite.addTest( unittest.makeSuite(tester_t))
    return suite

def run_suite():
    unittest.TextTestRunner(verbosity=2).run( create_suite() )

if __name__ == "__main__":
    run_suite()
