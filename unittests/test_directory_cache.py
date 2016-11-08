# Copyright 2014-2016 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import unittest
import parser_test_case

from pygccxml import parser


class Test(parser_test_case.parser_test_case_t):

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.header = "core_cache.hpp"

    def test_directory_cache(self):
        """
        Test the directory cache

        """

        cache = parser.directory_cache_t(
            dir="unittests/data/directory_cache_test")
        # Generate a cache on first read
        parser.parse([self.header], self.config, cache=cache)
        # Read from the cache the second time
        parser.parse([self.header], self.config, cache=cache)


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())

if __name__ == "__main__":
    run_suite()
