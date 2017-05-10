# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import unittest

from . import parser_test_case

from pygccxml import parser


class Test(parser_test_case.parser_test_case_t):

    def test_castxml_epic_version_check(self):
        """
        Test using a forbidden value for the castxml epic version.

        """

        if self.config.castxml_epic_version != 1:
            # Run this test only with castxml epic version == 1
            return

        self.config.castxml_epic_version = 2
        self.assertRaises(
            RuntimeError, lambda: parser.parse_string("", self.config))

        # Reset castxml epic version
        self.config.castxml_epic_version = 1


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
