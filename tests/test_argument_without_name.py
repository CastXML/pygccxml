# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations

TEST_FILES = ['test_argument_without_name.hpp']


@pytest.fixture
def global_ns():
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    config = autoconfig.cxx_parsers_cfg.config.clone()
    config.cflags = "-std=c++11"
    decls = parser.parse(TEST_FILES, config, COMPILATION_MODE)
    global_ns = declarations.get_global_namespace(decls)
    global_ns.init_optimizer()
    return global_ns


def test_argument_without_name(global_ns):
    """
    Test passing an object without name to a templated function.

    The test was failing when building the declaration string.
    The declaration string will be 'void (*)(  & )'. If the passed
    object had a name the result would then be 'void (*)(Name & )'.

    See bug #55

    """

    criteria = declarations.calldef_matcher(name="function")
    free_funcs = declarations.matcher.find(criteria, global_ns)
    for free_func in free_funcs:
        decl_string = free_func.create_decl_string(with_defaults=False)
        assert decl_string == "void (*)(  & )"
