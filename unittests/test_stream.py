# Copyright 2014-2016 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import unittest
import parser_test_case

from pygccxml import parser
from pygccxml import declarations


class Test(parser_test_case.parser_test_case_t):

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.header = "test_stream.hpp"
        self.config.cflags = "-std=c++11"

    def test_stream_non_copyable(self):
        """
        Test find_noncopyable_vars

        See #71

        find_noncopyable_vars is throwing:
        RuntimeError: maximum recursion depth exceeded while
        calling a Python object
        """
        decls = parser.parse([self.header], self.config)
        global_ns = declarations.get_global_namespace(decls)

        test_ns = global_ns.namespace('Test2')
        cls = test_ns.class_('FileStreamDataStream')
        declarations.type_traits_classes.find_noncopyable_vars(cls)

def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())

if __name__ == "__main__":
    run_suite()
