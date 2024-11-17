# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations

TEST_FILES = ['test_function_pointer.hpp']


@pytest.fixture
def global_ns():
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    config = autoconfig.cxx_parsers_cfg.config.clone()
    decls = parser.parse(TEST_FILES, config, COMPILATION_MODE)
    global_ns = declarations.get_global_namespace(decls)
    global_ns.init_optimizer()
    return global_ns


def test_function_pointer(global_ns):
    """
    Test working with pointers and function pointers.

    """

    # Test on a function pointer
    criteria = declarations.variable_matcher(name="func1")
    variables = declarations.matcher.find(criteria, global_ns)

    assert variables[0].name == "func1"
    assert isinstance(variables[0].decl_type, declarations.pointer_t) is True
    assert str(variables[0].decl_type) == "void (*)( int,double )"
    assert declarations.is_calldef_pointer(variables[0].decl_type) is True
    assert isinstance(
        declarations.remove_pointer(variables[0].decl_type),
        declarations.free_function_type_t
        ) is True

    # Get the function (free_function_type_t) and test the return and
    # argument types
    function = variables[0].decl_type.base
    assert isinstance(function.return_type, declarations.void_t)
    assert isinstance(function.arguments_types[0], declarations.int_t)
    assert isinstance(function.arguments_types[1], declarations.double_t)

    # Test on a normal pointer
    criteria = declarations.variable_matcher(name="myPointer")
    variables = declarations.matcher.find(criteria, global_ns)

    assert variables[0].name == "myPointer"
    assert isinstance(variables[0].decl_type, declarations.pointer_t)
    assert declarations.is_calldef_pointer(variables[0].decl_type) is False
    assert isinstance(
        declarations.remove_pointer(variables[0].decl_type),
        declarations.volatile_t
        ) is True

    # Test on function pointer in struct (x8)
    for d in global_ns.declarations:
        if d.name == "x8":
            assert isinstance(d.decl_type, declarations.pointer_t) is True
            assert declarations.is_calldef_pointer(d.decl_type)
            assert isinstance(
                declarations.remove_pointer(d.decl_type),
                declarations.member_function_type_t
                ) is True
            assert str(declarations.remove_pointer(d.decl_type)) == \
                "void ( ::some_struct_t::* )(  )"
