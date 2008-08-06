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
        self.header = 'better_templates_matcher_tester.hpp'
        
    def setUp(self):
        if not tester_t.global_ns:
            decls = parser.parse( [self.header], self.config )
            tester_t.global_ns = declarations.get_global_namespace( decls )
            tester_t.global_ns.init_optimizer()
            
    def test( self ):                
        classes = [ '::std::vector<Ogre::PlaneBoundedVolume,std::allocator<Ogre::PlaneBoundedVolume>>'
                    , '::std::vector<Ogre::Plane,  std::allocator<Ogre::Plane>>'
                    , '::Ogre::Singleton<    Ogre::PCZoneFactoryManager>' ]             
        for i in classes:
            c = self.global_ns.class_( i )

def create_suite():
    suite = unittest.TestSuite()        
    suite.addTest( unittest.makeSuite(tester_t))
    return suite

def run_suite():
    unittest.TextTestRunner(verbosity=2).run( create_suite() )

if __name__ == "__main__":
    run_suite()