# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations


TEST_FILES = [
    'test_smart_pointer.hpp'
]


@pytest.fixture
def global_ns():
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    config = autoconfig.cxx_parsers_cfg.config.clone()
    config.cflags = "-std=c++11"
    decls = parser.parse(TEST_FILES, config, COMPILATION_MODE)
    global_ns = declarations.get_global_namespace(decls)
    global_ns.init_optimizer()
    return global_ns


def test_is_smart_pointer(global_ns):
    """
    Test smart_pointer_traits.is_smart_pointer method.

    """

    criteria = declarations.declaration_matcher(name="yes1")
    decls = declarations.matcher.find(criteria, global_ns)
    assert declarations.smart_pointer_traits.is_smart_pointer(
        decls[0].decl_type) is True

    criteria = declarations.declaration_matcher(name="no1")
    decls = declarations.matcher.find(criteria, global_ns)
    assert declarations.smart_pointer_traits.is_smart_pointer(
            decls[0].decl_type) is False

    criteria = declarations.declaration_matcher(name="no2")
    decls = declarations.matcher.find(criteria, global_ns)
    assert declarations.smart_pointer_traits.is_smart_pointer(
            decls[0].decl_type) is False


def test_is_auto_pointer(global_ns):
    """
    Test auto_ptr_traits.is_smart_pointer method.

    """

    criteria = declarations.declaration_matcher(name="yes2")
    decls = declarations.matcher.find(criteria, global_ns)
    assert declarations.auto_ptr_traits.is_smart_pointer(
        decls[0].decl_type) is True

    criteria = declarations.declaration_matcher(name="no1")
    decls = declarations.matcher.find(criteria, global_ns)
    assert declarations.auto_ptr_traits.is_smart_pointer(
        decls[0].decl_type) is False

    criteria = declarations.declaration_matcher(name="no2")
    decls = declarations.matcher.find(criteria, global_ns)
    assert declarations.auto_ptr_traits.is_smart_pointer(
        decls[0].decl_type) is False


def test_smart_pointer_value_type(global_ns):
    """
    Test smart_pointer_traits.value_type method.

    """

    criteria = declarations.declaration_matcher(name="yes1")
    decls = declarations.matcher.find(criteria, global_ns)
    vt = declarations.smart_pointer_traits.value_type(decls[0].decl_type)
    assert isinstance(vt, declarations.int_t) is True


def test_auto_pointer_value_type(global_ns):
    """
    Test auto_pointer_traits.value_type method.

    """

    criteria = declarations.declaration_matcher(name="yes2")
    decls = declarations.matcher.find(criteria, global_ns)
    vt = declarations.auto_ptr_traits.value_type(decls[0].decl_type)
    assert isinstance(vt, declarations.double_t) is True
