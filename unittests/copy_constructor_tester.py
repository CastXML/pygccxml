# Copyright 2004-2008 Roman Yakovenko.
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

class tester_t( parser_test_case.parser_test_case_t ):
    def __init__(self, *args ):
        parser_test_case.parser_test_case_t.__init__( self, *args )
        self.global_ns = None
        
    def setUp(self):
        if not self.global_ns:
            xml_file = os.path.join( autoconfig.data_directory, 'ogre.1.7.xml' )
            reader = parser.source_reader_t( autoconfig.cxx_parsers_cfg.gccxml )            
            self.global_ns = declarations.get_global_namespace( reader.read_xml_file(xml_file) )
            self.global_ns.init_optimizer()
            
    def test( self ):                
        for x in self.global_ns.typedefs( 'SettingsMultiMap' ):
            self.failUnless( not declarations.is_noncopyable( x ) ) 
  
        for x in self.global_ns.typedefs( 'SettingsIterator' ):
            self.failUnless( not declarations.is_noncopyable( x ) ) 

        for x in self.global_ns.typedefs( 'SectionIterator' ):
            self.failUnless( not declarations.is_noncopyable( x ) ) 

def create_suite():
    suite = unittest.TestSuite()        
    suite.addTest( unittest.makeSuite(tester_t))
    return suite

def run_suite():
    unittest.TextTestRunner(verbosity=2).run( create_suite() )

if __name__ == "__main__":
    run_suite()
