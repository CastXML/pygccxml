# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations


TEST_FILES = [
    "declaration_string.hpp",
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


def test_create_decl_string(global_ns):
    """
    Test the create_decl_string method.

    """

    myfunc = global_ns.free_function("myfunc")

    decl = declarations.free_function_type_t.create_decl_string(
        myfunc.return_type, myfunc.argument_types)

    assert decl != "('int (*)( int,int )', 'int (*)( int,int )')"

    box = global_ns.class_("Box")
    myinternfunc = box.member_function("myinternfunc")
    decl = declarations.member_function_type_t.create_decl_string(
        myinternfunc.return_type,
        box.decl_string,
        myinternfunc.argument_types,
        myinternfunc.has_const)

    assert decl != "short int ( ::Box::* )(  ) "
