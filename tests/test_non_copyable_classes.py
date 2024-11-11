# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations

TEST_FILES = ["non_copyable_classes.hpp"]


@pytest.fixture
def global_ns():
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    config = autoconfig.cxx_parsers_cfg.config.clone()
    config.cflags = "-std=c++11"
    decls = parser.parse(TEST_FILES, config, COMPILATION_MODE)
    global_ns = declarations.get_global_namespace(decls)
    global_ns.init_optimizer()
    return global_ns


def test(global_ns):
    """
    Search for classes which can not be copied.

    See bug #13

    1) non copyable class
    2) non copyable const variable (fundamental type)
    3) non copyable const variable (class type)
    4) non copyable const variable (array type)
    5) non copyable const variable (class type)

    """

    main_foo_1 = global_ns.class_('MainFoo1')
    assert declarations.is_noncopyable(main_foo_1) is True

    main_foo_2 = global_ns.class_('MainFoo2')
    assert declarations.is_noncopyable(main_foo_2) is True

    main_foo_3 = global_ns.class_('MainFoo3')
    assert declarations.is_noncopyable(main_foo_3) is True

    main_foo_4 = global_ns.class_('MainFoo4')
    assert declarations.is_noncopyable(main_foo_4) is True

    main_foo_5 = global_ns.class_('MainFoo5')
    assert declarations.is_noncopyable(main_foo_5) is True

    main_foo_6 = global_ns.class_('MainFoo6')
    assert declarations.is_noncopyable(main_foo_6) is False
