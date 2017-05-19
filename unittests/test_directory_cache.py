# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import os
import sys
import shutil
import unittest

from . import parser_test_case

from pygccxml import parser


class Test(parser_test_case.parser_test_case_t):

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.header = "typedefs1.hpp"
        this_module_dir_path = os.path.abspath(
            os.path.dirname(sys.modules[__name__].__file__))
        self.cache_dir = os.path.join(
            this_module_dir_path, "data/directory_cache_test")

    def setUp(self):
        # Clear the cache tree
        if os.path.isdir(self.cache_dir):  # pragma: no cover
            shutil.rmtree(self.cache_dir)

    def test_directory_cache_without_compression(self):
        """
        Test the directory cache without compression

        """
        # Test with compression OFF
        cache = parser.directory_cache_t(directory=self.cache_dir)
        # Generate a cache on first read
        parser.parse([self.header], self.config, cache=cache)
        # Read from the cache the second time
        parser.parse([self.header], self.config, cache=cache)

    def test_directory_cache_with_compression(self):
        """
        Test the directory cache wit compression

        """
        # Test with compression ON
        cache = parser.directory_cache_t(
            directory=self.cache_dir, compression=True)
        # Generate a cache on first read
        parser.parse([self.header], self.config, cache=cache)
        # Read from the cache the second time
        parser.parse([self.header], self.config, cache=cache)

    def test_directory_cache_twice(self):
        """
        Setup two caches in a row.

        The second run will reload the same cache directory.
        """
        cache = parser.directory_cache_t(directory=self.cache_dir)
        parser.parse([self.header], self.config, cache=cache)
        cache = parser.directory_cache_t(directory=self.cache_dir)
        parser.parse([self.header], self.config, cache=cache)

    def test_directory_existing_dir(self):
        """
        Setup a cache when there is already a file at the cache's location.
        """
        open(self.cache_dir, "a").close()
        self.assertRaises(
            ValueError,
            lambda: parser.directory_cache_t(directory=self.cache_dir))
        os.remove(self.cache_dir)


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
