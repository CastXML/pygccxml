# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations

TEST_FILES = [
    "classes.hpp",
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


def test_global(global_ns):
    global_ns.class_('cls')
    global_ns.class_('::cls')


def test_typedefs(global_ns):
    global_ns.class_('cls2')
    global_ns.typedef('cls2')
    global_ns.class_('::cls2')

    global_ns.class_('cls3')
    global_ns.typedef('cls3')
    cls3 = global_ns.class_('::cls3')
    cls3.variable('i')


def test_ns1(global_ns):
    ns1 = global_ns.namespace('ns')

    global_ns.class_('nested_cls')
    with pytest.raises(Exception):
        global_ns.class_('ns::nested_cls')
    global_ns.class_('::ns::nested_cls')

    with pytest.raises(Exception):
        ns1.class_('::nested_cls')
    ns1.class_('nested_cls')
    ns1.class_('::ns::nested_cls')

    global_ns.class_('nested_cls2')
    with pytest.raises(Exception):
        global_ns.class_('ns::nested_cls2')
    global_ns.class_('::ns::nested_cls2')

    global_ns.class_('nested_cls3')
    with pytest.raises(Exception):
        global_ns.class_('ns::nested_cls3')
    global_ns.class_('::ns::nested_cls3')
