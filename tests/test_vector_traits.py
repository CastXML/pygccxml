# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations


TEST_FILES = [
    "vector_traits.hpp",
]


@pytest.fixture
def global_ns():
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    INIT_OPTIMIZER = True
    config = autoconfig.cxx_parsers_cfg.config.clone()
    # TOOD: this breaks the tests, check why
    # config.castxml_epic_version = 1
    decls = parser.parse(TEST_FILES, config, COMPILATION_MODE)
    global_ns = declarations.get_global_namespace(decls)
    if INIT_OPTIMIZER:
        global_ns.init_optimizer()
    return global_ns


def validate_yes(value_type, container):
    traits = declarations.vector_traits
    assert traits.is_my_case(container) is True
    assert declarations.is_same(
            value_type,
            traits.element_type(container)) is True
    assert traits.is_sequence(container) is True


def test_global_ns(global_ns):
    value_type = global_ns.class_('_0_')
    container = global_ns.typedef('container', recursive=False)
    validate_yes(value_type, container)


def test_yes(global_ns):
    yes_ns = global_ns.namespace('yes')
    for struct in yes_ns.classes():
        if not struct.name.startswith('_'):
            continue
        if not struct.name.endswith('_'):
            continue
        validate_yes(
            struct.typedef('value_type'),
            struct.typedef('container'))


def test_no(global_ns):
    traits = declarations.vector_traits
    no_ns = global_ns.namespace('no')
    for struct in no_ns.classes():
        if not struct.name.startswith('_'):
            continue
        if not struct.name.endswith('_'):
            continue
        assert traits.is_my_case(struct.typedef('container')) is False


def test_declaration():
    cnt = (
        'std::vector<std::basic_string<char, std::char_traits<char>, ' +
        'std::allocator<char>>,std::allocator<std::basic_string<char, ' +
        'std::char_traits<char>, std::allocator<char>>>>' +
        '@::std::vector<std::basic_string<char, std::char_traits<char>, ' +
        'std::allocator<char>>, std::allocator<std::basic_string<char, ' +
        'std::char_traits<char>, std::allocator<char>>>>')
    traits = declarations.find_container_traits(cnt)
    assert declarations.vector_traits == traits


def test_element_type(global_ns):
    do_nothing = global_ns.free_function('do_nothing')
    v = declarations.remove_reference(
        declarations.remove_declarated(
            do_nothing.arguments[0].decl_type))
    declarations.vector_traits.element_type(v)
