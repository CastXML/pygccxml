# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import os 
import stat
import unittest
import parser_test_case

from pygccxml import utils
from pygccxml import parser

class tester_t( parser_test_case.parser_test_case_t ):
    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.__fname = 'core_types.hpp'

    def test(self):
        fconfig = parser.file_configuration_t( data=self.__fname
                    , content_type=parser.CONTENT_TYPE.CACHED_SOURCE_FILE )
        try:
            prj_reader = parser.project_reader_t( self.config )
            prj_reader.read_files( [fconfig]
                                               , compilation_mode=parser.COMPILATION_MODE.FILE_BY_FILE )
            self.failUnless( os.path.exists( fconfig.cached_source_file ) )
            mtime1 = os.stat(fconfig.cached_source_file)[stat.ST_MTIME] 
            prj_reader.read_files( [fconfig]
                                               , compilation_mode=parser.COMPILATION_MODE.FILE_BY_FILE )
            mtime2 = os.stat(fconfig.cached_source_file)[stat.ST_MTIME] 
            self.failUnless( mtime1 == mtime2 )
        finally:
            utils.remove_file_no_raise( fconfig.cached_source_file )
   
def create_suite():
    suite = unittest.TestSuite()        
    suite.addTest( unittest.makeSuite(tester_t))    
    return suite

def run_suite():
    unittest.TextTestRunner(verbosity=2).run( create_suite() )

if __name__ == "__main__":
    run_suite()
