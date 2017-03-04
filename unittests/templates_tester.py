# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import unittest

from . import parser_test_case

from pygccxml import declarations


class Test(parser_test_case.parser_test_case_t):

    def __test_split_impl(self, decl_string, name, args):
        self.assertTrue(
            (name, args) == declarations.templates.split(decl_string))

    def __test_split_recursive_impl(self, decl_string, control_seq):
        self.assertTrue(
            control_seq ==
            list(declarations.templates.split_recursive(decl_string)))

    def __test_is_template_impl(self, decl_string):
        self.assertTrue(declarations.templates.is_instantiation(decl_string))

    def test_split_on_vector(self):
        self.__test_is_template_impl("vector<int,std::allocator<int> >")

        self.__test_split_impl(
            "vector<int,std::allocator<int> >",
            "vector",
            ["int", "std::allocator<int>"])

        self.__test_split_recursive_impl(
            "vector<int,std::allocator<int> >",
            [("vector", ["int", "std::allocator<int>"]),
                ("std::allocator", ["int"])])

    def test_split_on_string(self):
        self.__test_is_template_impl(
            "basic_string<char,std::char_traits<char>,std::allocator<char> >")

        self.__test_split_impl(
            "basic_string<char,std::char_traits<char>,std::allocator<char> >",
            "basic_string",
            ["char",
             "std::char_traits<char>",
             "std::allocator<char>"])

    def test_split_on_map(self):
        self.__test_is_template_impl(
            "map<long int,std::vector<int, std::allocator<int> >," +
            "std::less<long int>,std::allocator<std::pair<const long int, " +
            "std::vector<int, std::allocator<int> > > > >")

        self.__test_split_impl(
            "map<long int,std::vector<int, std::allocator<int> >," +
            "std::less<long int>,std::allocator<std::pair<const long int, " +
            "std::vector<int, std::allocator<int> > > > >",
            "map",
            ["long int",
             "std::vector<int, std::allocator<int> >",
             "std::less<long int>",
             "std::allocator<std::pair<const long int, " +
             "std::vector<int, std::allocator<int> > > >"])

    def test_join_on_vector(self):
        self.assertTrue(
            "vector< int, std::allocator<int> >" ==
            declarations.templates.join(
                "vector", ("int", "std::allocator<int>")))

    def test_bug_is_tmpl_inst(self):
        self.assertTrue(
            declarations.templates.is_instantiation(
                "::FX::QMemArray<unsigned char>::setRawData") is False)

    # disable broken test
    # def test_split_bug_fptr(self):
    #     x = 'map<std::string, bool (*)(std::string&, ' +
    #     'Ogre::MaterialScriptContext&), std::less<std::string>, ' +
    #     'std::allocator<std::pair<std::string const, bool (*)' +
    #     '(std::string&, Ogre::MaterialScriptContext&)> > >'
    #     name, args = declarations.templates.split( x )
    #     self.assertTrue( len(x) == 4, "This test is expected to fail." )


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
