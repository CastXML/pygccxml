# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations


TEST_FILES = [
    "type_as_exception_bug.h",
]


@pytest.fixture
def global_ns():
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    config = autoconfig.cxx_parsers_cfg.config.clone()
    # This test does not work with c++17 and above
    # See https://developers.redhat.com/articles/2021/08/06/porting-your-code-c17-gcc-11#exception_specification_changes # noqa
    # This test is thus excpected to use -std=c++14 forever
    config.cflags = "-std=c++14"
    decls = parser.parse(TEST_FILES, config, COMPILATION_MODE)
    global_ns = declarations.get_global_namespace(decls)
    return global_ns


def test_type_as_exception(global_ns):
    buggy = global_ns.member_function('buggy')
    expression_error = global_ns.class_('ExpressionError')
    assert len(buggy.exceptions) == 1
    err = buggy.exceptions[0]
    assert declarations.is_reference(err)
    err = declarations.remove_declarated(
        declarations.remove_reference(err))
    assert err is expression_error
