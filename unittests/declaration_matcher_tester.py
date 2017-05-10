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
        self.header = 'classes.hpp'
        self.global_ns = None

    def setUp(self):
        if not Test.global_ns:
            decls = parser.parse([self.header], self.config)
            Test.global_ns = declarations.get_global_namespace(decls)
            Test.global_ns.init_optimizer()
        self.global_ns = Test.global_ns

    def test_global(self):
        gns = self.global_ns
        gns.class_('cls')
        gns.class_('::cls')

    def test_typedefs(self):
        gns = self.global_ns
        gns.class_('cls2')
        if self.config.xml_generator == "castxml":
            gns.typedef('cls2')
        gns.class_('::cls2')

        gns.class_('cls3')
        if self.config.xml_generator == "castxml":
            gns.typedef('cls3')
        cls3 = gns.class_('::cls3')
        cls3.variable('i')

    def test_ns1(self):
        gns = self.global_ns
        ns1 = gns.namespace('ns')

        gns.class_('nested_cls')
        self.assertRaises(Exception, lambda: gns.class_('ns::nested_cls'))
        gns.class_('::ns::nested_cls')

        self.assertRaises(Exception, lambda: ns1.class_('::nested_cls'))
        ns1.class_('nested_cls')
        ns1.class_('::ns::nested_cls')

        gns.class_('nested_cls2')
        self.assertRaises(Exception, lambda: gns.class_('ns::nested_cls2'))
        gns.class_('::ns::nested_cls2')

        gns.class_('nested_cls3')
        self.assertRaises(Exception, lambda: gns.class_('ns::nested_cls3'))
        gns.class_('::ns::nested_cls3')


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
