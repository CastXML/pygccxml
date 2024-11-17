# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations


TEST_FILES = [
    "declarations_calldef.hpp",
]


@pytest.fixture
def global_ns():
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    INIT_OPTIMIZER = True
    config = autoconfig.cxx_parsers_cfg.config.clone()
    config.castxml_epic_version = 1
    decls = parser.parse(TEST_FILES, config, COMPILATION_MODE)
    global_ns = declarations.get_global_namespace(decls)
    if INIT_OPTIMIZER:
        global_ns.init_optimizer()
    return global_ns


TEMPLATE = """
    //test generated declaration string using gcc(xml) compiler
    #include "declarations_calldef.hpp"
    void test_generated_decl_string( %s );
    """


def test_member_function(global_ns):
    config = autoconfig.cxx_parsers_cfg.config.clone()
    member_inline_call = \
        global_ns.member_function('member_inline_call')
    decls = parser.parse_string(
        TEMPLATE %
        member_inline_call.decl_string,
        config)
    assert decls is not None


def test_free_function(global_ns):
    config = autoconfig.cxx_parsers_cfg.config.clone()
    return_default_args = \
        global_ns.free_function('return_default_args')
    decls = parser.parse_string(
        TEMPLATE %
        return_default_args.decl_string,
        config)
    assert decls is not None


def test_all_mem_and_free_funs(global_ns):
    config = autoconfig.cxx_parsers_cfg.config.clone()
    ns = global_ns.namespace('::declarations::calldef')
    for f in ns.member_functions():
        decls = parser.parse_string(
            TEMPLATE % f.decl_string, config)
        assert decls is not None
    for f in ns.free_functions():
        decls = parser.parse_string(
            TEMPLATE % f.decl_string, config)
        assert decls is not None
