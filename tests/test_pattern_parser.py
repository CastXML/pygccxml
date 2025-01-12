# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest
import platform

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations


TEST_FILES = [
    'test_pattern_parser.hpp'
]


@pytest.fixture
def global_ns():
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    config = autoconfig.cxx_parsers_cfg.config.clone()
    if platform.system() == "Darwin":
        config.cflags = "-std=c++11 -Dat_quick_exit=atexit -Dquick_exit=exit"
        # https://fr.mathworks.com/matlabcentral/answers/2013982-clibgen-generatelibrarydefinition-error-the-global-scope-has-no-quick_exit-on-mac-m2#answer_1439856
        # https://github.com/jetbrains/kotlin/commit/d50f585911dedec5723213da8835707ac95e1c01
    else:
        config.cflags = "-std=c++11"
    decls = parser.parse(TEST_FILES, config, COMPILATION_MODE)
    global_ns = declarations.get_global_namespace(decls)
    global_ns.init_optimizer()
    return global_ns


def test_template_split_std_vector(global_ns):
    """
    Demonstrate error in pattern parser, see #60

    """

    config = autoconfig.cxx_parsers_cfg.config.clone()
    if platform.system() == "Darwin":
        config.cflags = "-std=c++11 -Dat_quick_exit=atexit -Dquick_exit=exit"
        # https://fr.mathworks.com/matlabcentral/answers/2013982-clibgen-generatelibrarydefinition-error-the-global-scope-has-no-quick_exit-on-mac-m2#answer_1439856
        # https://github.com/jetbrains/kotlin/commit/d50f585911dedec5723213da8835707ac95e1c01
    else:
        config.cflags = "-std=c++11"
    decls = parser.parse(TEST_FILES, config)

    for decl in declarations.make_flatten(decls):
        if "myClass" in decl.name:
            _ = decl.partial_name


def test_matcher(global_ns):
    """
    Run the matcher on all the templated classes.

    This exercises the whole pipeline even more.

    """

    criteria = declarations.declaration_matcher(name="myClass")
    _ = declarations.matcher.find(criteria, global_ns)


def test_split():
    """
    Test a bunch of tricky name/args splits. More combinations could be
    tested but this is already covering most of the cases.

    In test_template_split_std_vector we test for a specific case that
    was failing (in a real world scenario).
    Here we test more possible combinations to make sure the splitting
    method is robust enough.

    """

    p1 = "std::vector<char, std::allocator<char> >"
    p2 = "std::vector<int, std::allocator<int> >"
    args_list = [
        "const std::basic_string<char> &", "const int &", "const double &"]

    for arg in args_list:

        li = [p1]
        name, args = declarations.templates.split(
            "myClass0a<" + ", ".join(li) + ">")
        assert name == "myClass0a"
        assert args == li

        li = [p1, p2]
        name, args = declarations.templates.split(
            "myClass0b<" + ", ".join(li) + ">")
        assert name == "myClass0b"
        assert args == li

        li = [p1, p2, p2]
        name, args = declarations.templates.split(
            "myClass0c<" + ", ".join(li) + ">")
        assert name == "myClass0c"
        assert args == li

        li = [p1 + " (" + arg + ")"]
        name, args = declarations.templates.split(
            "myClass1<" + ", ".join(li) + ">")
        assert name == "myClass1"
        assert args == li

        li = [p1 + " (" + arg + ", " + arg + ")"]
        name, args = declarations.templates.split(
            "myClass2<" + ", ".join(li) + ">")
        assert name == "myClass2"
        assert args == li

        li = [p2 + " (" + arg + ", " + arg + ")"]
        name, args = declarations.templates.split(
            "myClass3<" + ", ".join(li) + ">")
        assert name == "myClass3"
        assert args == li

        li = [p1 + " (" + arg + ", " + arg + ", " + arg + ")"]
        name, args = declarations.templates.split(
            "myClass4<" + ", ".join(li) + ">")
        assert name == "myClass4"
        assert args == li

        li = [
            p1 + " (" + arg + ", " + arg + ", " + arg + ")",
            p1]
        name, args = declarations.templates.split(
            "myClass5<" + ", ".join(li) + ">")
        assert name == "myClass5"
        assert args == li

        li = [
            p1,
            p1 + " (" + arg + ", " + arg + ", " + arg + ")"]
        name, args = declarations.templates.split(
            "myClass6<" + ", ".join(li) + ">")
        assert name == "myClass6"
        assert args == li

        li = [
            p2 + " (" + arg + ")",
            p1,
            p1 + " (" + arg + ", " + arg + ", " + arg + ")"]
        name, args = declarations.templates.split(
            "myClass7<" + ", ".join(li) + ">")
        assert name == "myClass7"
        assert args == li

        li = [
            p1,
            p2 + " (" + arg + ")",
            p1 + " (" + arg + ", " + arg + ", " + arg + ")"]
        name, args = declarations.templates.split(
            "myClass8<" + ", ".join(li) + ">")
        assert name == "myClass8"
        assert args == li

        li = [
            p2 + " (" + arg + ")",
            p1 + " (" + arg + ", " + arg + ")",
            p1]
        name, args = declarations.templates.split(
            "myClass9<" + ", ".join(li) + ">")
        assert name == "myClass9"
        assert args == li

        li = [
            p2 + " (" + arg + ")",
            p1 + " (" + arg + ", " + arg + ", " + arg + ")",
            p1,
            p2]
        name, args = declarations.templates.split(
            "myClass10<" + ", ".join(li) + ">")
        assert name == "myClass10"
        assert args == li
