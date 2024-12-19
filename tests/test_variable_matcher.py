# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import os

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations


TEST_FILES1 = [
    "bit_fields.hpp",
]

TEST_FILES2 = [
    "vector_traits.hpp",
]


def test_bit_fields():
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    config = autoconfig.cxx_parsers_cfg.config.clone()
    decls = parser.parse(TEST_FILES1, config, COMPILATION_MODE)

    criteria = declarations.variable_matcher_t(
        name='x',
        decl_type='unsigned int')
    x = declarations.matcher.get_single(criteria, decls)

    comp_str = (
        '(decl type==variable_t) and (name==x) and ' +
        '(value type==unsigned int)')
    assert str(criteria) == comp_str

    criteria = declarations.variable_matcher_t(
        name='::bit_fields::fields_t::x',
        decl_type=declarations.unsigned_int_t(),
        header_dir=os.path.dirname(
            x.location.file_name),
        header_file=x.location.file_name)

    x = declarations.matcher.get_single(criteria, decls)
    assert x is not None
    assert 'public' == x.access_type


def test_no_defaults():
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    config = autoconfig.cxx_parsers_cfg.config.clone()
    decls = parser.parse(TEST_FILES2, config, COMPILATION_MODE)
    global_ns = declarations.get_global_namespace(decls)

    global_ns.decls(lambda decl: 'vector<' in decl.name)
    global_ns.decl('vector<_0_>')
    global_ns.class_('vector<std::vector<int>>')
    global_ns.class_('vector<std::string>')
    global_ns.decl('vector<const int>')
