# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import io
import sys
import os
import unittest
import warnings

sys.path.insert(1, os.path.join(os.curdir, '..'))
sys.path.insert(1, "../pygccxml")

from pygccxml import parser  # nopep8
from pygccxml import utils  # nopep8


class Test(unittest.TestCase):

    def test_config(self):
        """
            Test that a missing include directory is printing a warning,
            not raising an error
        """

        # Some code to parse for the example
        code = "int a;"

        # Find the location of the xml generator (castxml or gccxml)
        generator_path, name = utils.find_xml_generator()

        # Path given as include director doesn't exist
        config = parser.xml_generator_configuration_t(
            xml_generator_path=generator_path,
            xml_generator=name,
            include_paths=["doesnt/exist", os.getcwd()])
        self.assertWarns(UserWarning, parser.parse_string, code, config)



def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
