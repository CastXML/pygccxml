# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import sys
import os
import unittest

sys.path.insert(1, os.path.join(os.curdir, '..'))
sys.path.insert(1, "../pygccxml")

from pygccxml import parser  # nopep8
from pygccxml import utils  # nopep8


class Test(unittest.TestCase):

    def test_config(self):
        """Test config setup with wrong xml generator setups."""

        # Some code to parse for the example
        code = "int a;"

        # Find the location of the xml generator (castxml or gccxml)
        generator_path, name = utils.find_xml_generator()

        # No xml generator path
        config = parser.xml_generator_configuration_t(xml_generator=name)
        self.assertRaises(
            RuntimeError, lambda: parser.parse_string(code, config))

        # Invalid path
        config = parser.xml_generator_configuration_t(
            xml_generator_path="wrong/path",
            xml_generator=name)
        self.assertRaises(
            RuntimeError, lambda: parser.parse_string(code, config))

        # None path
        config = parser.xml_generator_configuration_t(
            xml_generator_path=None,
            xml_generator=name)
        self.assertRaises(
            RuntimeError, lambda: parser.parse_string(code, config))

        # No name
        config = parser.xml_generator_configuration_t(
            xml_generator_path=generator_path)
        self.assertRaises(
            RuntimeError, lambda: parser.parse_string(code, config))

        # Random name
        config = parser.xml_generator_configuration_t(
            xml_generator_path=generator_path,
            xml_generator="not_a_generator")
        self.assertRaises(
            RuntimeError, lambda: parser.parse_string(code, config))

        # None name
        config = parser.xml_generator_configuration_t(
            xml_generator_path=generator_path,
            xml_generator=None)
        self.assertRaises(
            RuntimeError, lambda: parser.parse_string(code, config))


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
