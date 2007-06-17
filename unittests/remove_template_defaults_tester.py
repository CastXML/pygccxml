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
    global_ns = None
    def __init__(self, *args ):
        parser_test_case.parser_test_case_t.__init__( self, *args )
        self.header = 'remove_template_defaults.hpp'
        
    def setUp(self):
        if not tester_t.global_ns:
            decls = parser.parse( [self.header], self.config )
            tester_t.global_ns = declarations.get_global_namespace( decls )
            tester_t.global_ns.init_optimizer()
            
    def test_vector( self ):                
        v_int = self.global_ns.typedef( 'v_int' )        
        self.failUnless( 'vector< int >' 
                          == declarations.vector_traits.remove_defaults( v_int ) )
        v_string = self.global_ns.typedef( 'v_string' )
        self.failUnless( 'vector< std::string >'
                         == declarations.vector_traits.remove_defaults( v_string ) )
        v_v_int = self.global_ns.typedef( 'v_v_int' )                                 
        self.failUnless( 'vector< std::vector< int > >'
                         == declarations.vector_traits.remove_defaults( v_v_int ) )
        
    def test_list( self ):                
        l_int = self.global_ns.typedef( 'l_int' )
        self.failUnless( 'list< int >' 
                          == declarations.list_traits.remove_defaults( l_int ) )
        l_wstring = self.global_ns.typedef( 'l_wstring' )
        self.failUnless( 'list< std::wstring >'
                         == declarations.list_traits.remove_defaults( l_wstring ) )

    def test_deque( self ):                
        d_v_int = self.global_ns.typedef( 'd_v_int' )
        self.failUnless( 'deque< std::vector< int > >' 
                         == declarations.deque_traits.remove_defaults( d_v_int ) )
        d_l_string = self.global_ns.typedef( 'd_l_string' )
        self.failUnless( 'deque< std::list< std::string > >'
                         == declarations.deque_traits.remove_defaults( d_l_string ) )

    def test_queue( self ):                
        q_int = self.global_ns.typedef( 'q_int' )
        self.failUnless( 'queue< int >' 
                         == declarations.queue_traits.remove_defaults( q_int ) )
        q_string = self.global_ns.typedef( 'q_string' )
        self.failUnless( 'queue< std::string >'
                         == declarations.queue_traits.remove_defaults( q_string ) )


def create_suite():
    suite = unittest.TestSuite()        
    suite.addTest( unittest.makeSuite(tester_t))
    return suite

def run_suite():
    unittest.TextTestRunner(verbosity=2).run( create_suite() )

if __name__ == "__main__":
    run_suite()
