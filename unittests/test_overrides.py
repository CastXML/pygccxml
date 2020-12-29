# Copyright 2014-2020 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import unittest

from . import parser_test_case

from pygccxml import parser
from pygccxml import declarations


class Test(parser_test_case.parser_test_case_t):
    global_ns = None

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.header = "test_overrides.hpp"
        self.global_ns = None
        self.config.castxml_epic_version = 1

    def setUp(self):

        if not self.global_ns:
            decls = parser.parse([self.header], self.config)
            Test.global_ns = declarations.get_global_namespace(decls)
            Test.xml_generator_from_xml_file = \
                self.config.xml_generator_from_xml_file
        self.xml_generator_from_xml_file = Test.xml_generator_from_xml_file

        self.global_ns = Test.global_ns

    def test(self):
        """
        Check that the override information is populated for the
        simple::goodbye function.  It should contain the decl for the
        base::goodbye function.  Base::goodbye has no override so it
        will be none
        """
        base = self.global_ns.class_("base").member_function("goodbye")
        override_decl = self.global_ns.class_("simple")\
                            .member_function("goodbye")

        self.assertTrue(base.overrides is None)
        self.assertFalse(override_decl.overrides is None)
        self.assertEqual(override_decl.overrides, base)


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
