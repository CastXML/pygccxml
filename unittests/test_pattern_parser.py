# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import unittest

from . import parser_test_case

from pygccxml import parser
from pygccxml import declarations


class Test(parser_test_case.parser_test_case_t):

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.header = "test_pattern_parser.hpp"
        self.config.cflags = "-std=c++11"

    def test_template_split_std_vector(self):
        """
        Demonstrate error in pattern parser, see #60

        """

        if self.config.xml_generator == "gccxml":
            return

        decls = parser.parse([self.header], self.config)

        for decl in declarations.make_flatten(decls):
            if "myClass" in decl.name:
                _ = decl.partial_name

    def test_matcher(self):
        """
        Run the matcher on all the templated classes.

        This exercises the whole pipeline even more.

        """

        if self.config.xml_generator == "gccxml":
            return

        decls = parser.parse([self.header], self.config)
        global_ns = declarations.get_global_namespace(decls)
        criteria = declarations.declaration_matcher(name="myClass")
        _ = declarations.matcher.find(criteria, global_ns)

    def test_split(self):
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
            self.assertEqual(name, "myClass0a")
            self.assertEqual(args, li)

            li = [p1, p2]
            name, args = declarations.templates.split(
                "myClass0b<" + ", ".join(li) + ">")
            self.assertEqual(name, "myClass0b")
            self.assertEqual(args, li)

            li = [p1, p2, p2]
            name, args = declarations.templates.split(
                "myClass0c<" + ", ".join(li) + ">")
            self.assertEqual(name, "myClass0c")
            self.assertEqual(args, li)

            li = [p1 + " (" + arg + ")"]
            name, args = declarations.templates.split(
                "myClass1<" + ", ".join(li) + ">")
            self.assertEqual(name, "myClass1")
            self.assertEqual(args, li)

            li = [p1 + " (" + arg + ", " + arg + ")"]
            name, args = declarations.templates.split(
                "myClass2<" + ", ".join(li) + ">")
            self.assertEqual(name, "myClass2")
            self.assertEqual(args, li)

            li = [p2 + " (" + arg + ", " + arg + ")"]
            name, args = declarations.templates.split(
                "myClass3<" + ", ".join(li) + ">")
            self.assertEqual(name, "myClass3")
            self.assertEqual(args, li)

            li = [p1 + " (" + arg + ", " + arg + ", " + arg + ")"]
            name, args = declarations.templates.split(
                "myClass4<" + ", ".join(li) + ">")
            self.assertEqual(name, "myClass4")
            self.assertEqual(args, li)

            li = [
                p1 + " (" + arg + ", " + arg + ", " + arg + ")",
                p1]
            name, args = declarations.templates.split(
                "myClass5<" + ", ".join(li) + ">")
            self.assertEqual(name, "myClass5")
            self.assertEqual(args, li)

            li = [
                p1,
                p1 + " (" + arg + ", " + arg + ", " + arg + ")"]
            name, args = declarations.templates.split(
                "myClass6<" + ", ".join(li) + ">")
            self.assertEqual(name, "myClass6")
            self.assertEqual(args, li)

            li = [
                p2 + " (" + arg + ")",
                p1,
                p1 + " (" + arg + ", " + arg + ", " + arg + ")"]
            name, args = declarations.templates.split(
                "myClass7<" + ", ".join(li) + ">")
            self.assertEqual(name, "myClass7")
            self.assertEqual(args, li)

            li = [
                p1,
                p2 + " (" + arg + ")",
                p1 + " (" + arg + ", " + arg + ", " + arg + ")"]
            name, args = declarations.templates.split(
                "myClass8<" + ", ".join(li) + ">")
            self.assertEqual(name, "myClass8")
            self.assertEqual(args, li)

            li = [
                p2 + " (" + arg + ")",
                p1 + " (" + arg + ", " + arg + ")",
                p1]
            name, args = declarations.templates.split(
                "myClass9<" + ", ".join(li) + ">")
            self.assertEqual(name, "myClass9")
            self.assertEqual(args, li)

            li = [
                p2 + " (" + arg + ")",
                p1 + " (" + arg + ", " + arg + ", " + arg + ")",
                p1,
                p2]
            name, args = declarations.templates.split(
                "myClass10<" + ", ".join(li) + ">")
            self.assertEqual(name, "myClass10")
            self.assertEqual(args, li)


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
