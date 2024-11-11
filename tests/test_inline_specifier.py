# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations

TEST_FILES = ["inline_specifier.hpp"]


@pytest.fixture
def global_ns():
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    config = autoconfig.cxx_parsers_cfg.config.clone()
    config.cflags = "-std=c++11"
    decls = parser.parse(TEST_FILES, config, COMPILATION_MODE)
    global_ns = declarations.get_global_namespace(decls)
    global_ns.init_optimizer()
    return global_ns


def test_inline_specifier(global_ns):
    inlined_funcs = global_ns.calldefs('inlined')
    assert len(inlined_funcs) != 0
    for f in inlined_funcs:
        assert f.has_inline is True

    not_inlined_funcs = global_ns.calldefs('not_inlined')
    assert len(not_inlined_funcs) != 0
    for f in not_inlined_funcs:
        assert f.has_inline is False
