# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest

from pygccxml import parser
from pygccxml import utils


def test_config():
    """Test config setup with wrong xml generator setups."""

    # Some code to parse for the example
    code = "int a;"

    # Find the location of the xml generator (castxml)
    generator_path, name = utils.find_xml_generator()

    # No xml generator path
    config = parser.xml_generator_configuration_t(xml_generator=name)
    with pytest.raises(RuntimeError):
        parser.parse_string(code, config)

    # Invalid path
    config = parser.xml_generator_configuration_t(
        xml_generator_path="wrong/path",
        xml_generator=name)
    with pytest.raises(RuntimeError):
        parser.parse_string(code, config)

    # None path
    config = parser.xml_generator_configuration_t(
        xml_generator_path=None,
        xml_generator=name)
    with pytest.raises(RuntimeError):
        parser.parse_string(code, config)

    # No name
    config = parser.xml_generator_configuration_t(
        xml_generator_path=generator_path)
    with pytest.raises(RuntimeError):
        parser.parse_string(code, config)

    # Random name
    config = parser.xml_generator_configuration_t(
        xml_generator_path=generator_path,
        xml_generator="not_a_generator")
    with pytest.raises(RuntimeError):
        parser.parse_string(code, config)

    # None name
    config = parser.xml_generator_configuration_t(
        xml_generator_path=generator_path,
        xml_generator=None)
    with pytest.raises(RuntimeError):
        parser.parse_string(code, config)
