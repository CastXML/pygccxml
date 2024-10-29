# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations

TEST_FILES = [
    # TODO: once gccxml is removed; rename this to something like
    # annotate_tester
    "attributes_castxml.hpp",
]


@pytest.fixture
def global_ns():
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    INIT_OPTIMIZER = True
    config = autoconfig.cxx_parsers_cfg.config.clone()
    decls = parser.parse(TEST_FILES, config, COMPILATION_MODE)
    global_ns = declarations.get_global_namespace(decls)
    if INIT_OPTIMIZER:
        global_ns.init_optimizer()
    return global_ns


def test_attributes(global_ns):
    numeric = global_ns.class_('numeric_t')
    do_nothing = numeric.member_function('do_nothing')
    arg = do_nothing.arguments[0]
    assert "annotate(sealed)" == numeric.attributes
    assert "annotate(no throw)" == do_nothing.attributes
    assert "annotate(out)" == arg.attributes
    assert numeric.member_operators(name="=")[0].attributes is None


def test_attributes_thiscall():
    """
    Test attributes with the "f2" flag

    """

    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    config = autoconfig.cxx_parsers_cfg.config.clone()

    config.flags = ["f2"]
    config.castxml_epic_version = 1

    decls = parser.parse(TEST_FILES, config, COMPILATION_MODE)
    global_ns = declarations.get_global_namespace(decls)
    global_ns.init_optimizer()

    numeric = global_ns.class_('numeric_t')
    do_nothing = numeric.member_function('do_nothing')
    arg = do_nothing.arguments[0]

    assert "annotate(sealed)" == numeric.attributes
    assert "annotate(out)" == arg.attributes

    assert "annotate(no throw)" == do_nothing.attributes
    assert numeric.member_operators(name="=")[0].attributes is None
