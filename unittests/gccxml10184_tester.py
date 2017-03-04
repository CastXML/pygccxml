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
class A {
public:
    virtual ~A() = 0;
    unsigned int a : 1;
    unsigned int unused : 31;
};
"""


class Test(parser_test_case.parser_test_case_t):

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)

    def test(self):
        decls = parser.parse_string(code, self.config)
        global_ns = declarations.get_global_namespace(decls)
        self.assertTrue(global_ns.variable('a').bits == 1)
        self.assertTrue(global_ns.variable('unused').bits == 31)


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
