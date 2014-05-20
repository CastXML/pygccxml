#! /usr/bin/python
# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

from __future__ import unicode_literals

import unittest
import sys
sys.path.append("/home/mpopoff/repo/pygccxml")
from pygccxml import declarations
from pygccxml import parser

class tester_t( unittest.TestCase ):

    """
    Some methods like namespace() verify if their argument is a string.
    Check if this works well and if it is compatible with the
    from __future__ import unicode_literals statement.

    """

    def __init__(self, *args ):
        unittest.TestCase.__init__( self, *args )

    def test_namespace_argument_string(self):
        # Check with a string        
        self.global_ns.namespace("test")
    
    def test_namespace_argument_int(self):
        # Check with an int, should raise an error
        try:
            # This should fail
            self.global_ns.namespace(1)
            self.fail("No error message triggered")
        except AssertionError:
            pass

    def setUp(self):
        config = parser.config.gccxml_configuration_t()
        decls = parser.parse(["data/basic.hpp"], config)
        self.global_ns = declarations.get_global_namespace(decls)

def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(tester_t))
    return suite

def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())

if __name__ == "__main__":
    run_suite()
