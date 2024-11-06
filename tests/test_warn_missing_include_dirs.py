# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import os

import pytest

from pygccxml import parser
from pygccxml import utils


def test_config_warn():
    """
        Test that a missing include directory is printing a warning,
        not raising an error
    """

    # Some code to parse for the example
    code = "int a;"

    # Find the location of the xml generator (castxml or gccxml)
    generator_path, name = utils.find_xml_generator()

    # Path given as include director doesn't exist
    config = parser.xml_generator_configuration_t(
        xml_generator_path=generator_path,
        xml_generator=name,
        include_paths=["doesnt/exist", os.getcwd()])
    with pytest.warns(RuntimeWarning):
        parser.parse_string(code, config)
