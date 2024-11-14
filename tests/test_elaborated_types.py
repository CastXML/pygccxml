# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations


TEST_FILES = ['test_elaborated_types.hpp']


@pytest.fixture
def global_ns():
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    config = autoconfig.cxx_parsers_cfg.config.clone()
    config.castxml_epic_version = 1
    decls = parser.parse(TEST_FILES, config, COMPILATION_MODE)
    global_ns = declarations.get_global_namespace(decls)
    global_ns.init_optimizer()
    return global_ns


def test_is_elaborated_type(global_ns):
    """
    Test for the is_elaborated function
    """

    for specifier in ["class", "struct", "enum", "union"]:
        _test_impl_yes(specifier=specifier, global_ns=global_ns)
        _test_impl_no(specifier=specifier, global_ns=global_ns)
        _test_arg_impl(specifier=specifier, global_ns=global_ns)


def _test_impl_yes(specifier, global_ns):
    yes = global_ns.namespace(name="::elaborated_t::yes_" + specifier)
    for decl in yes.declarations:
        assert declarations.is_elaborated(decl.decl_type) is True


def _test_impl_no(specifier, global_ns):
    no = global_ns.namespace(name="::elaborated_t::no_" + specifier)
    for decl in no.declarations:
        assert declarations.is_elaborated(decl.decl_type) is False


def _test_arg_impl(specifier, global_ns):
    decls = global_ns.namespace(
        name="::elaborated_t::arguments_" + specifier)
    for decl in decls.declarations:
        # The first argument is not elaborated
        no = decl.arguments[0].decl_type
        # The second argument is always elaborated
        yes = decl.arguments[1].decl_type
        assert declarations.is_elaborated(yes) is True
        assert declarations.is_elaborated(no) is False
