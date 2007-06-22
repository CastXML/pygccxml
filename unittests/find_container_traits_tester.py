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
    
    def __cmp_traits( self, typedef, expected ):
        if isinstance( typedef, str ):
            typedef = self.global_ns.typedef( typedef )
        traits = declarations.find_container_traits( typedef )
        self.failUnless( traits, 'container traits for "%s" not found' % str( typedef ) )
        self.failUnless( traits is expected
                         , 'container "%s", expected %s, got %s' 
                           % ( str(typedef), expected.__name__, traits.__name__ ) )
        cls = declarations.remove_declarated( typedef )                                        
        self.failUnless( cls.container_traits is expected )
        
    def test_find_traits( self ):                
        self.__cmp_traits( 'v_int', declarations.vector_traits )
        self.__cmp_traits( 'l_int', declarations.list_traits )
        self.__cmp_traits( 'd_v_int', declarations.deque_traits )
        self.__cmp_traits( 'q_int', declarations.queue_traits )
        self.__cmp_traits( 'pq_int', declarations.priority_queue_traits)
        self.__cmp_traits( 's_v_int', declarations.set_traits)
        self.__cmp_traits( 'ms_v_int', declarations.multiset_traits)
        self.__cmp_traits( 'm_i2d', declarations.map_traits )
        self.__cmp_traits( 'mm_i2d', declarations.multimap_traits )
        self.__cmp_traits( 'hs_v_int', declarations.hash_set_traits )
        self.__cmp_traits( 'mhs_v_int', declarations.hash_multiset_traits )
        self.__cmp_traits( 'hm_i2d', declarations.hash_map_traits )
        self.__cmp_traits( 'hmm_i2d', declarations.hash_multimap_traits )

def create_suite():
    suite = unittest.TestSuite()        
    suite.addTest( unittest.makeSuite(tester_t))
    return suite

def run_suite():
    unittest.TextTestRunner(verbosity=2).run( create_suite() )

if __name__ == "__main__":
    run_suite()
