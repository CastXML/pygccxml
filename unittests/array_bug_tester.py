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

    def test1(self):
        code = 'int aaaa[2][3][4][5];'
        src_reader = parser.source_reader_t(self.config)
        global_ns = declarations.get_global_namespace(
            src_reader.read_string(code))
        aaaa_type = global_ns.variable('aaaa').decl_type
        self.assertTrue(
            'int[2][3][4][5]' == aaaa_type.decl_string,
            aaaa_type.decl_string)

    def test2(self):
        code = 'int* aaaa[2][3][4][5];'
        src_reader = parser.source_reader_t(self.config)
        global_ns = declarations.get_global_namespace(
            src_reader.read_string(code))
        aaaa_type = global_ns.variable('aaaa').decl_type
        self.assertTrue(
            'int *[2][3][4][5]' == aaaa_type.decl_string,
            aaaa_type.decl_string)

    def test3(self):
        code = 'int aaaa[2];'
        src_reader = parser.source_reader_t(self.config)
        global_ns = declarations.get_global_namespace(
            src_reader.read_string(code))
        aaaa_type = global_ns.variable('aaaa').decl_type
        self.assertTrue(
            'int[2]' == aaaa_type.decl_string,
            aaaa_type.decl_string)

    def test4(self):
        code = 'struct xyz{}; xyz aaaa[2][3];'
        src_reader = parser.source_reader_t(self.config)
        global_ns = declarations.get_global_namespace(
            src_reader.read_string(code))
        aaaa_type = global_ns.variable('aaaa').decl_type
        self.assertTrue(
            '::xyz[2][3]' == aaaa_type.decl_string,
            aaaa_type.decl_string)

    def test5(self):
        self._test_impl('char const arr[4] = {};', 'const char[4]', True)
        self._test_impl('const char arr[4] = {};', 'const char[4]', True)

    def test6(self):
        self._test_impl('char volatile arr[4] = {};',
                        'volatile char[4]', False)
        self._test_impl('volatile char arr[4] = {};',
                        'volatile char[4]', False)

    def test7(self):
        self._test_impl('char const volatile arr[4] = {};',
                        'volatile const char[4]', True)
        self._test_impl('const volatile char arr[4] = {};',
                        'volatile const char[4]', True)

    def _test_impl(self, code, expected, is_const_check):
        src_reader = parser.source_reader_t(self.config)
        global_ns = declarations.get_global_namespace(
            src_reader.read_string(code))
        arr_type = global_ns.variable('arr').decl_type
        self.assertTrue(
            expected == arr_type.decl_string,
            arr_type.decl_string)
        self.assertTrue(declarations.is_array(arr_type))
        if is_const_check:
            self.assertTrue(declarations.is_const(arr_type))


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
