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
        self.header = 'non_copyable_classes.hpp'
        self.global_ns = None

    def setUp(self):
        if not self.global_ns:
            decls = parser.parse([self.header], self.config)
            self.global_ns = declarations.get_global_namespace(decls)
            self.global_ns.init_optimizer()
            Test.xml_generator_from_xml_file = \
                self.config.xml_generator_from_xml_file
        self.xml_generator_from_xml_file = Test.xml_generator_from_xml_file

    def test(self):

        """
        Search for classes which can not be copied.

        See bug #13

        1) non copyable class
        2) non copyable const variable (fundamental type)
        3) non copyable const variable (class type)
        4) non copyable const variable (array type)
        5) non copyable const variable (class type)

        """

        main_foo_1 = self.global_ns.class_('MainFoo1')
        self.assertTrue(declarations.is_noncopyable(main_foo_1))

        main_foo_2 = self.global_ns.class_('MainFoo2')
        self.assertTrue(declarations.is_noncopyable(main_foo_2))

        main_foo_3 = self.global_ns.class_('MainFoo3')
        self.assertTrue(declarations.is_noncopyable(main_foo_3))

        main_foo_4 = self.global_ns.class_('MainFoo4')
        self.assertTrue(declarations.is_noncopyable(main_foo_4))

        main_foo_5 = self.global_ns.class_('MainFoo5')
        self.assertTrue(declarations.is_noncopyable(main_foo_5))

        if self.xml_generator_from_xml_file.is_castxml:
            # CastXML only test
            # MainFoo6 is copyable
            main_foo_6 = self.global_ns.class_('MainFoo6')
            self.assertFalse(declarations.is_noncopyable(main_foo_6))


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
