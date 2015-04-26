# Copyright 2014-2015 Insight Software Consortium.
# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import unittest
from pygccxml import declarations


class tester_t(unittest.TestCase):

    def __init__(self, *args):
        unittest.TestCase.__init__(self, *args)

    def test_extract(self):
        data = [
            ('thiscall',
             '(public: __thiscall std::auto_ptr<class pof::number_t>' +
             '::auto_ptr<class pof::number_t>(class std::auto_ptr' +
             '<class pof::number_t> &))'),
            ('',  "(const pof::number_t::`vftable')")]

        for expected, text in data:
            got = declarations.CALLING_CONVENTION_TYPES.extract(text)
            self.failUnless(
                got == expected, "Expected calling convention: %s, got %s" %
                (expected, got))


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(tester_t))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())

if __name__ == "__main__":
    run_suite()
