# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import os
import sys
import pprint
import unittest
import tempfile
import autoconfig
import parser_test_case
from pprint import pformat

import pygccxml
from pygccxml.utils import *
from pygccxml.parser import *
from pygccxml.declarations import *

def is_sub_path( root, some_path ):
    root = normalize_path( root )
    some_path = normalize_path( some_path )
    return some_path.startswith( root )
    

class core_t( parser_test_case.parser_test_case_t ):
    """Tests core algorithms of GCC-XML and GCC-XML file reader.
    Those most white-box testing.
    """
    global_ns = None
    def __init__(self, *args ):
        parser_test_case.parser_test_case_t.__init__( self, *args )
        self.global_ns = None

    def test_top_parent(self):
        enum = self.global_ns.enum( '::ns::ns32::E33' )
        self.failUnless( self.global_ns is enum.top_parent )

    #tests namespaces join functionality. described in gccxml.py
    def test_nss_join(self):
        #list of all namespaces
        nss = [ '::ns', '::ns::ns12', '::ns::ns22', '::ns::ns32' ]
        #list of all namespaces that have unnamed namespace
        unnamed_nss = nss[1:]
        #list of all enums [0:2] [3:5] [6:8] - has same parent
        enums = [ '::E11', '::E21', '::E31'
                  , '::ns::E12', '::ns::E22', '::ns::E32'
                  , '::ns::ns12::E13', '::ns::ns22::E23', '::ns::ns32::E33' ]

        for ns in nss:
            self.global_ns.namespace( ns )

        for enum in enums:
            self.global_ns.enum( enum )

        ns = self.global_ns.namespace( nss[0] )
        ns12 = self.global_ns.namespace( nss[1] )
        ns22 = self.global_ns.namespace( nss[2] )
        ns32 = self.global_ns.namespace( nss[3] )
        self.failUnless( ns and ( ns is ns12.parent is ns22.parent is ns32.parent )
                         , 'There are 2 or more instances of ns namespace.' )

        E11 = self.global_ns.enum( enums[0] )
        E21 = self.global_ns.enum( enums[1] )
        E31 = self.global_ns.enum( enums[2] )
        self.failUnless( E11.parent is E21.parent is E31.parent
                         , 'There are 2 or more instances of global namespace.' )

        nsE12 = self.global_ns.enum( enums[3] )
        nsE23 = self.global_ns.enum( enums[4] )
        nsE33 = self.global_ns.enum( enums[5] )
        self.failUnless( ns and ( ns is nsE12.parent is nsE23.parent is nsE33.parent )
                         , 'There are 2 or more instances of ns namespace.' )

    def _test_ns_membership(self, ns, enum_name ):
        unnamed_enum = ns.enum( lambda d: d.name == '' \
                                          and is_sub_path( autoconfig.data_directory, d.location.file_name )
                                , recursive=False )
        self.failUnless( unnamed_enum in ns.declarations
                         , "namespace '%s' does not contains unnamed enum." % ns.name )

        enum = ns.enum( enum_name, recursive=False )

        self.failUnless( enum in ns.declarations
                         , "namespace '%s' does not contains enum '%s'" % ( ns.name, enum.name ) )

        self.failUnless( unnamed_enum.parent is ns
                         , "unnamed enum belong to namespace '%s' but this namespace is not it's parent." % ns.name )

        self.failUnless( enum.parent is ns
                         , "enum '%s' belong to namespace '%s' but this namespace is not it's parent." % ( enum.name, ns.name ) )

    def _test_class_membership( self, class_inst, enum_name, access ):
        #getting enum through get_members function
        if class_inst.compiler == compilers.MSVC_PDB_9:
            nested_enum1 = class_inst.enum( name=enum_name )
        else:
            nested_enum1 = class_inst.enum( name=enum_name, function=access_type_matcher_t( access ) )

        #getting enum through declarations property
        nested_enum2 = class_inst.enum( enum_name )

        #it shoud be same object
        self.failUnless( nested_enum1 is nested_enum2
                         , "enum accessed through access definition('%s') and through declarations('%s') are different enums or instances."  \
                           %( nested_enum1.name, nested_enum2.name ) )

        #check whether we meaning same class instance
        self.failUnless( class_inst is nested_enum1.parent is nested_enum2.parent
                         , 'There are 2 or more instances of ns namespace.' )

    #test gccxml_file_reader_t._update_membership algorithm
    def test_membership(self):
        core_membership = self.global_ns.namespace( 'membership' )
        self._test_ns_membership( self.global_ns, 'EGlobal' )
        self._test_ns_membership( core_membership.namespace('enums_ns'), 'EWithin' )
        self._test_ns_membership( core_membership.namespace( '' ), 'EWithinUnnamed' )
        class_nested_enums = core_membership.class_( 'class_for_nested_enums_t' )
        self._test_class_membership( class_nested_enums, 'ENestedPublic', ACCESS_TYPES.PUBLIC )
        self._test_class_membership( class_nested_enums, 'ENestedProtected', ACCESS_TYPES.PROTECTED )
        self._test_class_membership( class_nested_enums, 'ENestedPrivate', ACCESS_TYPES.PRIVATE )

    def test_mangled(self):
        std = self.global_ns.namespace( 'std' )
        self.failUnless( std, 'std namespace has not been found' )
        self.failUnless( std.mangled, 'mangled name of std namespace should be different from None' )

    def _test_is_based_and_derived(self, base, derived, access):
        dhi_v = hierarchy_info_t( derived, access, True )
        dhi_not_v = hierarchy_info_t( derived, access, False )
        self.failUnless( dhi_v in base.derived or dhi_not_v in base.derived
                         , "base class '%s' doesn't has derived class '%s'" %( base.name, derived.name ) )

        bhi_v = hierarchy_info_t( base, access, True )
        bhi_not_v = hierarchy_info_t( base, access, False )

        self.failUnless( bhi_v in derived.bases or bhi_not_v in derived.bases
                         , "derive class '%s' doesn't has base class '%s'" %( derived.name, base.name ) )

    def test_class_hierarchy(self):
        class_hierarchy = self.global_ns.namespace( 'class_hierarchy' )

        base = class_hierarchy.class_( 'base_t' )
        other_base = class_hierarchy.class_( 'other_base_t' )
        derived_public = class_hierarchy.class_( 'derived_public_t' )
        derived_protected = class_hierarchy.class_( 'derived_protected_t' )
        derived_private = class_hierarchy.class_( 'derived_private_t' )
        multi_derived = class_hierarchy.class_( 'multi_derived_t' )

        self._test_is_based_and_derived( base, derived_public, ACCESS_TYPES.PUBLIC )
        self._test_is_based_and_derived( base, derived_protected, ACCESS_TYPES.PROTECTED )
        self._test_is_based_and_derived( base, derived_private, ACCESS_TYPES.PRIVATE )
        self._test_is_based_and_derived( base, multi_derived, ACCESS_TYPES.PROTECTED )
        self._test_is_based_and_derived( other_base, multi_derived, ACCESS_TYPES.PRIVATE )
        self._test_is_based_and_derived( derived_private, multi_derived, ACCESS_TYPES.PRIVATE )

    def _test_is_same_bases(self, derived1, derived2 ):
        bases1 = set([ id(hierarchy_info.related_class) for hierarchy_info in derived1.bases ])
        bases2 = set([ id(hierarchy_info.related_class) for hierarchy_info in derived2.bases ])
        self.failUnless( bases1 == bases2
                         , "derived class '%s' and derived class '%s' has references to different instance of base classes " \
                           % ( derived1.name, derived2.name ) )

    def test_class_join(self):
        diamand_hierarchy = self.global_ns.namespace( 'diamand_hierarchy' )
        base = diamand_hierarchy.class_( 'base_t' )
        derived1 = diamand_hierarchy.class_( 'derived1_t' )
        derived2 = diamand_hierarchy.class_( 'derived2_t' )
        final_derived = diamand_hierarchy.class_( 'final_derived_t' )

        self._test_is_based_and_derived( base, derived1, ACCESS_TYPES.PUBLIC )
        self._test_is_based_and_derived( base, derived2, ACCESS_TYPES.PUBLIC )
        self._test_is_based_and_derived( derived1, final_derived, ACCESS_TYPES.PUBLIC )
        self._test_is_based_and_derived( derived2, final_derived, ACCESS_TYPES.PUBLIC )
        self._test_is_same_bases(derived1, derived2)

    def test_fundamental_types(self):
        #check whether all build in types could be constructed
        errors = []
        for fundamental_type_name, fundamental_type in FUNDAMENTAL_TYPES.iteritems():
            if 'complex' in fundamental_type_name:
                continue #I check this in an other tester
            if isinstance( fundamental_type, java_fundamental_t ):
                continue #I don't check this at all
            typedef_name = 'typedef_' + fundamental_type_name.replace( ' ', '_' )
            typedef = self.global_ns.decl( decl_type=typedef_t, name=typedef_name )
            self.failUnless( typedef, "unable to find typedef to build-in type '%s'" % fundamental_type_name )
            if typedef.type.decl_string != fundamental_type.decl_string:
                errors.append( "there is a difference between typedef base type name('%s') and expected one('%s')"
                               % (typedef.type.decl_string, fundamental_type.decl_string) )
        if self.global_ns.compiler != compilers.MSVC_PDB_9:
            self.failIf( errors, pprint.pformat( errors ) )
        else:
            self.failUnless( 5 == len( errors ), pprint.pformat( errors ) )

    def test_compound_types(self):
        typedef_inst = self.global_ns.decl( decl_type=typedef_t, name='typedef_const_int' )
        self._test_type_composition( typedef_inst.type, const_t, int_t )

        typedef_inst = self.global_ns.decl( decl_type=typedef_t, name='typedef_pointer_int' )
        self._test_type_composition( typedef_inst.type, pointer_t, int_t )

        typedef_inst = self.global_ns.decl( decl_type=typedef_t, name='typedef_reference_int' )
        self._test_type_composition( typedef_inst.type, reference_t, int_t )

        typedef_inst = self.global_ns.decl( decl_type=typedef_t, name='typedef_const_unsigned_int_const_pointer' )
        self._test_type_composition( typedef_inst.type, const_t, pointer_t )
        self._test_type_composition( typedef_inst.type.base, pointer_t, const_t )
        self._test_type_composition( typedef_inst.type.base.base, const_t, unsigned_int_t )

        typedef_inst = self.global_ns.decl( decl_type=typedef_t, name='typedef_volatile_int' )
        self._test_type_composition( typedef_inst.type, volatile_t, int_t )

        var_inst = self.global_ns.variable( 'array255' )
        self._test_type_composition( var_inst.type, array_t, int_t )


        typedef_inst = self.global_ns.decl( decl_type=typedef_t, name='typedef_EFavoriteDrinks' )
        self.failUnless( isinstance( typedef_inst.type, declarated_t )
                         , " typedef to enum should be 'declarated_t' instead of '%s'" % typedef_inst.type.__class__.__name__ )
        enum_declaration = self.global_ns.enum( 'EFavoriteDrinks' )
        self.failUnless( typedef_inst.type.declaration is enum_declaration
                         , "instance of declaration_t has reference to '%s' instead of '%s'" \
                           % ( typedef_inst.type.declaration.name, enum_declaration.name ) )

    def test_free_function_type(self):
        function_ptr = self.global_ns.decl( decl_type=typedef_t, name='function_ptr' )
        self._test_type_composition( function_ptr.type, pointer_t, free_function_type_t )
        function_type = function_ptr.type.base
        self.failUnless( isinstance( function_type.return_type, int_t )
                         , "return function type of typedef 'function_ptr' should be '%s' instead of '%s' " \
                           %( 'int_t', function_type.return_type.__class__.__name__ ) )
        self.failUnless( len( function_type.arguments_types ) == 2
                         , "number of arguments of function of typedef 'function_ptr' should be 2 instead of '%d' " \
                           % len( function_type.arguments_types ) )
        self.failUnless( isinstance( function_type.arguments_types[0], int_t )
                         , "first argument of function of typedef 'function_ptr' should be '%s' instead of '%s' " \
                           %( 'int_t', function_type.arguments_types[0].__class__.__name__ ) )
        self.failUnless( isinstance( function_type.arguments_types[1], double_t )
                         , "first argument of function of typedef 'function_ptr' should be '%s' instead of '%s' " \
                           %( 'double_t', function_type.arguments_types[0].__class__.__name__ ) )

    def test_member_function_type(self):
        function_ptr = self.global_ns.decl( decl_type=typedef_t, name='member_function_ptr_t')
        self._test_type_composition( function_ptr.type, pointer_t, member_function_type_t )

        function_type = function_ptr.type.base

        members_pointers = self.global_ns.class_( 'members_pointers_t' )
        self.failUnless( function_type.class_inst.declaration is members_pointers
                         , "member function type class should be '%s' instead of '%s'" \
                           % ( members_pointers.decl_string, function_type.class_inst.decl_string ) )

        self.failUnless( isinstance( function_type.return_type, int_t )
                         , "return function type of typedef 'member_function_ptr_t' should be '%s' instead of '%s' " \
                           %( 'int_t', function_type.return_type.__class__.__name__ ) )
        self.failUnless( len( function_type.arguments_types ) == 1
                         , "number of arguments of function of typedef 'member_function_ptr_t' should be 1 instead of '%d' " \
                           % len( function_type.arguments_types ) )
        self.failUnless( isinstance( function_type.arguments_types[0], double_t )
                         , "first argument of function of typedef 'member_function_ptr_t' should be '%s' instead of '%s' " \
                           %( 'double_t', function_type.arguments_types[0].__class__.__name__ ) )

        if self.global_ns.compiler != compilers.MSVC_PDB_9:
            self.failUnless( function_type.has_const, " 'member_function_ptr_t' should be const function." )

    def test_member_variable_type(self):
        if self.global_ns.compiler == compilers.MSVC_PDB_9:
            return

        mv = self.global_ns.decl( decl_type=typedef_t, name='member_variable_ptr_t')
        self._test_type_composition( mv.type, pointer_t, member_variable_type_t )

        members_pointers = self.global_ns.class_( 'members_pointers_t' )
        self.failUnless( members_pointers, "unable to find class('%s')" % 'members_pointers_t' )
        self._test_type_composition( mv.type.base, member_variable_type_t, declarated_t )
        mv_type = mv.type.base
        self.failUnless( mv_type.base.declaration is members_pointers
                         , "member function type class should be '%s' instead of '%s'" \
                           % ( members_pointers.decl_string, mv_type.base.decl_string ) )

    def test_overloading(self):
        ns = self.global_ns.namespace( 'overloads' )

        do_nothings = ns.calldefs( 'do_nothing', recursive=False )
        self.failUnless( 4 == len(do_nothings)
                         , "expected number of overloaded 'do_nothing' functions is %d and existing(%d) is different" \
                           % ( 4, len(do_nothings) ) )
        for index, do_nothing in enumerate(do_nothings):
            others = do_nothings[:index] + do_nothings[index+1:]
            if set( do_nothing.overloads ) != set( others ):
                print '\nexisting: '
                for x in do_nothing.overloads:
                    print str(x)
                print '\nexpected: '
                for x in others:
                    print str(x)

            self.failUnless( set( do_nothing.overloads ) == set( others )
                             , "there is a difference between expected function overloads and existing ones." )

    def test_abstract_classes(self):
        ns = self.global_ns.namespace( 'abstract_classes' )
        abstract_i = ns.class_( 'abstract_i' )
        self.failUnless( abstract_i.is_abstract, "class 'abstract_i' should be abstract" )
        derived_abstract_i = ns.class_( 'derived_abstract_i' )
        self.failUnless( derived_abstract_i.is_abstract, "class 'derived_abstract_i' should be abstract" )
        implementation = ns.class_( 'implementation' )
        self.failUnless( not implementation.is_abstract, "class 'implementation' should not be abstract" )

    def test_versioning(self):
        for d in self.global_ns.decls():
            self.failUnless( d.compiler )

    def test_byte_size( self ):
        mptrs = self.global_ns.class_( 'members_pointers_t' )
        self.failUnless( mptrs.byte_size != 0 )

    def test_byte_align( self ):
        mptrs = self.global_ns.class_( 'members_pointers_t' )
        if mptrs.compiler != compilers.MSVC_PDB_9:
            self.failUnless( mptrs.byte_align != 0 )

    def test_byte_offset( self ):
        mptrs = self.global_ns.class_( 'members_pointers_t' )
        self.failUnless( mptrs.var( 'xxx' ).byte_offset != 0 )

