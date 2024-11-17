# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations

TEST_FILES = [
    "test_copy_constructor.hpp",
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


def test_copy_constructor(global_ns):
    """
    Check the is_copy_constructor method.

    This fails when using CastXML, see issue #27.

    """

    tclass = global_ns.class_("test")
    ctors = []
    for decl in tclass.declarations:
        if isinstance(decl, declarations.constructor_t):
            ctors.append(decl)

    # test::test(test const & t0) [copy constructor]
    assert declarations.is_copy_constructor(ctors[0])
    # test::test(float const & t0) [constructor]
    assert not declarations.is_copy_constructor(ctors[1])
    # test::test(myvar t0) [constructor]
    assert not declarations.is_copy_constructor(ctors[2])

    t2class = global_ns.class_("test2")
    ctors = []
    for decl in t2class.declarations:
        if isinstance(decl, declarations.constructor_t):
            ctors.append(decl)

    # test2::test2() [constructor]
    assert not declarations.is_copy_constructor(ctors[0])
    # test2::test2(test2 const & arg0) [copy constructor]
    assert declarations.is_copy_constructor(ctors[1])
