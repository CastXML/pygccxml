# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import sys
import pprint
import unittest
import autoconfig
import parser_test_case

import pygccxml
from pygccxml.utils import *
from pygccxml.parser import *
from pygccxml.declarations import *


class declarations_t( parser_test_case.parser_test_case_t ):
    def __init__(self, *args ):
        parser_test_case.parser_test_case_t.__init__( self, *args )
        self.global_ns = None

    def test_enumeration_t(self):
        enum = self.global_ns.enum( 'ENumbers' )
        expected_values = zip( [ 'e%d' % index for index in range(10) ]
                                     , [ index for index in range(10) ] )
        self.failUnless( expected_values == enum.values
                         , "expected enum values ( '%s' ) and existings ( '%s' ) are different" % \
                            ( pprint.pformat( expected_values ), pprint.pformat( enum.values ) ) )

    def test_namespace(self):
        pass #tested in core_tester

    def test_types(self):
        pass #tested in core_tester

    def test_variables(self):
        variables = self.global_ns.namespace( 'variables' )
        initialized = self.global_ns.variable( name='initialized' )

        expected_value = None
        if '0.9' in initialized.compiler:
            expected_value = '10122004ul'
        else:
            expected_value = '10122004'

        self.failUnless( initialized.value == expected_value
                         , "there is a difference between expected value( %s ) and real value(%s) of 'initialized' variable" \
                           % ( expected_value, initialized.value ) )
        self._test_type_composition( initialized.type, const_t, long_unsigned_int_t )

        static_var = initialized = self.global_ns.variable( name='static_var' )
        self.failUnless( static_var.type_qualifiers.has_static
                         , "static_var must have static type qualifier" )
        self.failUnless( not static_var.type_qualifiers.has_mutable
                         , "static_var must not have mutable type qualifier" )

        if 'PDB' in self.global_ns.compiler:
            return #TODO find out work around

        m_mutable = initialized = self.global_ns.variable( name='m_mutable' )
        self.failUnless( not m_mutable.type_qualifiers.has_static
                         , "m_mutable must not have static type qualifier" )
        ##TODO: "There is bug in GCCXML: doesn't write mutable qualifier."
        #self.failUnless( m_mutable.type_qualifiers.has_mutable
        #                 , "static_var must have mutable type qualifier" )

    def test_calldef_free_functions(self):
        ns = self.global_ns.namespace( 'calldef' )

        no_return_no_args = ns.free_function( 'no_return_no_args' )
        self._test_calldef_return_type( no_return_no_args, void_t )
        self.failUnless( no_return_no_args.has_extern, "function 'no_return_no_args' should have extern qualifier" )

        return_no_args = ns.free_function( 'return_no_args' )
        self._test_calldef_return_type( return_no_args, int_t )
        #from now there is no need to check return type.
        no_return_1_arg = ns.free_function( name='no_return_1_arg' )
        self.failUnless( no_return_1_arg, "unable to find 'no_return_1_arg' function" )
        self.failUnless( no_return_1_arg.arguments[0].name in [ 'arg', 'arg0' ] )
        self._test_calldef_args( no_return_1_arg, [ argument_t( name=no_return_1_arg.arguments[0].name, type=int_t() )] )

        return_default_args = ns.free_function( 'return_default_args' )
        self.failUnless( return_default_args.arguments[0].name in [ 'arg', 'arg0' ] )
        self.failUnless( return_default_args.arguments[1].name in [ 'arg1', 'flag' ] )
        self._test_calldef_args( return_default_args
                                 , [ argument_t( name=return_default_args.arguments[0].name
                                                 , type=int_t(), default_value='1' )
                                     , argument_t( name=return_default_args.arguments[1].name
                                                   , type=bool_t(), default_value='false' ) ] )
        self._test_calldef_exceptions( return_default_args, [] )

        calldef_with_throw = ns.free_function( 'calldef_with_throw' )
        self.failUnless( calldef_with_throw, "unable to find 'calldef_with_throw' function" )
        self._test_calldef_exceptions( calldef_with_throw, ['some_exception_t', 'other_exception_t'] )
        #from now there is no need to check exception specification

    def test_calldef_member_functions(self):
        struct_calldefs = self.global_ns.class_( 'calldefs_t' )

        member_inline_call = struct_calldefs.member_function( 'member_inline_call' )
        self._test_calldef_args( member_inline_call, [ argument_t( name='i', type=int_t() )] )

        member_const_call = struct_calldefs.member_function( 'member_const_call' )
        self.failUnless( member_const_call.has_const, "function 'member_const_call' should have const qualifier" )
        self.failUnless( member_const_call.virtuality == VIRTUALITY_TYPES.NOT_VIRTUAL
                         , "function 'member_const_call' should be non virtual function" )

        member_virtual_call = struct_calldefs.member_function( name='member_virtual_call' )
        self.failUnless( member_virtual_call.virtuality == VIRTUALITY_TYPES.VIRTUAL
                         , "function 'member_virtual_call' should be virtual function" )

        member_pure_virtual_call = struct_calldefs.member_function( 'member_pure_virtual_call' )
        self.failUnless( member_pure_virtual_call.virtuality == VIRTUALITY_TYPES.PURE_VIRTUAL
                         , "function 'member_pure_virtual_call' should be pure virtual function" )

        static_call = struct_calldefs.member_function( 'static_call' )
        self.failUnless( static_call.has_static, "function 'static_call' should have static qualifier" )
        #from now we there is no need to check static qualifier

    def test_constructors_destructors(self):
        struct_calldefs = self.global_ns.class_( 'calldefs_t' )

        destructor = struct_calldefs.calldef( '~calldefs_t' )
        self._test_calldef_args( destructor, [] )
        self._test_calldef_return_type( destructor, None.__class__)

        #well, now we have a few functions ( constructors ) with the same name, there is no easy way
        #to find the desired one. Well in my case I have only 4 constructors
        #1. from char
        #2. from (int,double)
        #3. default
        #4. copy constructor
        constructor_found = struct_calldefs.constructors( 'calldefs_t' )
        self.failUnless( len( constructor_found ) == 4
                         , "struct 'calldefs_t' has 4 constructors, pygccxml parser reports only about %d." \
                           % len( constructor_found ) )
        self.failUnless( 1 == len( filter( lambda constructor: constructor.is_copy_constructor, constructor_found ) )
                         , "copy constructor has not been found" )
        #there is nothing to check about constructors - I know the implementation of parser
        #In this case it doesn't different from any other function

    def test_operator_symbol(self):
        calldefs_operators = ['=', '==' ]
        calldefs_cast_operators = ['char *', 'double']
        struct_calldefs = self.global_ns.class_( 'calldefs_t')
        self.failUnless( struct_calldefs, "unable to find struct 'calldefs_t'")
        for decl in struct_calldefs.declarations:
            if not isinstance( decl, operator_t ):
                continue
            if not isinstance( decl, casting_operator_t ):
                self.failUnless( decl.symbol in calldefs_operators, "unable to find operator symbol for operator '%s'" % decl.decl_string )
            else:
                self.failUnless( decl.return_type.decl_string in calldefs_cast_operators, "unable to find operator symbol for operator '%s'" % decl.decl_string )

    def test_ellipsis( self ):
        ns = self.global_ns.ns( 'ellipsis_tester' )
        do_smth = ns.mem_fun( 'do_smth' )
        for a in do_smth.arguments:
            print str(a)
        self.failUnless( do_smth.has_ellipsis )
        do_smth_else = ns.free_fun( 'do_smth_else' )
        self.failUnless( do_smth_else.has_ellipsis )

