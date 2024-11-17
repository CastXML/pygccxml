# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations


TEST_FILES = ['find_noncopyable_vars.hpp']


@pytest.fixture
def global_ns():
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    config = autoconfig.cxx_parsers_cfg.config.clone()
    decls = parser.parse(TEST_FILES, config, COMPILATION_MODE)
    global_ns = declarations.get_global_namespace(decls)
    global_ns.init_optimizer()
    return global_ns


def test_find_noncopyable_vars(global_ns):
    """
    Test the find_noncopyable_vars function

    """

    # The ptr1 variable in the holder struct can be copied,
    # but not the ptr2 variable
    holder = global_ns.class_("holder")
    nc_vars = declarations.find_noncopyable_vars(holder)
    assert len(nc_vars) == 1
    assert nc_vars[0].name == "ptr2"
    assert declarations.is_pointer(nc_vars[0].decl_type) is True
    assert declarations.is_const(nc_vars[0].decl_type) is True
