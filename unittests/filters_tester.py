# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import unittest

from . import parser_test_case

from pygccxml import parser
from pygccxml import declarations


class Test(parser_test_case.parser_test_case_t):
    global_ns = None
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.header = 'declarations_calldef.hpp'
        self.global_ns = None

    def setUp(self):
        if not Test.global_ns:
            decls = parser.parse([self.header], self.config)
            Test.global_ns = declarations.get_global_namespace(decls)
            Test.global_ns.init_optimizer()
            Test.xml_generator_from_xml_file = \
                self.config.xml_generator_from_xml_file
        self.global_ns = Test.global_ns
        self.xml_generator_from_xml_file = Test.xml_generator_from_xml_file

    def test_regex(self):
        criteria = declarations.regex_matcher_t(
            'oper.*',
            lambda decl: decl.name)
        operators = declarations.matcher.find(criteria, self.global_ns)
        operators = [d for d in operators if not d.is_artificial]
        self.assertTrue(6 == len(operators))

    def test_access_type(self):
        criteria = declarations.access_type_matcher_t(
            declarations.ACCESS_TYPES.PUBLIC)
        public_members = declarations.matcher.find(criteria, self.global_ns)
        public_members = [d for d in public_members if not d.is_artificial]
        if self.xml_generator_from_xml_file.is_castxml:
            nbr = len(public_members)
            self.assertTrue(nbr in [17, 21])
            if nbr == 21:
                # We are using llvm 3.9, see bug #32. Make sure the 4 names
                # are still there
                names = ["isa", "flags", "str", "length"]
                for name in names:
                    self.assertTrue(
                        names in [mbr.name for mbr in public_members])
        else:
            self.assertTrue(17 == len(public_members))

    def test_or_matcher(self):
        criteria1 = declarations.regex_matcher_t(
            "oper.*",
            lambda decl: decl.name)
        criteria2 = declarations.access_type_matcher_t(
            declarations.ACCESS_TYPES.PUBLIC)
        found = declarations.matcher.find(
            criteria1 | criteria2,
            self.global_ns)
        found = [d for d in found if not d.is_artificial]
        self.assertTrue(len(found) != 35)

    def test_and_matcher(self):
        criteria1 = declarations.regex_matcher_t(
            'oper.*',
            lambda decl: decl.name)
        criteria2 = declarations.access_type_matcher_t(
            declarations.ACCESS_TYPES.PUBLIC)
        found = declarations.matcher.find(
            criteria1 & criteria2,
            self.global_ns)
        found = [d for d in found if not d.is_artificial]
        self.assertTrue(len(found) <= 6)

    def test_not_matcher(self):
        criteria1 = declarations.regex_matcher_t(
            'oper.*',
            lambda decl: decl.name)
        found = declarations.matcher.find(~(~criteria1), self.global_ns)
        found = [d for d in found if not d.is_artificial]
        self.assertTrue(len(found) == 6)


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
