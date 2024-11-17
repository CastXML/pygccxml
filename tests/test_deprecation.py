# Copyright 2021 Insight Software Consortium.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations


TEST_FILES = [
    "test_deprecation.hpp",
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


def _check_text_content(desired_text, deprecation_string):
    assert desired_text == deprecation_string


def test_comment_deprecation(global_ns):
    """
    Check the comment parsing
    """

    tnamespace = global_ns.namespace("deprecation")

    tenumeration = tnamespace.enumeration("com_enum")
    assert "deprecation" in dir(tenumeration)
    _check_text_content(
        'Enumeration is Deprecated',
        tenumeration.deprecation)

    tclass = tnamespace.class_("test")
    assert "deprecation" in dir(tclass)
    _check_text_content(
        "Test class Deprecated",
        tclass.deprecation)

    tmethod = tclass.member_functions()[0]
    tmethod_dep = tclass.member_functions()[1]

    assert "deprecation", dir(tmethod)
    assert tmethod.deprecation is None
    _check_text_content(
        "Function is deprecated",
        tmethod_dep.deprecation)

    tconstructor = tclass.constructors()[0]
    tconstructor_dep = tclass.constructors()[1]

    assert tconstructor.deprecation is None
    assert "deprecation" in dir(tconstructor_dep)
    _check_text_content(
        "One arg constructor is Deprecated",
        tconstructor_dep.deprecation)
