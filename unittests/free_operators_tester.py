# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import unittest

from . import parser_test_case

from pygccxml import parser
from pygccxml import declarations


class Test(parser_test_case.parser_test_case_t):

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.header = 'free_operators.hpp'
        self.global_ns = None

    def setUp(self):
        reader = parser.source_reader_t(self.config)
        decls = reader.read_file(self.header)
        self.global_ns = declarations.get_global_namespace(decls)

    def test(self):
        fo = self.global_ns.namespace('free_operators')
        number = fo.class_('number')
        rational = fo.class_('rational')
        for oper in fo.free_operators():
            if number.name in str(oper):
                self.assertTrue(number in oper.class_types)
            if rational.name in str(oper):
                self.assertTrue(rational in oper.class_types)


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
