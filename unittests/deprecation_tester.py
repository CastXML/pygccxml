# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import unittest
import warnings

from . import parser_test_case

from pygccxml import declarations


class Test(parser_test_case.parser_test_case_t):

    def test_scopedef_deprecations(self):
        """
        Test the deprecated attributes in scopedef

        """
        scopedef = declarations.scopedef_t()
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            _ = scopedef.declaration_not_found_t
            self._check(w)

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            _ = scopedef.multiple_declarations_found_t
            self._check(w)

    @staticmethod
    def _check(w):
        assert len(w) == 1
        assert issubclass(w[-1].category, DeprecationWarning)
        assert "deprecated" in str(w[-1].message)


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
