# Copyright 2021 Insight Software Consortium.
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
        self.header = "test_deprecation.hpp"
        self.global_ns = None
        self.config.castxml_epic_version = 1

    def _check_text_content(self, desired_text, deprecation_string):
        if deprecation_string:
            self.assertEqual(desired_text, deprecation_string)
        else:
            print("No text in deprecation attribute to check")

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
        Check the comment parsing
        """

        if self.config.castxml_epic_version != 1:
            # Run this test only with castxml epic version == 1
            return
        tnamespace = self.global_ns.namespace("deprecation")

        tenumeration = tnamespace.enumeration("com_enum")
        self.assertIn("deprecation", dir(tenumeration))
        self._check_text_content('Enumeration is Deprecated',
                                 tenumeration.deprecation)

        tclass = tnamespace.class_("test")
        self.assertIn("deprecation", dir(tclass))
        self._check_text_content("Test class Deprecated", tclass.deprecation)

        tmethod = tclass.member_functions()[0]
        tmethod_dep = tclass.member_functions()[1]

        self.assertIn("deprecation", dir(tmethod))
        self.assertIsNone(tmethod.deprecation)
        self._check_text_content("Function is deprecated",
                                 tmethod_dep.deprecation)

        tconstructor = tclass.constructors()[0]
        tconstructor_dep = tclass.constructors()[1]

        self.assertIsNone(tconstructor.deprecation)
        self.assertIn("deprecation", dir(tconstructor_dep))
        self._check_text_content("One arg constructor is Deprecated",
                                 tconstructor_dep.deprecation)


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
