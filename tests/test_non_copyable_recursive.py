# Copyright 2014-2016 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations

TEST_FILES = ["test_non_copyable_recursive.hpp"]


def test_infinite_recursion_base_classes():
    """
    Test find_noncopyable_vars

    See #71

    find_noncopyable_vars was throwing:
    RuntimeError: maximum recursion depth exceeded while
    calling a Python object
    """
    config = autoconfig.cxx_parsers_cfg.config.clone()
    decls = parser.parse(TEST_FILES, config)
    global_ns = declarations.get_global_namespace(decls)

    # Description of the problem (before the fix):
    # find_noncopyable_vars (on Child class) looks up the variables,
    # and finds aBasePtr2 (a pointer to the Base2 class).
    # Then it looks recursively at the base classes of Base2, and finds
    # Base1. Then, it looks up the variables from Base, to check if Base1
    # is non copyable. It finds another aBasePtr2 variable, which leads to
    # a new check of Base2; this recurses infinitely.
    test_ns = global_ns.namespace('Test1')
    cls = test_ns.class_('Child')
    declarations.type_traits_classes.find_noncopyable_vars(cls)
    assert declarations.type_traits_classes.is_noncopyable(cls) is True


def test_infinite_recursion_sstream():
    """
    Test find_noncopyable_vars

    See #71

    find_noncopyable_vars was throwing:
    RuntimeError: maximum recursion depth exceeded while
    calling a Python object
    """
    config = autoconfig.cxx_parsers_cfg.config.clone()
    decls = parser.parse(TEST_FILES, config)
    global_ns = declarations.get_global_namespace(decls)

    # Real life example of the bug. This leads to a similar error,
    # but the situation is more complex as there are multiple
    # classes that are related the one to the others
    # (basic_istream, basic_ios, ios_base, ...)
    test_ns = global_ns.namespace('Test2')
    cls = test_ns.class_('FileStreamDataStream')
    declarations.type_traits_classes.find_noncopyable_vars(cls)
    assert declarations.type_traits_classes.is_noncopyable(cls) is False
