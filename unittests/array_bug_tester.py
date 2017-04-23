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
            'int [2][3][4][5]' == aaaa_type.decl_string,
            aaaa_type.decl_string)

    def test2(self):
        code = 'int* aaaa[2][3][4][5];'
        src_reader = parser.source_reader_t(self.config)
        global_ns = declarations.get_global_namespace(
            src_reader.read_string(code))
        aaaa_type = global_ns.variable('aaaa').decl_type
        self.assertTrue(
            'int * [2][3][4][5]' == aaaa_type.decl_string,
            aaaa_type.decl_string)

    def test3(self):
        code = 'int aaaa[2];'
        src_reader = parser.source_reader_t(self.config)
        global_ns = declarations.get_global_namespace(
            src_reader.read_string(code))
        aaaa_type = global_ns.variable('aaaa').decl_type
        self.assertTrue(
            'int [2]' == aaaa_type.decl_string,
            aaaa_type.decl_string)

    def test4(self):
        code = 'struct xyz{}; xyz aaaa[2][3];'
        src_reader = parser.source_reader_t(self.config)
        global_ns = declarations.get_global_namespace(
            src_reader.read_string(code))
        aaaa_type = global_ns.variable('aaaa').decl_type
        self.assertTrue(
            '::xyz [2][3]' == aaaa_type.decl_string,
            aaaa_type.decl_string)

    def test5(self):
        code = 'char const arr[4] = {};'
        src_reader = parser.source_reader_t(self.config)
        global_ns = declarations.get_global_namespace(
            src_reader.read_string(code))
        arr_type = global_ns.variable('arr').decl_type
        if self.config.xml_generator == "gccxml":
            self.assertTrue(
                'char [4] const' == arr_type.decl_string,
                arr_type.decl_string)
        else:
            self.assertTrue(
                'char const [4]' == arr_type.decl_string,
                arr_type.decl_string)
        self.assertTrue(
            declarations.is_array(arr_type))
        self.assertTrue(
            declarations.is_const(arr_type))

    def test6(self):
        code = 'char volatile arr[4] = {};'
        src_reader = parser.source_reader_t(self.config)
        global_ns = declarations.get_global_namespace(
            src_reader.read_string(code))
        arr_type = global_ns.variable('arr').decl_type
        if self.config.xml_generator == "gccxml":
            self.assertTrue(
                'char [4] volatile' == arr_type.decl_string,
                arr_type.decl_string)
        else:
            self.assertTrue(
                'char volatile [4]' == arr_type.decl_string,
                arr_type.decl_string)
        self.assertTrue(
            declarations.is_array(arr_type))
        self.assertTrue(
            declarations.is_volatile(arr_type))

    def test7(self):
        code = 'char const volatile arr[4] = {};'
        src_reader = parser.source_reader_t(self.config)
        global_ns = declarations.get_global_namespace(
            src_reader.read_string(code))
        arr_type = global_ns.variable('arr').decl_type
        if self.config.xml_generator == "gccxml":
            self.assertTrue(
                'char [4] const volatile' == arr_type.decl_string,
                arr_type.decl_string)
        else:
            self.assertTrue(
                'char const volatile [4]' == arr_type.decl_string,
                arr_type.decl_string)
        self.assertTrue(
            declarations.is_array(arr_type))
        self.assertTrue(
            declarations.is_const(arr_type))
        self.assertTrue(
            declarations.is_volatile(arr_type))


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
