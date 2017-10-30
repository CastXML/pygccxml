# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import os
import unittest
import platform

from . import autoconfig
from . import parser_test_case

from pygccxml import utils
from pygccxml import parser


class tester_impl_t(parser_test_case.parser_test_case_t):

    def __init__(self, architecture, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.architecture = architecture
        self.global_ns = None
        self.__cxx_std = utils.cxx_standard(self.config.cflags)

    def test_enum_patcher(self):
        fix_enum = self.global_ns.free_function("fix_enum")
        default_val = fix_enum.arguments[0].default_value
        if self.__cxx_std.is_cxx11_or_greater:
            val = "::ns1::ns2::fruit::apple"
        else:
            val = "::ns1::ns2::apple"
        self.assertEqual(default_val, val)

        if 32 == self.architecture or \
                self.xml_generator_from_xml_file.is_castxml:
            fix_enum2 = self.global_ns.free_function("fix_enum2")
            default_val = fix_enum2.arguments[0].default_value
            self.assertEqual(default_val, val)

            ns1 = self.global_ns.namespace("ns1")
            ns2 = ns1.namespace("ns2")
            fix_enum2 = ns2.free_function("fix_enum2")
            default_val = fix_enum2.arguments[0].default_value
            self.assertEqual(default_val, val)

            fix_enum3 = self.global_ns.free_function("fix_enum3")
            default_val = fix_enum3.arguments[0].default_value
            val = val.replace("apple", "orange")
            self.assertEqual(default_val, val)

            if self.__cxx_std.is_cxx11_or_greater:
                fix_enum4 = self.global_ns.free_function("fix_enum4")
                default_val = fix_enum4.arguments[0].default_value
                self.assertEqual(default_val, "::ns4::color::blue")

                fix_enum5 = self.global_ns.free_function("fix_enum5")
                default_val = fix_enum5.arguments[0].default_value
                self.assertEqual(default_val, "::ns4::color::blue")

            lpe = self.global_ns.free_function("log_priority_enabled")
            default_val = lpe.arguments[0].default_value
            if self.__cxx_std.is_cxx11_or_greater:
                val = "(long int)" + \
                    "(::ACE_Log_Priority_Index::LM_INVALID_BIT_INDEX)"
            else:
                val = "(long int)(::LM_INVALID_BIT_INDEX)"
            self.assertEqual(default_val, val)

    def test_numeric_patcher(self):
        fix_numeric = self.global_ns.free_function("fix_numeric")
        if 32 == self.architecture:
            val = "0xffffffffffffffff"
            self.assertEqual(
                fix_numeric.arguments[0].default_value, val)
        else:
            generator = self.xml_generator_from_xml_file
            if generator.is_castxml1 or \
                    float(generator.xml_output_version) >= 1.137:
                val = "(unsigned long long)-1"
            else:
                val = "(ull)-1"
            self.assertEqual(
                fix_numeric.arguments[0].default_value, val)

    def test_unqualified_integral_patcher(self):
        if 32 != self.architecture:
            # For this check to be removed, patcher_tester_64bit.xml
            # will need to be updated for CastXML
            return

        ns1 = self.global_ns.namespace("ns1")
        st1 = ns1.class_("st1")
        fun1 = st1.member_function("fun1")
        output_verion = self.xml_generator_from_xml_file.xml_output_version
        if self.xml_generator_from_xml_file.is_castxml1 or \
                float(output_verion) >= 1.137:
            val1 = "ns1::DEFAULT_1"
            val2 = "ns1::st1::DEFAULT_2"
        else:
            val1 = "::ns1::DEFAULT_1"
            val2 = "::ns1::st1::DEFAULT_2"
        self.assertEqual(
            fun1.arguments[0].default_value, val1)
        self.assertEqual(
            fun1.arguments[1].default_value, val2)

        fun2 = self.global_ns.free_function("fun2")
        self.assertEqual(
            fun2.arguments[0].default_value,
            "::DEFAULT_1")
        output_verion = self.xml_generator_from_xml_file.xml_output_version
        if self.xml_generator_from_xml_file.is_castxml1 or \
                float(output_verion) >= 1.137:
            val1 = "ns1::DEFAULT_1"
            val2 = "ns1::st1::DEFAULT_2"
        else:
            # Before XML output version 1.137, the following two
            # were unpatched and were identical to the text in
            # matcher.hpp
            val1 = "ns1::DEFAULT_1"
            val2 = "::ns1::st1::DEFAULT_2"
        self.assertEqual(
            fun2.arguments[1].default_value, val1)
        self.assertEqual(
            fun2.arguments[2].default_value, val2)

    def test_unnamed_enum_patcher(self):
        fix_unnamed = self.global_ns.free_function("fix_unnamed")
        self.assertEqual(
            fix_unnamed.arguments[0].default_value, "int(::fx::unnamed)")

    def test_function_call_patcher(self):
        fix_function_call = self.global_ns.free_function("fix_function_call")
        default_val = fix_function_call.arguments[0].default_value
        output_verion = self.xml_generator_from_xml_file.xml_output_version
        if self.xml_generator_from_xml_file.is_castxml1 or \
                float(output_verion) >= 1.137:
            val = "function_call::calc(1, 2, 3)"
        else:
            val = "calc(1, 2, 3)"
        self.assertEqual(default_val, val)

    def test_fundamental_patcher(self):
        fcall = self.global_ns.free_function("fix_fundamental")
        if self.__cxx_std.is_cxx11_or_greater:
            val = "(unsigned int)(::fundamental::spam::eggs)"
        else:
            val = "(unsigned int)(::fundamental::eggs)"
        self.assertEqual(
            fcall.arguments[0].default_value, val)

    def test_constructor_patcher(self):
        typedef__func = self.global_ns.free_function("typedef__func")
        default_val = typedef__func.arguments[0].default_value
        val = "typedef_::alias()"
        self.assertEqual(default_val, val)
        if 32 == self.architecture:
            clone_tree = self.global_ns.free_function("clone_tree")
            default_values = [
                ("vector<std::basic_string<char, std::char_traits<char>," +
                    " std::allocator<char> >,std::allocator" +
                    "<std::basic_string<char, std::char_traits<char>, " +
                    "std::allocator<char> > > >()"),
                ("vector<std::basic_string<char, std::char_traits<char>," +
                    "std::allocator<char> >,std::allocator" +
                    "<std::basic_string<char, std::char_traits<char>, " +
                    "std::allocator<char> > > >((&allocator" +
                    "<std::basic_string<char, std::char_traits<char>, " +
                    "std::allocator<char> > >()))")]
            self.assertIn(
                clone_tree.arguments[0].default_value, default_values)


class tester_32_t(tester_impl_t):
    global_ns = None

    def __init__(self, *args):
        tester_impl_t.__init__(self, 32, *args)

    def setUp(self):
        if not tester_32_t.global_ns:
            reader = parser.source_reader_t(self.config)
            tester_32_t.global_ns = reader.read_file(
                "patcher.hpp")[0].top_parent
            tester_32_t.xml_generator_from_xml_file = \
                reader.xml_generator_from_xml_file
        self.global_ns = tester_32_t.global_ns
        self.xml_generator_from_xml_file = \
            tester_32_t.xml_generator_from_xml_file


class tester_64_t(tester_impl_t):
    global_ns = None

    def __init__(self, *args):
        tester_impl_t.__init__(self, 64, *args)
        self.original_get_architecture = utils.get_architecture

    def setUp(self):
        self.original_get_architecture = utils.get_architecture
        utils.get_architecture = lambda: 64

        if not tester_64_t.global_ns:
            reader = parser.source_reader_t(self.config)
            if "castxml" not in self.config.xml_generator:
                tester_64_t.global_ns = reader.read_xml_file(
                    os.path.join(
                        autoconfig.data_directory,
                        "patcher_tester_64bit.xml"))[0].top_parent
            else:
                tester_64_t.global_ns = reader.read_file(
                    "patcher.hpp")[0].top_parent
            tester_64_t.xml_generator_from_xml_file = \
                reader.xml_generator_from_xml_file
        self.global_ns = tester_64_t.global_ns
        self.xml_generator_from_xml_file = \
            tester_64_t.xml_generator_from_xml_file

    def tearDown(self):
        utils.get_architecture = self.original_get_architecture


def create_suite():
    suite = unittest.TestSuite()
    if "castxml" not in autoconfig.cxx_parsers_cfg.config.xml_generator:
        suite.addTest(unittest.makeSuite(tester_32_t))
    suite.addTest(unittest.makeSuite(tester_64_t))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
