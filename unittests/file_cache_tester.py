# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import os
import sys
import unittest
import subprocess

from . import autoconfig
from . import parser_test_case

from pygccxml import parser


class Test(parser_test_case.parser_test_case_t):
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.header = os.path.join(autoconfig.data_directory, 'core_cache.hpp')
        self.cache_file = os.path.join(
            autoconfig.data_directory,
            'pygccxml.cache')
        if os.path.exists(self.cache_file) and os.path.isfile(self.cache_file):
            os.remove(self.cache_file)

    def touch(self):
        # Need to change file.
        with open(self.header, "a+") as header:
            header.write("//touch")

    def test_update(self):

        # Save the content of the header file for later
        with open(self.header, "r") as old_header:
            content = old_header.read()

        declarations = parser.parse([self.header], self.config)
        cache = parser.file_cache_t(self.cache_file)
        cache.update(
            source_file=self.header,
            configuration=self.config,
            declarations=declarations,
            included_files=[])
        self.assertTrue(
            declarations == cache.cached_value(
                self.header,
                self.config),
            "cached declarations and source declarations are different")
        self.touch()
        self.assertTrue(
            cache.cached_value(self.header, self.config) is None,
            "cache didn't recognize that some files on disk has been changed")

        # We wrote a //touch in the header file. Just replace the file with the
        # original content. The touched file would be sometimes commited by
        # error as it was modified.
        with open(self.header, "w") as new_header:
            new_header.write(content)

    def test_from_file(self):
        declarations = parser.parse([self.header], self.config)
        cache = parser.file_cache_t(self.cache_file)
        cache.update(
            source_file=self.header,
            configuration=self.config,
            declarations=declarations,
            included_files=[])
        self.assertTrue(
            declarations == cache.cached_value(
                self.header,
                self.config),
            "cached declarations and source declarations are different")
        cache.flush()
        cache = parser.file_cache_t(self.cache_file)
        self.assertTrue(
            declarations == cache.cached_value(
                self.header,
                self.config),
            ("cached declarations and source declarations are different, " +
                "after pickling"))


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
