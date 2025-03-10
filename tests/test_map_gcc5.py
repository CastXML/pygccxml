# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import platform

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations

TEST_FILES = ["test_map_gcc5.hpp"]


def test_map_gcc5():
    """
    The code in test_map_gcc5.hpp was breaking pygccxml.

    Test that case (gcc5 + castxml + c++11).

    See issue #45 and #55

    """

    config = autoconfig.cxx_parsers_cfg.config.clone()
    if platform.system() == "Darwin":
        config.cflags = "-std=c++11 -Dat_quick_exit=atexit -Dquick_exit=exit"
        # https://fr.mathworks.com/matlabcentral/answers/2013982-clibgen-generatelibrarydefinition-error-the-global-scope-has-no-quick_exit-on-mac-m2#answer_1439856
        # https://github.com/jetbrains/kotlin/commit/d50f585911dedec5723213da8835707ac95e1c01
    else:
        config.cflags = "-std=c++11"

    decls = parser.parse(TEST_FILES, config)
    global_ns = declarations.get_global_namespace(decls)

    # This calldef is defined with gcc > 4.9 (maybe earlier, not tested)
    # and -std=c++11. Calling create_decl_string is failing with gcc.
    # With clang the calldef does not exist so the matcher
    # will just return an empty list, letting the test pass.
    # See the test_argument_without_name.py for an equivalent test,
    # which is not depending on the presence of the _M_clone_node
    # method in the stl_tree.h file.
    criteria = declarations.calldef_matcher(name="_M_clone_node")
    free_funcs = declarations.matcher.find(criteria, global_ns)
    for free_funcs in free_funcs:
        free_funcs.create_decl_string(with_defaults=False)
