# Copyright 2014-2016 Insight Software Consortium.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import unittest
import parser_test_case

from pygccxml import parser
from pygccxml import declarations
from pygccxml import utils


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

        # GCCXML and CastXML return the constructors in a different order.
        # I hope this index inversion will cover the two cases. If different
        # compilers give other orders, we will need to find a nicer solution.
        if "CastXML" in utils.xml_generator:
            positions = [0, 1]
        elif "GCC" in utils.xml_generator:
            positions = [1, 0]

        # test2::test2() [constructor]
        self.assertFalse(declarations.is_copy_constructor(ctors[positions[0]]))
        # test2::test2(test2 const & arg0) [copy constructor]
        self.assertTrue(declarations.is_copy_constructor(ctors[positions[1]]))


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(tester_t))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())

if __name__ == "__main__":
    run_suite()
