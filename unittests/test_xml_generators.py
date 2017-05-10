# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import unittest
import logging

from . import parser_test_case

from pygccxml import utils


class Test(parser_test_case.parser_test_case_t):
    mock_logger = logging.getLogger("Test")

    def test_old_xml_generators(self):
        """
        Tests for the xml_generators class.

        This is for gccxml and for castxml using the gccxml xml file format
        """
        self._test_impl("0.6", False, "is_gccxml_06")
        self._test_impl("1.114", False, "is_gccxml_07")
        self._test_impl("1.115", False, "is_gccxml_09_buggy")
        self._test_impl("1.126", False, "is_gccxml_09_buggy")
        self._test_impl("1.127", False, "is_gccxml_09")
        self._test_impl("1.136", True, "is_castxml")

    def test_casxtml_epic_version_1(self):
        """
        Test with the castxml epic version set to 1
        """
        gen = utils.xml_generators(
            self.mock_logger, castxml_format="1.1.0")
        self.assertFalse(gen.is_gccxml)
        self.assertTrue(gen.is_castxml)
        self.assertTrue(gen.is_castxml1)
        self.assertEqual(gen.xml_output_version, "1.1.0")

        self.assertRaises(RuntimeError, lambda: utils.xml_generators(
            self.mock_logger, "1.136", "1.1.0"))

        self.assertRaises(RuntimeError, lambda: utils.xml_generators(
            self.mock_logger, None, None))

    def _test_impl(
            self, gccxml_cvs_revision, is_castxml,
            expected_gccxml_cvs_revision):
        """
        Implementation detail for the test

        Args:
            gccxml_cvs_revision (str|None) : a known cvs revision
            is_castxml (bool): check for castxml
            expected_gccxml_cvs_revision (str): will be used to check if the
                attribute is set to True.
        """
        gen = utils.xml_generators(
            self.mock_logger, gccxml_cvs_revision)
        if is_castxml:
            self.assertFalse(gen.is_gccxml)
            self.assertTrue(gen.is_castxml)
        else:
            self.assertTrue(gen.is_gccxml)
            self.assertFalse(gen.is_castxml)
        self.assertTrue(getattr(gen, expected_gccxml_cvs_revision))
        self.assertEqual(gen.xml_output_version, gccxml_cvs_revision)


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
