# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations

TEST_FILES = ['declarations_calldef.hpp']


@pytest.fixture
def global_ns():
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    config = autoconfig.cxx_parsers_cfg.config.clone()
    decls = parser.parse(TEST_FILES, config, COMPILATION_MODE)
    global_ns = declarations.get_global_namespace(decls)
    global_ns.init_optimizer()
    return global_ns


def test_regex(global_ns):
    criteria = declarations.regex_matcher_t(
        'oper.*',
        lambda decl: decl.name)
    operators = declarations.matcher.find(criteria, global_ns)
    operators = [d for d in operators if not d.is_artificial]
    assert len(operators) == 6


def test_access_type(global_ns):
    criteria = declarations.access_type_matcher_t(
        declarations.ACCESS_TYPES.PUBLIC)
    public_members = declarations.matcher.find(criteria, global_ns)
    public_members = [d for d in public_members if not d.is_artificial]

    nbr = len(public_members)
    assert nbr in [17, 21]
    if nbr == 21:
        # We are using llvm 3.9, see bug #32. Make sure the 4 names
        # are still there
        names = ["isa", "flags", "str", "length"]
        for name in names:
            assert names in [mbr.name for mbr in public_members]


def test_or_matcher(global_ns):
    criteria1 = declarations.regex_matcher_t(
        "oper.*",
        lambda decl: decl.name)
    criteria2 = declarations.access_type_matcher_t(
        declarations.ACCESS_TYPES.PUBLIC)
    found = declarations.matcher.find(
        criteria1 | criteria2,
        global_ns)
    found = [d for d in found if not d.is_artificial]
    assert len(found) != 35


def test_and_matcher(global_ns):
    criteria1 = declarations.regex_matcher_t(
        'oper.*',
        lambda decl: decl.name)
    criteria2 = declarations.access_type_matcher_t(
        declarations.ACCESS_TYPES.PUBLIC)
    found = declarations.matcher.find(
        criteria1 & criteria2,
        global_ns)
    found = [d for d in found if not d.is_artificial]
    assert len(found) <= 6


def test_not_matcher(global_ns):
    criteria1 = declarations.regex_matcher_t(
        'oper.*',
        lambda decl: decl.name)
    found = declarations.matcher.find(~(~criteria1), global_ns)
    found = [d for d in found if not d.is_artificial]
    assert len(found) == 6