class gccxml_declarations_t( declarations_t ):
    global_ns = None
    def __init__(self, *args ):
        declarations_t.__init__( self, *args )
        self.test_files = [ 'declarations_enums.hpp'
                            , 'declarations_variables.hpp'
                            , 'declarations_calldef.hpp'
        ]
        self.global_ns = None

    def setUp(self):
        if not gccxml_declarations_t.global_ns:
            decls = parse( self.test_files, self.config, self.COMPILATION_MODE )
            gccxml_declarations_t.global_ns = get_global_namespace( decls )
        if not self.global_ns:
            self.global_ns = gccxml_declarations_t.global_ns

class all_at_once_tester_t( gccxml_declarations_t ):
    COMPILATION_MODE = COMPILATION_MODE.ALL_AT_ONCE
    def __init__(self, *args):
        gccxml_declarations_t.__init__(self, *args)

class file_by_file_tester_t( gccxml_declarations_t ):
    COMPILATION_MODE = COMPILATION_MODE.FILE_BY_FILE
    def __init__(self, *args):
        gccxml_declarations_t.__init__(self, *args)

class pdb_based_tester_t( declarations_t ):
    def __init__(self, *args ):
        declarations_t.__init__( self, *args )
        self.global_ns = autoconfig.get_pdb_global_ns()

def create_suite():
    suite = unittest.TestSuite()
    suite.addTest( unittest.makeSuite(file_by_file_tester_t))
    suite.addTest( unittest.makeSuite(all_at_once_tester_t))
    if sys.platform == 'win32' and autoconfig.get_pdb_global_ns():
        suite.addTest( unittest.makeSuite(pdb_based_tester_t))

    return suite

def run_suite():
    unittest.TextTestRunner(verbosity=2).run( create_suite() )

if __name__ == "__main__":
    run_suite()
