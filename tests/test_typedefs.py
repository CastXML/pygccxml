# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations


def test_typedefs_src_reader():
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    header = 'typedefs_base.hpp'
    config = autoconfig.cxx_parsers_cfg.config.clone()
    decls = parser.parse([header], config)
    global_ns = declarations.find_declaration(
        decls,
        decl_type=declarations.namespace_t,
        name='::')
    global_ns.init_optimizer()

    item_cls = global_ns.class_(name='item_t')
    assert item_cls is not None
    assert len(item_cls.aliases) == 1
    assert item_cls.aliases[0].name == 'Item'


def test_typedefs_source_reader():
    COMPILATION_MODE = parser.COMPILATION_MODE.FILE_BY_FILE
    config = autoconfig.cxx_parsers_cfg.config.clone()

    decls = parser.parse(
        ['typedefs1.hpp', 'typedefs2.hpp'],
        config,
        COMPILATION_MODE
    )
    item_cls = declarations.find_declaration(
        decls,
        decl_type=declarations.class_t,
        name='item_t')
    assert item_cls is not None
    assert len(item_cls.aliases) == 3
    expected_aliases = {'Item', 'Item1', 'Item2'}
    real_aliases = set([typedef.name for typedef in item_cls.aliases])
    assert real_aliases == expected_aliases
