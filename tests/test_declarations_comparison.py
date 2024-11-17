# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import copy

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations

TEST_FILES = [
    "declarations_comparison.hpp",
]


def test_comparison_declaration_by_declaration():
    config = autoconfig.cxx_parsers_cfg.config.clone()
    config.castxml_epic_version = 1
    parsed = parser.parse(TEST_FILES, config)
    copied = copy.deepcopy(parsed)
    parsed = declarations.make_flatten(parsed)
    copied = declarations.make_flatten(copied)
    parsed.sort()
    copied.sort()
    failuers = []
    for parsed_decl, copied_decl, index in \
            zip(parsed, copied, list(range(len(copied)))):

        if parsed_decl != copied_decl:
            failuers.append(
                ("__lt__ and/or __qe__ does not working " +
                    "properly in case of %s, %s, index %d") %
                (parsed_decl.__class__.__name__,
                    copied_decl.__class__.__name__, index))
    assert failuers == []


def test_comparison_from_reverse():
    config = autoconfig.cxx_parsers_cfg.config.clone()
    config.castxml_epic_version = 1
    parsed = parser.parse(TEST_FILES, config)
    copied = copy.deepcopy(parsed)
    parsed.sort()
    copied.reverse()
    copied.sort()
    x = parsed[4:6]
    x.sort()
    y = copied[4:6]
    y.sort()
    assert parsed == copied


def test___lt__transitivnost():
    ns_std = declarations.namespace_t(name='std')
    ns_global = declarations.namespace_t(name='::')
    ns_internal = declarations.namespace_t(name='ns')
    ns_internal.parent = ns_global
    ns_global.declarations.append(ns_internal)
    left2right = [ns_std, ns_global]
    right2left = [ns_global, ns_std]
    left2right.sort()
    right2left.sort()
    assert left2right == right2left


def test_same_declarations_different_intances():
    config = autoconfig.cxx_parsers_cfg.config.clone()
    config.castxml_epic_version = 1
    parsed = parser.parse(TEST_FILES, config)
    copied = copy.deepcopy(parsed)
    assert parsed == copied
