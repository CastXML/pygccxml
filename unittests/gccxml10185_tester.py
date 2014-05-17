# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import unittest
import parser_test_case

from pygccxml import parser
from pygccxml import declarations

code = \
"""
template <typename T> struct A {};
template <int N> struct A<const char[N]>
{ static int size(const char[N]) { return N - 1; } };
"""

class tester_t( parser_test_case.parser_test_case_t ):
    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)

    def test(self):
        src_reader = parser.source_reader_t( self.config )
        global_ns = declarations.get_global_namespace( src_reader.read_string( code ) )
        a = global_ns.class_( 'A<const char [N]>' )
        a.mem_fun( 'size' )


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest( unittest.makeSuite(tester_t))
    return suite

def run_suite():
    unittest.TextTestRunner(verbosity=2).run( create_suite() )

if __name__ == "__main__":
    run_suite()
