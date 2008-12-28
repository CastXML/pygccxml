# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import os
import sys
import unittest
import autoconfig
import parser_test_case

import pprint
from pygccxml import msvc
from pygccxml import utils
from pygccxml import parser
from pygccxml import declarations

print msvc.undecorate_blob( '?make_flatten@algorithms@reflection@engine_objects@@YAXAEBVinstance_info_t@23@V?$back_insert_iterator@V?$vector@Vinstance_info_t@reflection@engine_objects@@V?$allocator@Vinstance_info_t@reflection@engine_objects@@@std@@@std@@@std@@@Z' )

class tester_t( parser_test_case.parser_test_case_t ):

    global_ns = None

    known_issues = set([
        #pointer to functions
        'void (** myclass_t::get_do_smth(void))(std::auto_ptr<number_t> &)'
        , 'void myclass_t::set_do_smth(void (**)(std::auto_ptr<number_t> &))'
        # array as function argument
        , 'int FA10_i_i(int * const)'
    ])
    if 'msvc71' == utils.native_compiler.get_gccxml_compiler():
        known_issues.add( 'std::auto_ptr<number_t> & std::auto_ptr<number_t>::operator=(std::auto_ptr_ref<number_t>)' )

    def __init__(self, *args ):
        parser_test_case.parser_test_case_t.__init__( self, *args )
        self.header = r'msvc\mydll.h'

    def setUp(self):
        if not tester_t.global_ns:
            decls = parser.parse( [self.header], self.config )
            tester_t.global_ns = declarations.get_global_namespace( decls )
            tester_t.global_ns.init_optimizer()

    def is_included( self, decl ):
        if not isinstance( decl, ( declarations.calldef_t, declarations.variable_t) ):
            return False
        for suffix in [ self.header, 'memory' ]:
            if decl.location.file_name.endswith( suffix ):
                return True
        else:
            return False

    def __tester_impl( self, fname ):
        symbols = msvc.exported_symbols.load_from_file( fname )
        self.failUnless( 'identity' in symbols )

        undecorated_blob_names = set()
        for blob in symbols.iterkeys():
            undname = msvc.undecorate_blob( blob )
            if "`" in undname:
                continue
            undecorated_blob_names.add( undname )

        undecorated_decl_names = set()
        for f in self.global_ns.decls(self.is_included):
            undecorated_decl_names.add( msvc.undecorate_decl( f ) )

        issuperset = undecorated_decl_names.issuperset( undecorated_blob_names )
        if not issuperset:
            common = undecorated_decl_names.intersection( undecorated_blob_names )

            undecorated_decl_names.difference_update(common)
            undecorated_blob_names.difference_update(common)
            if not self.known_issues.issubset( undecorated_blob_names ):
                undecorated_blob_names.difference_update( self.known_issues )
                msg = [ "undecorate_decl - failed" ]
                msg.append( "undecorated_decl_names :" )
                for i in undecorated_decl_names:
                    msg.append( '\t==>%s<==' % i )
                msg.append( "undecorated_blob_names :" )
                for i in undecorated_blob_names:
                    msg.append( '\t==>%s<==' % i )

                self.fail( os.linesep.join(msg) )

    def test_map_file( self ):
        map_file = os.path.join( autoconfig.data_directory, 'msvc', 'release', 'mydll.map' )
        self.__tester_impl( map_file )

    def test_dll_file( self ):
        dll_file = os.path.join( autoconfig.data_directory, 'msvc', 'release', 'mydll.dll' )
        self.__tester_impl( dll_file )

def create_suite():
    suite = unittest.TestSuite()
    if 'win' in sys.platform:
        suite.addTest( unittest.makeSuite(tester_t))
    return suite

def run_suite():
    unittest.TextTestRunner(verbosity=2).run( create_suite() )

if __name__ == "__main__":
    run_suite()
