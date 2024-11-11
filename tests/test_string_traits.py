# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations


TEST_FILES = [
    "string_traits.hpp",
]


@pytest.fixture
def global_ns():
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    config = autoconfig.cxx_parsers_cfg.config.clone()
    decls = parser.parse(TEST_FILES, config, COMPILATION_MODE)
    global_ns = declarations.get_global_namespace(decls)
    global_ns.init_optimizer()
    return global_ns


def validate_yes(ns, controller):
    for typedef in ns.typedefs():
        assert controller(typedef.decl_type) is True


def validate_no(ns, controller):
    for typedef in ns.typedefs():
        assert controller(typedef.decl_type) is False


def test_string(global_ns):
    string_traits = global_ns.namespace('string_traits')
    validate_yes(
        string_traits.namespace('yes'),
        declarations.is_std_string)
    validate_no(
        string_traits.namespace('no'),
        declarations.is_std_string)


def test_wstring(global_ns):
    wstring_traits = global_ns.namespace('wstring_traits')
    validate_yes(
        wstring_traits.namespace('yes'),
        declarations.is_std_wstring)
    validate_no(
        wstring_traits.namespace('no'),
        declarations.is_std_wstring)
