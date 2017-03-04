# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import unittest

from . import parser_test_case

from pygccxml import declarations


class tester_t(parser_test_case.parser_test_case_t):

    def __test_split_impl(self, decl_string, name, args):
        self.assertTrue(
            (name, args) == declarations.call_invocation.split(decl_string))

    def __test_split_recursive_impl(self, decl_string, control_seq):
        self.assertTrue(
            control_seq ==
            list(declarations.call_invocation.split_recursive(decl_string)))

    def __test_is_call_invocation_impl(self, decl_string):
        self.assertTrue(
            declarations.call_invocation.is_call_invocation(decl_string))

    def test_split_on_vector(self):
        self.__test_is_call_invocation_impl("vector(int,std::allocator(int) )")

        self.__test_split_impl(
            "vector(int,std::allocator(int) )",
            "vector",
            ["int", "std::allocator(int)"])

        self.__test_split_recursive_impl(
            "vector(int,std::allocator(int) )",
            [("vector", ["int", "std::allocator(int)"]),
                ("std::allocator", ["int"])])

    def test_split_on_string(self):
        self.__test_is_call_invocation_impl(
            "basic_string(char,std::char_traits(char),std::allocator(char) )")

        self.__test_split_impl(
            "basic_string(char,std::char_traits(char),std::allocator(char) )",
            "basic_string",
            ["char", "std::char_traits(char)", "std::allocator(char)"])

    def test_split_on_map(self):
        self.__test_is_call_invocation_impl(
            "map(long int,std::vector(int, std::allocator(int) )," +
            "std::less(long int),std::allocator(std::pair" +
            "(const long int, std::vector(int, std::allocator(int) ) ) ) )")

        self.__test_split_impl(
            "map(long int,std::vector(int, std::allocator(int) )," +
            "std::less(long int),std::allocator(std::pair" +
            "(const long int, std::vector(int, std::allocator(int) ) ) ) )",
            "map",
            ["long int", "std::vector(int, std::allocator(int) )",
                "std::less(long int)",
                "std::allocator(std::pair(const long int," +
                " std::vector(int, std::allocator(int) ) ) )"])

    def test_join_on_vector(self):
        self.assertTrue(
            "vector( int, std::allocator(int) )" ==
            declarations.call_invocation.join(
                "vector", ("int", "std::allocator(int)")))

    def test_find_args(self):
        temp = 'x()()'
        found = declarations.call_invocation.find_args(temp)
        self.assertTrue((1, 2) == found)
        found = declarations.call_invocation.find_args(temp, found[1] + 1)
        self.assertTrue((3, 4) == found)
        temp = 'x(int,int)(1,2)'
        found = declarations.call_invocation.find_args(temp)
        self.assertTrue((1, 9) == found)
        found = declarations.call_invocation.find_args(temp, found[1] + 1)
        self.assertTrue((10, 14) == found)

    def test_bug_unmatched_brace(self):
        src = 'AlternativeName((&string("")), (&string("")), (&string("")))'
        self.__test_split_impl(
            src, 'AlternativeName', [
                '(&string(""))', '(&string(""))', '(&string(""))'])


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(tester_t))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
