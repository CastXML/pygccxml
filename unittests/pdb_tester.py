import os
import unittest
import autoconfig

from pygccxml.msvc import pdb
from pygccxml import declarations

class tester_t( unittest.TestCase ):
    def __init__(self, *args):
        unittest.TestCase.__init__(self, *args)

    def test(self):
        control_pdb = os.path.join( autoconfig.data_directory, r'xxx.pdb' )
        reader = pdb.reader_t( control_pdb )
        reader.read()
        f = file( 'decls.cpp', 'w+' )
        declarations.print_declarations( reader.global_ns, writer=f.write )
        f.close()

def create_suite():
    suite = unittest.TestSuite()        
    suite.addTest( unittest.makeSuite(tester_t))
    return suite

def run_suite():
    unittest.TextTestRunner(verbosity=2).run( create_suite() )

if __name__ == "__main__":
    run_suite()