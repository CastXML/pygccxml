# Copyright 2014-2020 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest
import platform

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations


@pytest.fixture
def global_ns_fixture():
    config = autoconfig.cxx_parsers_cfg.config.clone()
    config.castxml_epic_version = 1
    if platform.system() == "Darwin":
        config.cflags = "-std=c++11 -Dat_quick_exit=atexit -Dquick_exit=exit"
        # https://fr.mathworks.com/matlabcentral/answers/2013982-clibgen-generatelibrarydefinition-error-the-global-scope-has-no-quick_exit-on-mac-m2#answer_1439856
        # https://github.com/jetbrains/kotlin/commit/d50f585911dedec5723213da8835707ac95e1c01
    else:
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
