# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations

TEST_FILES = ['test_order.hpp']


@pytest.fixture
def global_ns():
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    config = autoconfig.cxx_parsers_cfg.config.clone()
    decls = parser.parse(TEST_FILES, config, COMPILATION_MODE)
    global_ns = declarations.get_global_namespace(decls)
    global_ns.init_optimizer()
    return global_ns


def test_order(global_ns):
    """
    Test order of const, volatile, etc... in decl_string.

    The convention in pygccxml is that const and volatile qualifiers
    are placed on the right of their `base` type.

    """
    c1 = global_ns.variable("c1")
    c2 = global_ns.variable("c2")
    assert c1.decl_type.decl_string == "int const"
    assert c2.decl_type.decl_string == "int const"

    cptr1 = global_ns.variable("cptr1")
    cptr2 = global_ns.variable("cptr2")
    assert cptr1.decl_type.decl_string == "int const * const"
    assert cptr2.decl_type.decl_string == "int const * const"

    v1 = global_ns.variable("v1")
    v2 = global_ns.variable("v2")
    assert v1.decl_type.decl_string == "int volatile"
    assert v2.decl_type.decl_string == "int volatile"

    vptr1 = global_ns.variable("vptr1")
    vptr2 = global_ns.variable("vptr2")
    decl_string = "int volatile * volatile"
    assert vptr1.decl_type.decl_string == decl_string
    assert vptr2.decl_type.decl_string == decl_string

    cv1 = global_ns.variable("cv1")
    cv2 = global_ns.variable("cv2")
    cv3 = global_ns.variable("cv3")
    cv4 = global_ns.variable("cv4")
    assert cv1.decl_type.decl_string == "int const volatile"
    assert cv2.decl_type.decl_string == "int const volatile"
    assert cv3.decl_type.decl_string == "int const volatile"
    assert cv4.decl_type.decl_string == "int const volatile"

    cvptr1 = global_ns.variable("cvptr1")
    cvptr2 = global_ns.variable("cvptr2")
    cvptr3 = global_ns.variable("cvptr3")
    cvptr4 = global_ns.variable("cvptr4")
    decl_string = "int const volatile * const volatile"
    assert cvptr1.decl_type.decl_string == decl_string
    assert cvptr2.decl_type.decl_string == decl_string
    assert cvptr3.decl_type.decl_string == decl_string
    assert cvptr4.decl_type.decl_string == decl_string

    ac1 = global_ns.variable("ac1")
    ac2 = global_ns.variable("ac2")
    assert ac1.decl_type.decl_string, "int const [2]"
    assert ac2.decl_type.decl_string, "int const [2]"

    acptr1 = global_ns.variable("acptr1")
    acptr2 = global_ns.variable("acptr2")
    assert acptr1.decl_type.decl_string == "int const * const [2]"
    assert acptr2.decl_type.decl_string == "int const * const [2]"

    class_a = global_ns.variable("classA")
    assert class_a.decl_type.decl_string == "::A const"
