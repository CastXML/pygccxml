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
        self.headers = [ 'remove_template_defaults.hpp', 'indexing_suites2.hpp' ]
        
    def setUp(self):
        if not tester_t.global_ns:
            decls = parser.parse( self.headers, self.config )
            tester_t.global_ns = declarations.get_global_namespace( decls )
            tester_t.global_ns.init_optimizer()
    
    def __cmp_traits( self, typedef, expected, partial_name):
        if isinstance( typedef, str ):
            typedef = self.global_ns.typedef( typedef )
        traits = declarations.find_container_traits( typedef )
        self.failUnless( traits, 'container traits for "%s" not found' % str( typedef ) )
        self.failUnless( traits is expected
                         , 'container "%s", expected %s_traits, got %s_traits' 
                           % ( str(typedef), expected.name(), traits.name() ) )
        cls = declarations.remove_declarated( typedef )                                        
        self.failUnless( cls.container_traits is expected )
        self.failUnless( cls.partial_name == partial_name )

    def test_find_traits( self ):
        self.__cmp_traits( 'v_int', declarations.vector_traits, "vector< int >" )
        self.__cmp_traits( 'l_int', declarations.list_traits, "list< int >" )
        self.__cmp_traits( 'd_v_int', declarations.deque_traits, "deque< std::vector< int > >" )
        self.__cmp_traits( 'q_int', declarations.queue_traits, "queue< int >" )
        self.__cmp_traits( 'pq_int', declarations.priority_queue_traits, "priority_queue< int >")
        self.__cmp_traits( 's_v_int', declarations.set_traits, "set< std::vector< int > >")
        self.__cmp_traits( 'ms_v_int', declarations.multiset_traits, "multiset< std::vector< int > >")
        self.__cmp_traits( 'm_i2d', declarations.map_traits, "map< int, double >" )
        self.__cmp_traits( 'mm_i2d', declarations.multimap_traits, "multimap< int, double >" )
        self.__cmp_traits( 'hs_v_int', declarations.hash_set_traits, "hash_set< std::vector< int > >" )
        self.__cmp_traits( 'mhs_v_int', declarations.hash_multiset_traits, "hash_multiset< std::vector< int > >" )
        self.__cmp_traits( 'hm_i2d', declarations.hash_map_traits, "hash_map< int, double >" )
        self.__cmp_traits( 'hmm_i2d', declarations.hash_multimap_traits, "hash_multimap< int, double >" )

    def test_multimap( self ):
        mm = self.global_ns.classes( lambda decl: decl.name.startswith( 'multimap' ) )
        for m in mm:
            traits = declarations.find_container_traits( m )
            print m.partial_name

    def test_recursive_partial_name( self ):
        f1 = self.global_ns.free_fun( 'f1' )
        t1 = declarations.class_traits.get_declaration( f1.arguments[0].type )
        self.failUnless( 'type< std::set< std::vector< int > > >' == t1.partial_name )

    def test_from_ogre( self ):
        x = 'map<std::string, bool (*)(std::string&, Ogre::MaterialScriptContext&), std::less<std::string>, std::allocator<std::pair<std::string const, bool (*)(std::string&, Ogre::MaterialScriptContext&)> > >'
        ct = declarations.find_container_traits( x )
        y = ct.remove_defaults( x )
    
    def test_infinite_loop(self):
        rt = self.global_ns.free_fun( 'test_infinite_loop' ).return_type
        map_traits = declarations.find_container_traits( rt )
        self.failUnless( map_traits is declarations.map_traits )
        elem = map_traits.element_type( rt )
        self.failUnless( elem.decl_string == 'int' )
    
def create_suite():
    suite = unittest.TestSuite()        
    suite.addTest( unittest.makeSuite(tester_t))
    return suite

def run_suite():
    unittest.TextTestRunner(verbosity=2).run( create_suite() )

if __name__ == "__main__":
    run_suite()
