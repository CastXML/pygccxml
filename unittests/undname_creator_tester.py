# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import os
import sys
import unittest
import autoconfig
import parser_test_case

import subprocess
from pygccxml import binary_parsers
from pygccxml import utils
from pygccxml import parser
from pygccxml import declarations

class tester_t( parser_test_case.parser_test_case_t ):

    global_ns = None

    known_issues = set([
        # array as function argument: 'int FA10_i_i(int * const)'
          '?FA10_i_i@@YAHQAH@Z'
        #pointer to function: 'void myclass_t::set_do_smth(void (**)(std::auto_ptr<number_t> &))'
        , '?set_do_smth@myclass_t@@QAEXPAP6AXAAV?$auto_ptr@Vnumber_t@@@std@@@Z@Z'
        #pointer to functions: 'void (** myclass_t::get_do_smth(void))(std::auto_ptr<number_t> &)'
        , '?get_do_smth@myclass_t@@QAEPAP6AXAAV?$auto_ptr@Vnumber_t@@@std@@@ZXZ'
    ])
    if 'msvc71' == utils.native_compiler.get_gccxml_compiler():
        #missing reference in argument - compiler issue 'std::auto_ptr<number_t> & std::auto_ptr<number_t>::operator=(std::auto_ptr_ref<number_t>)'
        known_issues.add( '??4?$auto_ptr@Vnumber_t@@@std@@QAEAAV01@U?$auto_ptr_ref@Vnumber_t@@@1@@Z' )

    def __init__(self, *args ):
        parser_test_case.parser_test_case_t.__init__( self, *args )
        self.binary_parsers_dir = os.path.join( autoconfig.data_directory, 'binary_parsers' )
        self.header = os.path.join( self.binary_parsers_dir, r'mydll.h' )
        self.map_file = os.path.join( self.binary_parsers_dir, 'binaries', 'mydll.map' )
        self.dll_file = os.path.join( self.binary_parsers_dir, 'binaries', 'mydll.dll' )

    def setUp(self):
        if not tester_t.global_ns:
            decls = parser.parse( [self.header], self.config )
            tester_t.global_ns = declarations.get_global_namespace( decls )
            tester_t.global_ns.init_optimizer()


            process = subprocess.Popen( args='scons msvc_compiler=%s' % autoconfig.compiler
                                        , shell=True
                                        , stdin=subprocess.PIPE
                                        , stdout=subprocess.PIPE
                                        , stderr=subprocess.STDOUT
                                        , cwd=self.binary_parsers_dir )
            process.stdin.close()

            while process.poll() is None:
                line = process.stdout.readline()
                print line.rstrip()
            for line in process.stdout.readlines():
                print line.rstrip()
            if process.returncode:
                raise RuntimeError( "unable to compile binary parser module. See output for the errors." )

    def is_included( self, decl ):
        if not isinstance( decl, ( declarations.calldef_t, declarations.variable_t) ):
            return False
        for suffix in [ self.header, 'memory' ]:
            if decl.location.file_name.endswith( suffix ):
                return True
        else:
            return False

    def __tester_impl( self, fname ):
        symbols, parser = binary_parsers.merge_information( self.global_ns, fname, runs_under_unittest=True )
        self.failUnless( 'identity' in symbols )

        blob_names = set()
        for blob in parser.loaded_symbols:
            if isinstance( blob, tuple ):
                blob = blob[0]
            undname = binary_parsers.undecorate_blob( blob )
            if "`" in undname:
                continue
            blob_names.add( blob )

        decl_blob_names = set( symbols.keys() )

        issuperset = decl_blob_names.issuperset( blob_names )
        if not issuperset:
            common = decl_blob_names.intersection( blob_names )

            decl_blob_names.difference_update(common)
            blob_names.difference_update(common)
            if not self.known_issues.issubset( blob_names ):
                blob_names.difference_update( self.known_issues )
                msg = [ "undecorate_decl - failed" ]
                msg.append( "decl_blob_names :" )
                for i in decl_blob_names:
                    msg.append( '\t==>%s<==' % i )
                msg.append( "blob_names :" )
                for i in blob_names:
                    msg.append( '\t==>%s<==' % i )

                self.fail( os.linesep.join(msg) )

    def test_map_file( self ):
        self.__tester_impl( self.map_file )

    def test_dll_file( self ):
        self.__tester_impl( self.dll_file )

    def test_compare_parsers( self ):
        dsymbols, dparser = binary_parsers.merge_information( self.global_ns, self.dll_file, runs_under_unittest=True )
        msymbols, mparser = binary_parsers.merge_information( self.global_ns, self.map_file, runs_under_unittest=True )

        self.failUnless( len( dparser.loaded_symbols ) == len( mparser.loaded_symbols ) )

        was_error = False
        for blob, decl in dsymbols.iteritems():
            if blob not in msymbols:
                was_error = True
                print '\n%s could not be found in map file loaded symbols' % binary_parsers.undecorate_blob( blob )
                #~ self.failUnless( blob in msymbols, binary_parsers.undecorate_blob( blob ) )
            else:
                mdecl = msymbols[ blob ]
                self.failUnless( mdecl is decl )
        self.failUnless( was_error == False )

def create_suite():
    suite = unittest.TestSuite()
    if 'win' in sys.platform:
        suite.addTest( unittest.makeSuite(tester_t))
    return suite

def run_suite():
    unittest.TextTestRunner(verbosity=2).run( create_suite() )

if __name__ == "__main__":
    run_suite()
