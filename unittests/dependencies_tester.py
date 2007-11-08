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
    def __init__(self, *args ):
        parser_test_case.parser_test_case_t.__init__( self, *args )
        self.header = 'include_all.hpp'
        self.global_ns = None
        
    def setUp(self):
        if not self.global_ns:
            decls = parser.parse( [self.header], self.config )
            self.global_ns = declarations.get_global_namespace( decls )
            self.global_ns.init_optimizer()

    def test_variable( self ):
        ns_vars = self.global_ns.namespace( '::declarations::variables' )
        static_var = ns_vars.variable( 'static_var' )
        dependencies = static_var.i_depend_on_them()        
        self.failUnless( len(dependencies) == 1 )
        self.failUnless( dependencies[0].declaration is static_var )
        self.failUnless( dependencies[0].depend_on_it.decl_string == 'int' )

        m_mutable = ns_vars.variable( 'm_mutable' )
        dependencies = m_mutable.i_depend_on_them()
        self.failUnless( len(dependencies) == 1 )
        self.failUnless( dependencies[0].declaration is m_mutable )
        self.failUnless( dependencies[0].depend_on_it.decl_string == 'int' )
        
    def test_class( self ):
        ns_vars = self.global_ns.namespace( '::declarations::variables' )

        cls = ns_vars.class_( 'struct_variables_t' )
        dependencies = cls.i_depend_on_them()
        if '0.9' in cls.compiler:
            self.failUnless( len(dependencies) == 1 )
        else:
            self.failUnless( len(dependencies) == 2 ) #compiler generated copy constructor
        
        m_mutable = ns_vars.variable( 'm_mutable' )
        dependencies = filter( lambda dependency: dependency.declaration is m_mutable
                               , dependencies )            
        self.failUnless( len(dependencies) == 1 )
        self.failUnless( dependencies[0].depend_on_it.decl_string == 'int' )
        self.failUnless( dependencies[0].access_type == 'public' )

        ns_dh = self.global_ns.namespace( '::core::diamand_hierarchy' )
        fd_cls = ns_dh.class_( 'final_derived_t' )
        derived1_cls = ns_dh.class_( 'derived1_t' )
        dependencies = fd_cls.i_depend_on_them()
        dependencies = filter( lambda dependency: dependency.depend_on_it is derived1_cls
                               , dependencies )  
        self.failUnless( len(dependencies) == 1 )
        self.failUnless( dependencies[0].depend_on_it is derived1_cls)
        self.failUnless( dependencies[0].access_type == 'public' )
        
    def test_calldefs( self ):
        ns = self.global_ns.namespace( '::declarations::calldef' )
        return_default_args = ns.calldef( 'return_default_args' )
        dependencies = return_default_args.i_depend_on_them()
        self.failUnless( len(dependencies) == 3 )
        used_types = map( lambda dependency: dependency.depend_on_it.decl_string 
                          , dependencies )
                          
        self.failUnless( used_types == [ 'int', 'bool', 'int' ] )

        some_exception = ns.class_( 'some_exception_t' )
        other_exception = ns.class_( 'other_exception_t' )
        calldef_with_throw = ns.calldef( 'calldef_with_throw' )
        dependencies = calldef_with_throw.i_depend_on_them()
        self.failUnless( len(dependencies) == 3 )
        dependencies = filter( lambda dependency: dependency.depend_on_it in ( some_exception, other_exception )
                               , dependencies )
        self.failUnless( len(dependencies) == 2 )
        
    def test_coverage( self ):
        self.global_ns.i_depend_on_them()
        
def create_suite():
    suite = unittest.TestSuite()        
    suite.addTest( unittest.makeSuite(tester_t))
    return suite

def run_suite():
    unittest.TextTestRunner(verbosity=2).run( create_suite() )

if __name__ == "__main__":
    run_suite()
