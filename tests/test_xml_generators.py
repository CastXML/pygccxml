# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest

import logging

from pygccxml import utils


mock_logger = logging.getLogger("Test")


def test_old_xml_generators():
    """
    Tests for the xml_generators class.

    This is for gccxml and for castxml using the gccxml xml file format
    """
    _test_impl("0.6", False, "is_gccxml_06")
    _test_impl("1.114", False, "is_gccxml_07")
    _test_impl("1.115", False, "is_gccxml_09_buggy")
    _test_impl("1.126", False, "is_gccxml_09_buggy")
    _test_impl("1.127", False, "is_gccxml_09")
    _test_impl("1.136", True, "is_castxml")


def test_casxtml_epic_version_1():
    """
    Test with the castxml epic version set to 1
    """
    gen = utils.xml_generators(
        mock_logger, castxml_format="1.1.0")
    assert gen.is_gccxml is False
    assert gen.is_castxml is True
    assert gen.is_castxml1 is True
    assert gen.xml_output_version == "1.1.0"

    with pytest.raises(RuntimeError):
        utils.xml_generators(mock_logger, "1.136", "1.1.0")

    with pytest.raises(RuntimeError):
        utils.xml_generators(mock_logger, None, None)


def _test_impl(
        gccxml_cvs_revision, is_castxml,
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
        mock_logger, gccxml_cvs_revision)
    if is_castxml:
        assert gen.is_gccxml is False
        assert gen.is_castxml is True
    else:
        assert gen.is_gccxml is True
        assert gen.is_castxml is False
    assert getattr(gen, expected_gccxml_cvs_revision) is True
    assert gen.xml_output_version == gccxml_cvs_revision
