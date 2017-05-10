# Copyright 2014-2017 Insight Software Consortium.
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
        # TODO: once gccxml is removed; rename this to something like
        # annotate_tester
        self.header = "attributes_" + self.config.xml_generator + ".hpp"

    def setUp(self):
        # Reset flags before each test
        self.config.flags = ""

    def test_attributes(self):

        decls = parser.parse([self.header], self.config)
        Test.global_ns = declarations.get_global_namespace(decls)
        Test.global_ns.init_optimizer()

        numeric = self.global_ns.class_('numeric_t')
        do_nothing = numeric.member_function('do_nothing')
        arg = do_nothing.arguments[0]

        generator = self.config.xml_generator_from_xml_file
        if generator.is_castxml1 or \
            (generator.is_castxml and
                float(generator.xml_output_version) >= 1.137):
            # This works since:
            # https://github.com/CastXML/CastXML/issues/25
            # https://github.com/CastXML/CastXML/pull/26
            # https://github.com/CastXML/CastXML/pull/27
            # The version bump to 1.137 came way later but this is the
            # only way to make sure the test is running correctly
            self.assertTrue("annotate(sealed)" == numeric.attributes)
            self.assertTrue("annotate(no throw)" == do_nothing.attributes)
            self.assertTrue("annotate(out)" == arg.attributes)
            self.assertTrue(
                numeric.member_operators(name="=")[0].attributes is None)
        else:
            self.assertTrue("gccxml(no throw)" == do_nothing.attributes)
            self.assertTrue("gccxml(out)" == arg.attributes)

    def test_attributes_thiscall(self):
        """
        Test attributes with the "f2" flag

        """
        if self.config.compiler != "msvc":
            return

        self.config.flags = ["f2"]

        decls = parser.parse([self.header], self.config)
        Test.global_ns = declarations.get_global_namespace(decls)
        Test.global_ns.init_optimizer()

        numeric = self.global_ns.class_('numeric_t')
        do_nothing = numeric.member_function('do_nothing')
        arg = do_nothing.arguments[0]

        generator = self.config.xml_generator_from_xml_file
        if generator.is_castxml1 or (
                generator.is_castxml and
                float(generator.xml_output_version) >= 1.137):
            self.assertTrue("annotate(sealed)" == numeric.attributes)
            self.assertTrue("annotate(out)" == arg.attributes)

            self.assertTrue(
                "__thiscall__ annotate(no throw)" == do_nothing.attributes)
            self.assertTrue(
                numeric.member_operators(name="=")[0].attributes ==
                "__thiscall__")


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
