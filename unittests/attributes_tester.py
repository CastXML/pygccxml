# Copyright 2014-2016 Insight Software Consortium.
# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import unittest
import parser_test_case

from pygccxml import parser
from pygccxml import declarations
from pygccxml import utils


class tester_t(parser_test_case.parser_test_case_t):
    global_ns = None

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.header = "attributes_" + self.config.xml_generator + ".hpp"

    def setUp(self):
        if not tester_t.global_ns:
            decls = parser.parse([self.header], self.config)
            tester_t.global_ns = declarations.get_global_namespace(decls)
            tester_t.global_ns.init_optimizer()

    def test(self):

        if "CastXML" in utils.xml_generator:
            prefix = "annotate"
        else:
            prefix = "gccxml"

        numeric = self.global_ns.class_('numeric_t')

        # Dependending on the compiler, this attribute will be found
        # or not: never on OS X (clang and gcc),
        # always on ubuntu (clang and gcc). Just skip this test for the
        # moment.

        # self.assertTrue(None is numeric.attributes)

        do_nothing = numeric.mem_fun('do_nothing')
        self.assertTrue((prefix + "(no throw)") == do_nothing.attributes)
        arg = do_nothing.arguments[0]
        self.assertTrue((prefix + "(out)") == arg.attributes)


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(tester_t))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())

if __name__ == "__main__":
    run_suite()
