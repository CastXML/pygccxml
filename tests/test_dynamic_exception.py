# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest

import warnings

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations


TEST_FILES = [
    "test_dynamic_exception.hpp",
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
    global_ns.init_optimizer()
    return global_ns


def test_calldef_with_throw(global_ns, helpers):
    calldef_with_throw = global_ns.free_function("calldef_with_throw")
    assert calldef_with_throw is not None
    helpers._test_calldef_exceptions(
        global_ns, calldef_with_throw,
        ["some_exception_t", "other_exception_t"]
    )

    calldef_with_throw = global_ns.calldef('calldef_with_throw')
    some_exception = global_ns.class_('some_exception_t')
    other_exception = global_ns.class_('other_exception_t')

    # Legacy way of fetching dependencies. Is still valid but deprecated
    warnings.simplefilter("ignore", Warning)
    dependencies_old = calldef_with_throw.i_depend_on_them()
    warnings.simplefilter("error", Warning)
    assert len(dependencies_old) == 3
    dependencies_old = [
        dependency for dependency in dependencies_old if
        dependency.depend_on_it in (some_exception, other_exception)]
    assert len(dependencies_old) == 2

    dependencies_new = declarations.get_dependencies_from_decl(
        calldef_with_throw)
    assert len(dependencies_new) == 3
    dependencies_new = [
        dependency for dependency in dependencies_new if
        dependency.depend_on_it in (some_exception, other_exception)]
    assert len(dependencies_new) == 2
