# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import unittest
import autoconfig
import parser_test_case

import pygccxml
from pygccxml.utils import *
from pygccxml.parser import *
from pygccxml.declarations import *

class tester_t( parser_test_case.parser_test_case_t ):
    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)

    def test_compound_argument_type(self):
        reader = source_reader_t( self.config )
        decls = reader.read_file( 'declarations_calldef.hpp' )
        do_smth = find_declaration( decls, type=member_function_t, name='do_smth' )
        self.failUnless( do_smth, "unable to find calldefs_t.do_smth" )
        cpptype = do_smth.function_type()

def create_suite():
    suite = unittest.TestSuite()        
    suite.addTest( unittest.makeSuite(tester_t))
    return suite

def run_suite():
    unittest.TextTestRunner(verbosity=2).run( create_suite() )

if __name__ == "__main__":
    run_suite()
