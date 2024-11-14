# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations


TEST_FILES = ['free_operators.hpp']


@pytest.fixture
def global_ns():
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    config = autoconfig.cxx_parsers_cfg.config.clone()
    decls = parser.parse(TEST_FILES, config, COMPILATION_MODE)
    global_ns = declarations.get_global_namespace(decls)
    global_ns.init_optimizer()
    return global_ns


def test_free_operators(global_ns):
    fo = global_ns.namespace('free_operators')
    number = fo.class_('number')
    rational = fo.class_('rational')
    for oper in fo.free_operators():
        if number.name in str(oper):
            assert number in oper.class_types
        if rational.name in str(oper):
            assert rational in oper.class_types
