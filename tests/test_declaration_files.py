# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import os

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations


TEST_FILES = [
    'core_ns_join_1.hpp',
    'core_ns_join_2.hpp',
    'core_ns_join_3.hpp',
    'core_membership.hpp',
    'core_class_hierarchy.hpp',
    'core_types.hpp',
    'core_diamand_hierarchy_base.hpp',
    'core_diamand_hierarchy_derived1.hpp',
    'core_diamand_hierarchy_derived2.hpp',
    'core_diamand_hierarchy_final_derived.hpp',
    'core_overloads_1.hpp',
    'core_overloads_2.hpp',
    'typedefs_base.hpp',
]


def test_declaration_files():
    config = autoconfig.cxx_parsers_cfg.config.clone()
    prj_reader = parser.project_reader_t(config)
    decls = prj_reader.read_files(
        TEST_FILES,
        compilation_mode=parser.COMPILATION_MODE.ALL_AT_ONCE)
    files = declarations.declaration_files(decls)
    result = set()
    for fn in files:
        result.add(os.path.split(fn)[1])
    assert set(TEST_FILES).issubset(result) is True
