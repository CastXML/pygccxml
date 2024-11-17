# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest

from . import autoconfig

from pygccxml import parser


def test_castxml_epic_version_check():
    """
    Test using a forbidden value for the castxml epic version.

    """

    config = autoconfig.cxx_parsers_cfg.config.clone()
    config.castxml_epic_version = 2
    with pytest.raises(RuntimeError):
        parser.parse_string("", config)
