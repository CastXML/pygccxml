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
        self.header = "test_elaborated_types.hpp"

    def test_is_elaborated_type(self):
        """
        Test for the is_elaborated function
        """

        decls = parser.parse([self.header], self.config)
        global_ns = declarations.get_global_namespace(decls)

        if self.config.castxml_epic_version != 1:
            return

        if self.config.xml_generator_from_xml_file.is_castxml1:
            self._test_impl_yes(global_ns, "class")
            self._test_impl_yes(global_ns, "struct")
            self._test_impl_yes(global_ns, "enum")
            self._test_impl_yes(global_ns, "union")

            self._test_impl_no(global_ns, "class")
            self._test_impl_no(global_ns, "struct")
            self._test_impl_no(global_ns, "enum")
            self._test_impl_no(global_ns, "union")

    def _test_impl_yes(self, global_ns, specifier):
        yes = global_ns.namespace(name="::elaborated_t::yes_" + specifier)
        for decl in yes.declarations:
            self.assertTrue(
                declarations.is_elaborated(decl.decl_type))
            self.assertIn(specifier, str(decl.decl_type))

    def _test_impl_no(self, global_ns, specifier):
        no = global_ns.namespace(name="::elaborated_t::no_" + specifier)
        for decl in no.declarations:
            self.assertFalse(
                declarations.is_elaborated(decl.decl_type))
            self.assertNotIn(specifier, str(decl.decl_type))


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
