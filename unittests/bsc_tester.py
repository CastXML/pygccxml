import os
import unittest
import autoconfig

from pygccxml.msvc import bsc

class tester_t( unittest.TestCase ):
    def __init__(self, *args):
        unittest.TestCase.__init__(self, *args)

    def test(self):
        control_bsc = os.path.join( autoconfig.data_directory, r'xxx.bsc' )
        reader = bsc.reader_t( control_bsc )
        reader.print_stat()
        print 'is_case_sensitive', reader.is_case_sensitive
        reader.load_instances()
        print 'done'
        #reader.files        
        #reader.print_classes( )#r'c:\dev\produce_pdb\produce_pdb.cpp')


def create_suite():
    suite = unittest.TestSuite()        
    suite.addTest( unittest.makeSuite(tester_t))
    return suite

def run_suite():
    unittest.TextTestRunner(verbosity=2).run( create_suite() )

if __name__ == "__main__":
    run_suite()