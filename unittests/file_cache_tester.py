# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import os
import sys
import stat
import time
import unittest
import tempfile
import autoconfig
import parser_test_case
from pprint import pformat

import pygccxml
from pygccxml.utils import *
from pygccxml.parser import *
from pygccxml.declarations import *

class tester_t( parser_test_case.parser_test_case_t ):
    COMPILATION_MODE = COMPILATION_MODE.ALL_AT_ONCE
    def __init__(self, *args ):
        parser_test_case.parser_test_case_t.__init__( self, *args )
        self.header = os.path.join( autoconfig.data_directory, 'core_cache.hpp' )
        self.cache_file = os.path.join( autoconfig.data_directory, 'pygccxml.cache' )
        if os.path.exists( self.cache_file ) and os.path.isfile( self.cache_file ):
            os.remove(self.cache_file)

    def touch(self):
        #os.utime( self.header, ( os.stat( self.header )[ stat.ST_ATIME ], int( time.time() ) ) )
        # Need to change file.
        header = open(self.header, "a")
        header.write("//touch")
        header.close()

        
    def test_update(self):
        declarations = parse( [self.header], self.config )
        cache = file_cache_t( self.cache_file )
        cache.update( source_file=self.header
                      , configuration=self.config
                      , declarations=declarations
                      , included_files=[] )
        self.failUnless( declarations == cache.cached_value(self.header, self.config)
                        , "cached declarations and source declarations are different")
        self.touch()
        self.failUnless( None == cache.cached_value(self.header, self.config)
                         , "cache didn't recognize that some files on disk has been changed" )

    def test_from_file(self):
        declarations = parse( [self.header], self.config )
        cache = file_cache_t( self.cache_file )
        cache.update( source_file=self.header
                      , configuration=self.config
                      , declarations=declarations
                      , included_files=[] )
        self.failUnless( declarations == cache.cached_value(self.header, self.config)
                         , "cached declarations and source declarations are different")
        cache.flush()
        cache = file_cache_t( self.cache_file )
        self.failUnless( declarations == cache.cached_value(self.header, self.config)
                         , "cached declarations and source declarations are different, after pickling")


def create_suite():
    suite = unittest.TestSuite()        
    suite.addTest( unittest.makeSuite(tester_t))
    return suite

def run_suite():
    unittest.TextTestRunner(verbosity=2).run( create_suite() )

if __name__ == "__main__":
    run_suite()