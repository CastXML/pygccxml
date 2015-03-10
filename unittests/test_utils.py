# Copyright 2014 Insight Software Consortium.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import os
import unittest
import autoconfig
import parser_test_case

from pygccxml import utils


class tester_t(parser_test_case.parser_test_case_t):

    def test(self):
        path = os.path.normpath("/mypath/folder1/folder2/folder3")
        dirs = [
            "/mypath/folder1/folder2/",
            "/mypath3/folder1/folder2/folder3",
            "home",
            "/test/test1/mypath"]

        self.assertTrue(utils.utils.contains_parent_dir(path, dirs))

        dirs = ["/home", "/mypath/test/"]

        self.assertFalse(utils.utils.contains_parent_dir(path, dirs))


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(tester_t))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())

if __name__ == "__main__":
    run_suite()
