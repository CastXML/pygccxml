# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import unittest

from . import parser_test_case

from pygccxml import declarations


class Test(parser_test_case.parser_test_case_t):

    def test_extract(self):
        data = [
            ('thiscall',
             '(public: __thiscall std::auto_ptr<class pof::number_t>' +
             '::auto_ptr<class pof::number_t>(class std::auto_ptr' +
             '<class pof::number_t> &))'),
            ('',  "(const pof::number_t::`vftable')")]

        for expected, text in data:
            got = declarations.CALLING_CONVENTION_TYPES.extract(text)
            self.assertTrue(
                got == expected, "Expected calling convention: %s, got %s" %
                (expected, got))


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
