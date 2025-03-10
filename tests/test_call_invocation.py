# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

from pygccxml import declarations


def __test_split_impl(decl_string, name, args):
    assert (name, args) == \
        declarations.call_invocation.split(decl_string)


def __test_split_recursive_impl(decl_string, control_seq):
    assert control_seq == \
        list(declarations.call_invocation.split_recursive(decl_string))


def __test_is_call_invocation_impl(decl_string):
    assert declarations.call_invocation.is_call_invocation(decl_string)


def test_split_on_vector():
    __test_is_call_invocation_impl("vector(int,std::allocator(int) )")

    __test_split_impl(
        "vector(int,std::allocator(int) )",
        "vector",
        ["int", "std::allocator(int)"])

    __test_split_recursive_impl(
        "vector(int,std::allocator(int) )",
        [("vector", ["int", "std::allocator(int)"]),
            ("std::allocator", ["int"])])


def test_split_on_string():
    __test_is_call_invocation_impl(
        "basic_string(char,std::char_traits(char),std::allocator(char) )")

    __test_split_impl(
        "basic_string(char,std::char_traits(char),std::allocator(char) )",
        "basic_string",
        ["char", "std::char_traits(char)", "std::allocator(char)"])


def test_split_on_map():
    __test_is_call_invocation_impl(
        "map(long int,std::vector(int, std::allocator(int) )," +
        "std::less(long int),std::allocator(std::pair" +
        "(const long int, std::vector(int, std::allocator(int) ) ) ) )")

    __test_split_impl(
        "map(long int,std::vector(int, std::allocator(int) )," +
        "std::less(long int),std::allocator(std::pair" +
        "(const long int, std::vector(int, std::allocator(int) ) ) ) )",
        "map",
        ["long int", "std::vector(int, std::allocator(int) )",
            "std::less(long int)",
            "std::allocator(std::pair(const long int," +
            " std::vector(int, std::allocator(int) ) ) )"])


def test_join_on_vector():
    assert "vector(int, std::allocator(int))" == \
        declarations.call_invocation.join(
            "vector", ("int", "std::allocator(int)"))


def test_find_args():
    temp = 'x()()'
    found = declarations.call_invocation.find_args(temp)
    assert (1, 2) == found
    found = declarations.call_invocation.find_args(temp, found[1] + 1)
    assert (3, 4) == found
    temp = 'x(int,int)(1,2)'
    found = declarations.call_invocation.find_args(temp)
    assert (1, 9) == found
    found = declarations.call_invocation.find_args(temp, found[1] + 1)
    assert (10, 14) == found


def test_bug_unmatched_brace():
    src = 'AlternativeName((&string("")), (&string("")), (&string("")))'
    __test_split_impl(
        src, 'AlternativeName', [
            '(&string(""))', '(&string(""))', '(&string(""))'])
