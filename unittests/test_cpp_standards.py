# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import platform
import unittest

from . import parser_test_case

from pygccxml import parser


class Test(parser_test_case.parser_test_case_t):

    def test(self):
        """
        Test different compilation standards by setting cflags.

        """

        parser.parse(["cpp_standards.hpp"], self.config)

        if platform.system() != 'Windows':
            self.config.cflags = "-std=c++98"
            parser.parse(["cpp_standards.hpp"], self.config)

            self.config.cflags = "-std=c++03"
            parser.parse(["cpp_standards.hpp"], self.config)

        self.config.cflags = "-std=c++11"
        parser.parse(["cpp_standards.hpp"], self.config)

        # This is broken with llvm 3.6.2 (the one from homebrew)
        # It should work with never llvms but I keep the test disabled
        # See https://llvm.org/bugs/show_bug.cgi?id=24872
        # self.config.cflags = "-std=c++14"
        # parser.parse(["cpp_standards.hpp"], self.config)

        # Same as above
        # self.config.cflags = "-std=c++1z"
        # parser.parse(["cpp_standards.hpp"], self.config)

        # Pass down a flag that does not exist.
        # This should raise an exception.
        self.config.cflags = "-std=c++00"
        self.assertRaises(
            RuntimeError,
            lambda: parser.parse(["cpp_standards.hpp"], self.config))

    def test_cpp17(self):
        """
        Test c++17 by setting cflags.

        """

        self.config.cflags = "-std=c++17"
        parser.parse(["cpp_standard_17.hpp"], self.config)


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(
        unittest.TestLoader().loadTestsFromTestCase(testCaseClass=Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
