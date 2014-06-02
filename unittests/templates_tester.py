#! /usr/bin/python
# Copyright 2004-2013 Roman Yakovenko
# Copyright 2014 Insight Software Consortium
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import unittest

from pygccxml import declarations


class tester_t(unittest.TestCase):

    def __init__(self, *args):
        unittest.TestCase.__init__(self, *args)

    def __test_split_impl(self, decl_string, name, args):
        self.failUnless(
            (name, args) == declarations.templates.split(decl_string))

    def __test_split_recursive_impl(self, decl_string, control_seq):
        self.failUnless(
            control_seq == declarations.templates.split_recursive(decl_string))

    def __test_is_template_impl(self, decl_string):
        self.failUnless(declarations.templates.is_instantiation(decl_string))

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
        self.failUnless(
            "vector< int, std::allocator<int> >"
            == declarations.templates.join(
                "vector", ("int", "std::allocator<int>")))

    def test_bug_is_tmpl_inst(self):
        self.failUnless(
            False == declarations.templates.is_instantiation(
                "::FX::QMemArray<unsigned char>::setRawData"))

    # disable broken test
    # def test_split_bug_fptr(self):
    #     x = 'map<std::string, bool (*)(std::string&, ' +
    #     'Ogre::MaterialScriptContext&), std::less<std::string>, ' +
    #     'std::allocator<std::pair<std::string const, bool (*)' +
    #     '(std::string&, Ogre::MaterialScriptContext&)> > >'
    #     name, args = declarations.templates.split( x )
    #     self.failUnless( len(x) == 4, "This test is expected to fail." )


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(tester_t))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())

if __name__ == "__main__":
    run_suite()
