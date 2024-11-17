# Copyright 2014-2020 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations


@pytest.fixture
def global_ns_fixture():
    config = autoconfig.cxx_parsers_cfg.config.clone()
    config.castxml_epic_version = 1
    config.cflags = "-std=c++11"
    decls = parser.parse(["test_overrides.hpp"], config)
    global_ns = declarations.get_global_namespace(decls)
    return global_ns


def test_overrides(global_ns_fixture):
    """
    Check that the override information is populated for the
    simple::goodbye function. It should contain the decl for the
    base::goodbye function.  Base::goodbye has no override so it
    will be none
    """
    base = global_ns_fixture.class_("base").member_function("goodbye")
    override_decl = global_ns_fixture.class_("simple")\
                                     .member_function("goodbye")

    assert base.overrides is None
    assert override_decl.overrides is not None
    assert override_decl.overrides == base
