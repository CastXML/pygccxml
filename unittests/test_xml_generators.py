# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import unittest
import logging
import parser_test_case

from pygccxml import utils


class Test(parser_test_case.parser_test_case_t):

    def test_xml_generators(self):
        """
        Tests for the xml_generators class.
        """
        self._test_impl(None, False, "is_gccxml_06")
        self._test_impl(1.114, False, "is_gccxml_07")
        self._test_impl(1.115, False, "is_gccxml_09_buggy")
        self._test_impl(1.126, False, "is_gccxml_09_buggy")
        self._test_impl(1.127, False, "is_gccxml_09")
        self._test_impl(1.136, True, "is_castxml")

    def _test_impl(self, version, is_castxml, expected_version):
        gen = utils.xml_generators(logging.getLogger("Test"), version)
        if is_castxml:
            self.assertFalse(gen.is_gccxml)
            self.assertTrue(gen.is_castxml)
        else:
            self.assertTrue(gen.is_gccxml)
            self.assertFalse(gen.is_castxml)
        self.assertTrue(getattr(gen, expected_version))
        self.assertEqual(gen.xml_output_version, version)


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
