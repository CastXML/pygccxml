# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations

TEST_FILES1 = ["bit_fields.hpp"]
TEST_FILES2 = ["unnamed_ns_bug.hpp"]


def test_namespace_matcher_get_single():
    config = autoconfig.cxx_parsers_cfg.config.clone()
    decls = parser.parse(TEST_FILES1, config)
    criteria = declarations.namespace_matcher_t(name='bit_fields')
    declarations.matcher.get_single(criteria, decls)
    assert str(criteria) == '(decl type==namespace_t) and (name==bit_fields)'


def test_namespace_matcher_allow_empty():
    config = autoconfig.cxx_parsers_cfg.config.clone()
    decls = parser.parse(TEST_FILES1, config)
    global_ns = declarations.get_global_namespace(decls)
    assert 0 == len(global_ns.namespaces('does not exist', allow_empty=True))


def test_namespace_matcher_upper():
    config = autoconfig.cxx_parsers_cfg.config.clone()
    decls = parser.parse(TEST_FILES2, config)
    declarations.matcher.get_single(
        declarations.namespace_matcher_t(name='::'), decls)
