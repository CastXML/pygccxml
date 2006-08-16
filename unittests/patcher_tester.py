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
    
    decls = None
    
    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.__decls = None
        
    def setUp( self ):
        if tester_t.decls is None:
            reader = parser.source_reader_t( self.config )
            tester_t.decls = reader.read_file( 'patcher.hpp' )
        self.__decls = tester_t.decls

    def test_enum_patcher(self):
        fix_enum = declarations.find_declaration( self.__decls, type=declarations.free_function_t, name='fix_enum' )
        self.failUnless( fix_enum, "Free function fix_enum has not been found." )
        self.failUnless( fix_enum.arguments[0].default_value == '::ns1::ns2::apple' )

        #double_call = declarations.find_declaration( decls, type=declarations.free_function_t, name='double_call' )

    def test_numeric_patcher(self):
        fix_numeric = declarations.find_declaration( self.__decls, type=declarations.free_function_t, name='fix_numeric' )
        self.failUnless( fix_numeric, "Free function fix_numeric has not been found." )
        self.failUnless( fix_numeric.arguments[0].default_value == u"0xffffffffffffffff" )

    def test_unnamed_enum_patcher(self):
        fix_unnamed = declarations.find_declaration( self.__decls, type=declarations.free_function_t, name='fix_unnamed' )
        self.failUnless( fix_unnamed, "Free function fix_unnamed has not been found." )
        self.failUnless( fix_unnamed.arguments[0].default_value == u"int(::fx::unnamed)" )

    def test_function_call_patcher(self):
        fix_function_call = declarations.find_declaration( self.__decls, type=declarations.free_function_t, name='fix_function_call' )
        self.failUnless( fix_function_call, "Free function fix_function_call has not been found." )
        self.failUnless( fix_function_call.arguments[0].default_value == u"function_call::calc( 1, 2, 3 )" )

    def test_fundamental_patcher(self):
        fcall = declarations.find_declaration( self.__decls, type=declarations.free_function_t, name='fix_fundamental' )
        self.failUnless( fcall, "Free function fix_function_call has not been found." )
        self.failUnless( fcall.arguments[0].default_value == u"(unsigned int)(::fundamental::eggs)" )

    def test_constructor_patcher(self):
        typedef__func = declarations.find_declaration( self.__decls, type=declarations.free_function_t, name='typedef__func' )
        self.failUnless( typedef__func, "Free function typedef__func has not been found." )
        self.failUnless( typedef__func.arguments[0].default_value == u"::typedef_::alias( )" )

def create_suite():
    suite = unittest.TestSuite()        
    suite.addTest( unittest.makeSuite(tester_t))    
    return suite

def run_suite():
    unittest.TextTestRunner(verbosity=2).run( create_suite() )

if __name__ == "__main__":
    run_suite()