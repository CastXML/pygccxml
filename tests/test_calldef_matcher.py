# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations


TEST_FILES = [
    "declarations_calldef.hpp",
]


@pytest.fixture
def decls():
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    config = autoconfig.cxx_parsers_cfg.config.clone()
    decls = parser.parse(TEST_FILES, config, COMPILATION_MODE)
    return decls


def test_calldef_matcher(decls):
    criteria = declarations.calldef_matcher_t(
        name='return_default_args',
        return_type='int',
        arg_types=[None, declarations.bool_t()])
    rda = declarations.matcher.get_single(criteria, decls)
    assert rda is not None
