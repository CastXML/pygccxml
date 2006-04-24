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
    COMPILATION_MODE = COMPILATION_MODE.ALL_AT_ONCE
    def __init__(self, *args ):
        parser_test_case.parser_test_case_t.__init__( self, *args )
        self.content = "abra cadabra " + os.linesep

    def test_gccxml_on_input_with_errors(self):
        self.failUnlessRaises( gccxml_runtime_error_t, parse_string, self.content, self.config )

def create_suite():
    suite = unittest.TestSuite()        
    suite.addTest( unittest.makeSuite(tester_t))
    return suite

def run_suite():
    unittest.TextTestRunner(verbosity=2).run( create_suite() )

if __name__ == "__main__":
    run_suite()
