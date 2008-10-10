# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import copy
import unittest
import autoconfig
import parser_test_case

import pygccxml
from pygccxml.utils import *
from pygccxml.parser import *
from pygccxml.declarations import *

class tester_t(parser_test_case.parser_test_case_t):
    COMPILATION_MODE = COMPILATION_MODE.ALL_AT_ONCE
    def __init__(self, *args ):
        parser_test_case.parser_test_case_t.__init__( self, *args )
        self.header = 'declarations_comparison.hpp'

    def test_comparison_declaration_by_declaration(self):
        parsed = parse( [self.header], self.config )
        copied = copy.deepcopy( parsed )
        parsed = make_flatten( parsed )
        copied = make_flatten( copied )
        parsed.sort()
        copied.sort()
        failuers = []
        for parsed_decl, copied_decl, index in zip( parsed, copied, range(len(copied)) ):
            if parsed_decl != copied_decl:
                failuers.append( "__lt__ and/or __qe__ does not working properly in case of %s, %s, index %d" \
                                 % ( parsed_decl.__class__.__name__, copied_decl.__class__.__name__, index ) )
        self.failUnless( not failuers, 'Failures: ' + '\n\t'.join(failuers) )

    def test_comparison_from_reverse(self):
        parsed = parse( [self.header], self.config )
        copied = copy.deepcopy( parsed )
        parsed.sort()
        copied.reverse()
        copied.sort()
        x = parsed[4:6]
        x.sort()
        y = copied[4:6]
        y.sort()
        self.failUnless( parsed == copied
                         , "__lt__ and/or __qe__ does not working properly" )

    def test___lt__transitivnost(self):
        ns_std = namespace_t(name='std')
        ns_global = namespace_t(name='::')
        ns_internal = namespace_t(name='ns')
        ns_internal.parent = ns_global
        ns_global.declarations.append( ns_internal )
        left2right = [ ns_std, ns_global ]
        right2left = [ ns_global, ns_std ]
        left2right.sort()
        right2left.sort()
        self.failUnless( left2right == right2left, "bug: find me" )

    def test_same_declarations_different_intances(self):
        parsed = parse( [self.header], self.config )
        copied = copy.deepcopy( parsed )
        self.failUnless( parsed == copied
                         , "__lt__ and/or __qe__ does not working properly" )

def create_suite():
    suite = unittest.TestSuite()        
    suite.addTest( unittest.makeSuite(tester_t))
    return suite

def run_suite():
    unittest.TextTestRunner(verbosity=2).run( create_suite() )

if __name__ == "__main__":
    run_suite()
