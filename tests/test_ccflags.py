# Copyright 2014-2021 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations


TEST_FILES = [
    "test_ccflags.hpp",
]

COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE


@pytest.fixture
def config():
    config = autoconfig.cxx_parsers_cfg.config.clone()
    config.castxml_epic_version = 1
    config.append_cflags("-fopenmp")
    return config


def test_ccflags(config):
    # First check that macro is not defined.
    decls = parser.parse(TEST_FILES, config, COMPILATION_MODE)
    global_ns = declarations.get_global_namespace(decls)

    namespace_names = [
        n.name for n in global_ns.namespaces(allow_empty=True)
    ]
    assert "ccflags_test_namespace" not in namespace_names

    # Next check that macro is defined when passed directly as ccflag

    if "clang++" in config.compiler_path:
        config.append_ccflags("-Xpreprocessor")
    config.append_ccflags("-fopenmp")

    decls = parser.parse(TEST_FILES, config, COMPILATION_MODE)
    global_ns = declarations.get_global_namespace(decls)

    namespace_names = [n.name for n in global_ns.namespaces()]
    assert "ccflags_test_namespace" in namespace_names
