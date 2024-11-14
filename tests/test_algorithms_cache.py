# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations


TEST_FILES = ['core_membership.hpp']


@pytest.fixture
def global_ns():
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    config = autoconfig.cxx_parsers_cfg.config.clone()
    decls = parser.parse(TEST_FILES, config, COMPILATION_MODE)
    global_ns = declarations.get_global_namespace(decls)
    global_ns.init_optimizer()
    return global_ns


def test_name_based(global_ns):
    cls = global_ns.class_(name='class_for_nested_enums_t')

    cls_full_name = declarations.full_name(cls)
    assert cls.cache.full_name == cls_full_name

    cls_declaration_path = declarations.declaration_path(cls)
    assert cls.cache.declaration_path == cls_declaration_path

    enum = cls.enumeration('ENestedPublic')

    enum_full_name = declarations.full_name(enum)
    assert enum.cache.full_name == enum_full_name

    enum_declaration_path = declarations.declaration_path(enum)
    assert enum.cache.declaration_path == enum_declaration_path

    # now we change class name, all internal decls cache should be cleared
    cls.name = "new_name"
    assert not cls.cache.full_name
    assert not cls.cache.declaration_path

    assert not enum.cache.full_name
    assert not enum.cache.declaration_path


def test_access_type(global_ns):
    cls = global_ns.class_(name='class_for_nested_enums_t')
    enum = cls.enumeration('ENestedPublic')
    assert enum.cache.access_type == 'public'
    enum.cache.reset_access_type()
    assert not enum.cache.access_type
    assert 'public' == cls.find_out_member_access_type(enum)
    assert enum.cache.access_type == 'public'
