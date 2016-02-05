# Copyright 2014-2016 Insight Software Consortium.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import unittest
import parser_test_case

from pygccxml import parser
from pygccxml import declarations


class tester_t(parser_test_case.parser_test_case_t):

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.header = "test_copy_constructor.hpp"

    def setUp(self):
        decls = parser.parse([self.header], self.config)
        self.global_ns = declarations.get_global_namespace(decls)

    def test(self):
        """
        Check the is_copy_constructor method.

        This fails when using CastXML, see issue #27.

        """

        tclass = self.global_ns.class_("test")
        ctors = []
        for decl in tclass.declarations:
            if isinstance(decl, declarations.calldef.constructor_t):
                ctors.append(decl)

        # test::test(test const & t0) [copy constructor]
        self.assertTrue(ctors[0].is_copy_constructor)
        # test::test(float const & t0) [constructor]
        self.assertFalse(ctors[1].is_copy_constructor)
        # test::test(myvar t0) [constructor]
        self.assertFalse(ctors[2].is_copy_constructor)

        t2class = self.global_ns.class_("test2")
        ctors = []
        for decl in t2class.declarations:
            if isinstance(decl, declarations.calldef.constructor_t):
                ctors.append(decl)

        # test2::test2() [constructor]
        self.assertFalse(ctors[0].is_copy_constructor)
        # test2::test2(test2 const & arg0) [copy constructor]
        self.assertTrue(ctors[1].is_copy_constructor)


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(tester_t))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())

if __name__ == "__main__":
    run_suite()