class pdb_based_core_tester_t( core_t ):
    def __init__(self, *args ):
        core_t.__init__( self, *args )
        self.global_ns = autoconfig.get_pdb_global_ns()

class core_gccxml_t( core_t ):
    """Tests core algorithms of GCC-XML and GCC-XML file reader.
    Those most white-box testing.
    """
    global_ns = None
    def __init__(self, *args ):
        core_t.__init__( self, *args )
        self.test_files = [ 'core_ns_join_1.hpp'
                            , 'core_ns_join_2.hpp'
                            , 'core_ns_join_3.hpp'
                            , 'core_membership.hpp'
                            , 'core_class_hierarchy.hpp'
                            , 'core_types.hpp'
                            , 'core_diamand_hierarchy_base.hpp'
                            , 'core_diamand_hierarchy_derived1.hpp'
                            , 'core_diamand_hierarchy_derived2.hpp'
                            , 'core_diamand_hierarchy_final_derived.hpp'
                            , 'core_overloads_1.hpp'
                            , 'core_overloads_2.hpp'
                            , 'abstract_classes.hpp'
        ]
        self.global_ns = None

    def setUp(self):
        if not core_t.global_ns:
            decls = parse( self.test_files, self.config, self.COMPILATION_MODE )
            core_t.global_ns = pygccxml.declarations.get_global_namespace( decls )
            if self.INIT_OPTIMIZER:
                core_t.global_ns.init_optimizer()
        self.global_ns = core_t.global_ns

