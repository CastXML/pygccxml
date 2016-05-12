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
        # TODO: once gccxml is removed; rename this to something like
        # annotate_tester
        self.header = "attributes_" + self.config.xml_generator + ".hpp"

    def setUp(self):
        if not tester_t.global_ns:
            decls = parser.parse([self.header], self.config)
            tester_t.global_ns = declarations.get_global_namespace(decls)
            tester_t.global_ns.init_optimizer()

    def test(self):

        numeric = self.global_ns.class_('numeric_t')
        do_nothing = numeric.mem_fun('do_nothing')
        arg = do_nothing.arguments[0]

        if "CastXML" in utils.xml_generator:
            if utils.xml_output_version >= 1.137:
                # This works since:
                # https://github.com/CastXML/CastXML/issues/25
                # https://github.com/CastXML/CastXML/pull/26
                # https://github.com/CastXML/CastXML/pull/27
                # The version bump to 1.137 came way later but this is the
                # only way to make sure the test is running correctly
                self.assertTrue("annotate(sealed)" == numeric.attributes)
                self.assertTrue("annotate(no throw)" == do_nothing.attributes)
                self.assertTrue("annotate(out)" == arg.attributes)
        else:
            self.assertTrue("gccxml(no throw)" == do_nothing.attributes)
            self.assertTrue("gccxml(out)" == arg.attributes)


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(tester_t))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())

if __name__ == "__main__":
    run_suite()
