# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import os
import warnings
import unittest

from . import parser_test_case

from pygccxml import utils


class Test(parser_test_case.parser_test_case_t):

    def test(self):
        path = os.path.normpath("/mypath/folder1/folder2/folder3")
        dirs = [
            os.path.normpath("/mypath/folder1/folder2/"),
            os.path.normpath("/mypath3/folder1/folder2/folder3"),
            os.path.normpath("home"),
            os.path.normpath("/test/test1/mypath")]

        self.assertTrue(utils.utils.contains_parent_dir(path, dirs))

        dirs = [os.path.normpath("/home"), os.path.normpath("/mypath/test/")]

        self.assertFalse(utils.utils.contains_parent_dir(path, dirs))

    def test_deprecation_wrapper(self):
        """
        The DeprecationWrapper is not part of the public API

        We still need to test it.
        """

        a = utils.utils.DeprecationWrapper(
            DeprecatedClass,
            "DeprecatedClass",
            "NewClass",
            "1.9.0")
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            a()
            assert len(w) == 1
            assert issubclass(w[-1].category, DeprecationWarning)
            assert "deprecated" in str(w[-1].message)


class DeprecatedClass(object):
    """
    An empty class used for testing purposes.
    """
    pass


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