class core_all_at_once_t( core_gccxml_t ):
    COMPILATION_MODE = COMPILATION_MODE.ALL_AT_ONCE
    INIT_OPTIMIZER = True
    def __init__(self, *args):
        core_gccxml_t.__init__(self, *args)

class core_all_at_once_no_opt_t( core_gccxml_t ):
    COMPILATION_MODE = COMPILATION_MODE.ALL_AT_ONCE
    INIT_OPTIMIZER = False
    def __init__(self, *args):
        core_gccxml_t.__init__(self, *args)

class core_file_by_file_t( core_gccxml_t ):
    COMPILATION_MODE = COMPILATION_MODE.FILE_BY_FILE
    INIT_OPTIMIZER = True
    def __init__(self, *args):
        core_gccxml_t.__init__(self, *args)

class core_file_by_file_no_opt_t( core_gccxml_t ):
    COMPILATION_MODE = COMPILATION_MODE.FILE_BY_FILE
    INIT_OPTIMIZER = False
    def __init__(self, *args):
        core_gccxml_t.__init__(self, *args)

def create_suite():
    suite = unittest.TestSuite()
    if autoconfig.cxx_parsers_cfg.gccxml:
        suite.addTest( unittest.makeSuite(core_all_at_once_t))
        suite.addTest( unittest.makeSuite(core_all_at_once_no_opt_t))
        suite.addTest( unittest.makeSuite(core_file_by_file_t))
        suite.addTest( unittest.makeSuite(core_file_by_file_no_opt_t))
    if autoconfig.cxx_parsers_cfg.pdb_loader:
        suite.addTest( unittest.makeSuite(pdb_based_core_tester_t))
    return suite

def run_suite():
    unittest.TextTestRunner(verbosity=2).run( create_suite() )

if __name__ == "__main__":
    run_suite()
##~     import hotshot
##~     import hotshot.stats
##~     statistics_file = tempfile.mkstemp( suffix='.stat' )[1]
##~     profile = hotshot.Profile(statistics_file)
##~
##~     profile.runcall( run_suite )
##~     profile.close()
##~     statistics = hotshot.stats.load( statistics_file )
##~     statistics.strip_dirs()
##~     statistics.sort_stats( 'time', 'calls' )
##~     statistics.print_stats( 678 )
