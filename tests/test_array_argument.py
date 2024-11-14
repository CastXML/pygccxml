# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations

TEST_FILES = ['test_array_argument.hpp']


@pytest.fixture
def global_ns():
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    config = autoconfig.cxx_parsers_cfg.config.clone()
    config.cflags = "-std=c++11"
    decls = parser.parse(TEST_FILES, config, COMPILATION_MODE)
    global_ns = declarations.get_global_namespace(decls)
    global_ns.init_optimizer()
    return global_ns


def test_array_argument(global_ns):

    """
    Test to ensure that function arguments' array size are kept intact
    rather than presented as pointers.

    """

    criteria = declarations.calldef_matcher(name="function")
    free_funcs = declarations.matcher.find(criteria, global_ns)
    for free_func in free_funcs:
        decl_string = free_func.create_decl_string(with_defaults=False)
        assert decl_string == "void ( ::test::* )( int [1024],int [512] )"
        arg1 = free_func.arguments[0]
        arg2 = free_func.arguments[1]
        assert arg1.decl_type.decl_string == "int [1024]"
        assert arg1.name == "arg1"
        assert declarations.type_traits.array_size(arg1.decl_type) == 1024
        assert isinstance(
            declarations.type_traits.array_item_type(arg1.decl_type),
            declarations.cpptypes.int_t
        ) is True
        assert arg2.decl_type.decl_string == "int [512]"
        assert arg2.name == "arg2"
        assert declarations.type_traits.array_size(arg2.decl_type) == 512
        assert isinstance(
            declarations.type_traits.array_item_type(arg2.decl_type),
            declarations.cpptypes.int_t
        ) is True
