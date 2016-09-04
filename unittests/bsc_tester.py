import os
import unittest
import autoconfig

from pygccxml.binary_parsers import bsc


class Test(unittest.TestCase):

    def __init__(self, *args):
        unittest.TestCase.__init__(self, *args)
        self.bsc_file = os.path.join(
            autoconfig.data_directory,
            'msvc_build',
            'Debug',
            'msvc_build.bsc')

    def test(self):
        reader = bsc.reader_t(self.bsc_file)
        reader.print_stat()
        print 'is_case_sensitive', reader.is_case_sensitive
        reader.load_instances()
        # reader.files
        reader.print_classes()  # r'c:\dev\produce_pdb\produce_pdb.cpp')
        # names = []
        # for inst in reader.instances:
        # names.append( '{%s}<=====>{%s}' % ( inst.name, inst.mangled_name ) )
        # names.sort()
        # for name in names:
        # print name


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())

if __name__ == "__main__":
    run_suite()
