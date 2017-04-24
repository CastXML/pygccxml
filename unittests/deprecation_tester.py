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

    def test_declaration_path(self):
        """
        Test the deprecated with_defaults parameter

        """
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            declarations.declaration_path(None, True)
            self._check(w)

    def test_nss(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            try:
                declarations.namespace_t().nss()
            except RuntimeError:
                pass
            self._check(w)

    def test_free_fun(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            try:
                declarations.namespace_t().free_fun()
            except RuntimeError:
                pass
            self._check(w)

    def test_free_funs(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            try:
                declarations.namespace_t().free_funs()
            except RuntimeError:
                pass
            self._check(w)

    def test_mem_fun(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            try:
                declarations.scopedef_t().mem_fun()
            except RuntimeError:
                pass
            self._check(w)

    def test_mem_funs(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            try:
                declarations.scopedef_t().mem_funs()
            except RuntimeError:
                pass
            self._check(w)

    def test_mem_oper(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            try:
                declarations.scopedef_t().mem_oper()
            except RuntimeError:
                pass
            self._check(w)

    def test_mem_opers(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            try:
                declarations.scopedef_t().mem_opers()
            except RuntimeError:
                pass
            self._check(w)

    def test_enum(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            try:
                declarations.scopedef_t().enum()
            except RuntimeError:
                pass
            self._check(w)

    def test_enums(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            try:
                declarations.scopedef_t().enums()
            except RuntimeError:
                pass
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
