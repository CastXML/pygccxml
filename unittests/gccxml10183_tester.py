# Copyright 2014-2016 Insight Software Consortium.
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
template <typename> class A {};
template <typename T> void f(A<T> const& a){ A<__typeof__(a)>(); }
template void f<int>(A<int> const& a);
"""


class Test(parser_test_case.parser_test_case_t):

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)

    def test(self):
        src_reader = parser.source_reader_t(self.config)
        global_ns = declarations.get_global_namespace(
            src_reader.read_string(code))

        # TODO: demangled attribute does not existe for castxml
        # and will not be added. Remove this test once gccxml
        # support is dropped.
        if 'GCCXML' in utils.xml_generator:
            global_ns.decl('A<int>')
            f = global_ns.free_fun('f')
            self.assertTrue(f.demangled == 'void f<int>(A<int> const&)')


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
