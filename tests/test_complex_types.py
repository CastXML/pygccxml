# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest

from . import autoconfig

from pygccxml import declarations
from pygccxml import parser


TEST_FILES = [
    "complex_types.hpp",
]


@pytest.fixture
def global_ns():
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    INIT_OPTIMIZER = True
    config = autoconfig.cxx_parsers_cfg.config.clone()
    config.castxml_epic_version = 1
    decls = parser.parse(TEST_FILES, config, COMPILATION_MODE)
    global_ns = declarations.get_global_namespace(decls)
    if INIT_OPTIMIZER:
        global_ns.init_optimizer()
    return global_ns


def test_complex_types():
    """
    This test tests presence of complex long double, float within
    FUNDAMENTAL_TYPES map
    """
    pass
    # TODO: write test