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

class tester_impl_t( parser_test_case.parser_test_case_t ):

    def __init__(self, architecture, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.architecture = architecture
        self.global_ns = None
        
    def setUp( self ):
        reader = parser.source_reader_t( self.config )
        if 32 == self.architecture:
            self.global_ns = reader.read_file( 'patcher.hpp' )[0].top_parent
        else:
            original_get_architecture = utils.get_architecture
            utils.get_architecture = lambda: 64
            self.global_ns = reader.read_xml_file( 
                    os.path.join( autoconfig.data_directory, 'patcher_tester_64bit.xml' ) )[0].top_parent
            utils.get_architecture = original_get_architecture
    
    def test_enum_patcher(self):
        fix_enum = self.global_ns.free_fun( 'fix_enum' )
        self.failUnless( fix_enum.arguments[0].default_value == '::ns1::ns2::apple' )

        #double_call = declarations.find_declaration( decls, type=declarations.free_function_t, name='double_call' )

    def test_numeric_patcher(self):
        fix_numeric = self.global_ns.free_fun( 'fix_numeric' )
        if 32 == self.architecture:
            self.failUnless( fix_numeric.arguments[0].default_value == u"0xffffffffffffffff" )
        else: 
            self.failUnless( fix_numeric.arguments[0].default_value == u"0ffffffff" )
            
    def test_unnamed_enum_patcher(self):
        fix_unnamed = self.global_ns.free_fun( 'fix_unnamed' )
        self.failUnless( fix_unnamed.arguments[0].default_value == u"int(::fx::unnamed)" )

    def test_function_call_patcher(self):
        fix_function_call = self.global_ns.free_fun( 'fix_function_call' )
        self.failUnless( fix_function_call.arguments[0].default_value == u"function_call::calc( 1, 2, 3 )" )

    def test_fundamental_patcher(self):
        fcall = self.global_ns.free_fun( 'fix_fundamental' )
        self.failUnless( fcall.arguments[0].default_value == u"(unsigned int)(::fundamental::eggs)" )

    def test_constructor_patcher(self):
        typedef__func = self.global_ns.free_fun( 'typedef__func' )
        self.failUnless( typedef__func.arguments[0].default_value == u"::typedef_::alias( )" )
        if 32 == self.architecture:
            clone_tree = self.global_ns.free_fun( 'clone_tree' )
            default_value = 'vector<std::basic_string<char, std::char_traits<char>, std::allocator<char> >,std::allocator<std::basic_string<char, std::char_traits<char>, std::allocator<char> > > >()'
            self.failUnless( default_value == clone_tree.arguments[0].default_value )
        
class tester_32_t( tester_impl_t ):
    def __init__(self, *args):
        tester_impl_t.__init__(self, 32, *args)

class tester_64_t( tester_impl_t ):
    def __init__(self, *args):
        tester_impl_t.__init__(self, 64, *args)

def create_suite():
    suite = unittest.TestSuite()        
    suite.addTest( unittest.makeSuite(tester_32_t))    
    suite.addTest( unittest.makeSuite(tester_64_t))    
    return suite

def run_suite():
    unittest.TextTestRunner(verbosity=2).run( create_suite() )

if __name__ == "__main__":
    run_suite()
