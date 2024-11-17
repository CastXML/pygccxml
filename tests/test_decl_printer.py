# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import sys
import pytest

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations


TEST_FILES = [
    'core_ns_join_1.hpp',
    'core_ns_join_2.hpp',
    'core_ns_join_3.hpp',
    'core_membership.hpp',
    'core_class_hierarchy.hpp',
    'core_types.hpp',
    'core_diamand_hierarchy_base.hpp',
    'core_diamand_hierarchy_derived1.hpp',
    'core_diamand_hierarchy_derived2.hpp',
    'core_diamand_hierarchy_final_derived.hpp',
    'core_overloads_1.hpp',
    'core_overloads_2.hpp',
    'typedefs_base.hpp',
]


@pytest.fixture
def decls():
    COMPILATION_MODE = parser.COMPILATION_MODE.FILE_BY_FILE
    config = autoconfig.cxx_parsers_cfg.config.clone()
    config.castxml_epic_version = 1
    decls = parser.parse(TEST_FILES, config, COMPILATION_MODE)
    return decls


def test_printer(decls):
    # Redirect sys.stdout to a class with a writer doing nothing
    # This greatly reduces the size of the test output and makes
    # test log files readable.
    # Note: flush needs to be defined; because if not this will
    # result in an AttributeError on call.
    class DontPrint(object):
        def write(*args):
            pass

        def flush(*args):
            pass
    sys.stdout = DontPrint()

    declarations.print_declarations(decls)


def test__str__(decls):
    decls = declarations.make_flatten(decls)
    for decl in decls:
        str(decl)
