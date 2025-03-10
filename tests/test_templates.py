# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

from pygccxml import declarations


def __test_split_impl(decl_string, name, args):
    assert (name, args) == \
        declarations.templates.split(decl_string)


def __test_split_recursive_impl(decl_string, control_seq):
    assert control_seq == \
        list(declarations.templates.split_recursive(decl_string))


def __test_is_template_impl(decl_string):
    assert declarations.templates.is_instantiation(decl_string)


def test_split_on_vector():
    __test_is_template_impl("vector<int, std::allocator<int>>")

    __test_split_impl(
        "vector<int, std::allocator<int>>",
        "vector",
        ["int", "std::allocator<int>"])

    __test_split_recursive_impl(
        "vector<int, std::allocator<int>>",
        [("vector", ["int", "std::allocator<int>"]),
            ("std::allocator", ["int"])])


def test_split_on_string():
    __test_is_template_impl(
        "basic_string<char, std::char_traits<char>, std::allocator<char>>")

    __test_split_impl(
        "basic_string<char, std::char_traits<char>, std::allocator<char>>",
        "basic_string",
        ["char",
            "std::char_traits<char>",
            "std::allocator<char>"])


def test_split_on_map():
    __test_is_template_impl(
        "map<long int,std::vector<int, std::allocator<int>>," +
        "std::less<long int>, std::allocator<std::pair<const long int, " +
        "std::vector<int, std::allocator<int>>>>>")

    __test_split_impl(
        "map<long int,std::vector<int, std::allocator<int>>," +
        "std::less<long int>, std::allocator<std::pair<const long int, " +
        "std::vector<int, std::allocator<int>>>>>",
        "map",
        ["long int",
            "std::vector<int, std::allocator<int>>",
            "std::less<long int>",
            "std::allocator<std::pair<const long int, " +
            "std::vector<int, std::allocator<int>>>>"])


def test_join_on_vector():
    assert "vector<int, std::allocator<int>>" == \
        declarations.templates.join(
            "vector", ("int", "std::allocator<int>"))


def test_bug_is_tmpl_inst():
    assert declarations.templates.is_instantiation(
        "::FX::QMemArray<unsigned char>::setRawData") is False
