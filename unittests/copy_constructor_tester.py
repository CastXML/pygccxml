# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import os
import bz2
import unittest

from . import autoconfig
from . import parser_test_case

from pygccxml import parser
from pygccxml import declarations


class Test(parser_test_case.parser_test_case_t):

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.global_ns = None
        self.xml_path = None

    def setUp(self):
        if not self.global_ns:

            # Extract the xml file from the bz2 archive
            bz2_path = os.path.join(
                autoconfig.data_directory,
                'ogre.1.7.xml.bz2')
            self.xml_path = os.path.join(
                autoconfig.data_directory,
                'ogre.1.7.xml')
            with open(self.xml_path, 'wb') as new_file:
                # bz2.BZ2File can not be used in a with statement in python 2.6
                bz2_file = bz2.BZ2File(bz2_path, 'rb')
                for data in iter(lambda: bz2_file.read(100 * 1024), b''):
                    new_file.write(data)
                bz2_file.close()

            reader = parser.source_reader_t(autoconfig.cxx_parsers_cfg.config)
            self.global_ns = declarations.get_global_namespace(
                reader.read_xml_file(
                    self.xml_path))
            self.global_ns.init_optimizer()

    def tearDown(self):
        # Delete the extracted xml file
        os.remove(self.xml_path)

    def test(self):
        for x in self.global_ns.typedefs('SettingsMultiMap'):
            self.assertTrue(not declarations.is_noncopyable(x))

        for x in self.global_ns.typedefs('SettingsIterator'):
            self.assertTrue(not declarations.is_noncopyable(x))

        for x in self.global_ns.typedefs('SectionIterator'):
            self.assertTrue(not declarations.is_noncopyable(x))


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
