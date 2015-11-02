# Copyright 2014-2015 Insight Software Consortium.
# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import unittest
import parser_test_case

from pygccxml import parser
from pygccxml import declarations
from pygccxml import utils

code = \
    """
template <typename T> struct A {};
template <int N> struct A<const char[N]>
{ static int size(const char[N]) { return N - 1; } };
"""


class tester_t(parser_test_case.parser_test_case_t):

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

        src_reader = parser.source_reader_t(self.config)
        global_ns = declarations.get_global_namespace(
            src_reader.read_string(code))
        if 'GCCXML' in utils.xml_generator:
            a = global_ns.class_('A<const char [N]>')
            a.mem_fun('size')
        elif 'CastXML' in utils.xml_generator:
            self.assertRaises(
                global_ns.declaration_not_found_t,
                lambda: global_ns.class_('A<const char [N]>'))


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(tester_t))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())

if __name__ == "__main__":
    run_suite()
