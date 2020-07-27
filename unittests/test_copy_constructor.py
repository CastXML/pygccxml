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

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.header = "test_copy_constructor.hpp"
        self.global_ns = None

    def setUp(self):
        if not self.global_ns:
            decls = parser.parse([self.header], self.config)
            Test.global_ns = declarations.get_global_namespace(decls)
            Test.xml_generator_from_xml_file = \
                self.config.xml_generator_from_xml_file
        self.xml_generator_from_xml_file = Test.xml_generator_from_xml_file
        self.global_ns = Test.global_ns

    def test(self):
        """
        Check the is_copy_constructor method.

        This fails when using CastXML, see issue #27.

        """

        tclass = self.global_ns.class_("test")
        ctors = []
        for decl in tclass.declarations:
            if isinstance(decl, declarations.constructor_t):
                ctors.append(decl)

        # test::test(test const & t0) [copy constructor]
        self.assertTrue(declarations.is_copy_constructor(ctors[0]))
        # test::test(float const & t0) [constructor]
        self.assertFalse(declarations.is_copy_constructor(ctors[1]))
        # test::test(myvar t0) [constructor]
        self.assertFalse(declarations.is_copy_constructor(ctors[2]))

        t2class = self.global_ns.class_("test2")
        ctors = []
        for decl in t2class.declarations:
            if isinstance(decl, declarations.constructor_t):
                ctors.append(decl)

        # test2::test2() [constructor]
        self.assertFalse(declarations.is_copy_constructor(ctors[0]))
        # test2::test2(test2 const & arg0) [copy constructor]
        self.assertTrue(declarations.is_copy_constructor(ctors[1]))


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
