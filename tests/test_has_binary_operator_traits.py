# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations

TEST_FILES = ["has_public_binary_operator_traits.hpp"]


@pytest.fixture
def global_ns():
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    config = autoconfig.cxx_parsers_cfg.config.clone()
    decls = parser.parse(TEST_FILES, config, COMPILATION_MODE)
    global_ns = declarations.get_global_namespace(decls)
    global_ns.init_optimizer()
    return global_ns


def test_yes_equal(global_ns):
    yes_ns = global_ns.namespace('yesequal')
    for typedef in yes_ns.typedefs():
        assert declarations.has_public_equal(typedef) is True


def test_no_equal(global_ns):
    no_ns = global_ns.namespace('noequal')
    for typedef in no_ns.typedefs():
        assert declarations.has_public_equal(typedef) is False


def test_yes_less(global_ns):
    yes_ns = global_ns.namespace('yesless')
    for typedef in yes_ns.typedefs():
        assert declarations.has_public_less(typedef)


def test_no_less(global_ns):
    no_ns = global_ns.namespace('noless')
    for typedef in no_ns.typedefs():
        assert declarations.has_public_less(typedef) is False
