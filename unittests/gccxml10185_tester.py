# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import unittest

from . import parser_test_case

from pygccxml import parser
from pygccxml import declarations

code = \
    """
template <typename T> struct A {};
template <int N> struct A<const char[N]>
{ static int size(const char[N]) { return N - 1; } };
"""


class Test(parser_test_case.parser_test_case_t):

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)

    def test(self):
        """
        The purpose of this test was to check if changes to GCCXML
        would lead to changes in the outputted xml file (Meaning
        the bug was fixed).

        GCCXML wrongly outputted partial template specialization.
        CastXML does not have this bug. In this case we check if
        the template specialization can not be found; which is the
        expected/wanted behaviour.

        https://github.com/CastXML/CastXML/issues/20

        """

        decls = parser.parse_string(code, self.config)
        global_ns = declarations.get_global_namespace(decls)
        self.assertRaises(
            declarations.declaration_not_found_t,
            lambda: global_ns.class_('A<const char [N]>'))


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
