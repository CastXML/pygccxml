# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest

from . import autoconfig

from pygccxml import declarations
from pygccxml import parser
from pygccxml import utils


TEST_FILES = [
    "patcher.hpp",
]

config = autoconfig.cxx_parsers_cfg.config.clone()
project_reader = parser.project_reader_t(config=config, cache=None)
decls = project_reader.read_files(
    TEST_FILES,
    parser.COMPILATION_MODE.ALL_AT_ONCE
)
config.xml_generator_from_xml_file = project_reader.xml_generator_from_xml_file
config.__cxx_std = utils.cxx_standard(config.cflags)


@pytest.fixture
def global_ns():
    global_ns = declarations.get_global_namespace(decls)
    return global_ns


def test_enum_patcher(global_ns):
    fix_enum = global_ns.free_function("fix_enum")
    default_val = fix_enum.arguments[0].default_value
    if config.__cxx_std.is_cxx11_or_greater:
        val = "::ns1::ns2::fruit::apple"
    else:
        val = "::ns1::ns2::apple"
    assert default_val == val

    fix_enum2 = global_ns.free_function("fix_enum2")
    default_val = fix_enum2.arguments[0].default_value
    assert default_val == val

    ns1 = global_ns.namespace("ns1")
    ns2 = ns1.namespace("ns2")
    fix_enum2 = ns2.free_function("fix_enum2")
    default_val = fix_enum2.arguments[0].default_value
    assert default_val == val

    fix_enum3 = global_ns.free_function("fix_enum3")
    default_val = fix_enum3.arguments[0].default_value
    val = val.replace("apple", "orange")
    assert default_val == val

    if config.__cxx_std.is_cxx11_or_greater:
        fix_enum4 = global_ns.free_function("fix_enum4")
        default_val = fix_enum4.arguments[0].default_value
        assert default_val == "::ns4::color::blue"

        fix_enum5 = global_ns.free_function("fix_enum5")
        default_val = fix_enum5.arguments[0].default_value
        assert default_val == "::ns4::color::blue"

    lpe = global_ns.free_function("log_priority_enabled")
    default_val = lpe.arguments[0].default_value
    if config.__cxx_std.is_cxx11_or_greater:
        val = "(long int)" + \
            "(::ACE_Log_Priority_Index::LM_INVALID_BIT_INDEX)"
    else:
        val = "(long int)(::LM_INVALID_BIT_INDEX)"
    assert default_val == val


def test_numeric_patcher(global_ns):
    fix_numeric = global_ns.free_function("fix_numeric")
    generator = config.xml_generator_from_xml_file
    if generator.is_castxml1 or \
            float(generator.xml_output_version) >= 1.137:
        val = "(unsigned long long)-1"
    else:
        val = "(ull)-1"
    assert fix_numeric.arguments[0].default_value == val


def test_unqualified_integral_patcher(global_ns):
    # For this check to be removed, patcher_tester_64bit.xml
    # will need to be updated for CastXML
    return

    ns1 = global_ns.namespace("ns1")
    st1 = ns1.class_("st1")
    fun1 = st1.member_function("fun1")
    output_verion = xml_generator_from_xml_file.xml_output_version
    if xml_generator_from_xml_file.is_castxml1 or \
            float(output_verion) >= 1.137:
        val1 = "ns1::DEFAULT_1"
        val2 = "ns1::st1::DEFAULT_2"
    else:
        val1 = "::ns1::DEFAULT_1"
        val2 = "::ns1::st1::DEFAULT_2"
    assertEqual(
        fun1.arguments[0].default_value, val1)
    assertEqual(
        fun1.arguments[1].default_value, val2)

    fun2 = global_ns.free_function("fun2")
    assertEqual(
        fun2.arguments[0].default_value,
        "::DEFAULT_1")
    output_verion = xml_generator_from_xml_file.xml_output_version
    if xml_generator_from_xml_file.is_castxml1 or \
            float(output_verion) >= 1.137:
        val1 = "ns1::DEFAULT_1"
        val2 = "ns1::st1::DEFAULT_2"
    else:
        # Before XML output version 1.137, the following two
        # were unpatched and were identical to the text in
        # matcher.hpp
        val1 = "ns1::DEFAULT_1"
        val2 = "::ns1::st1::DEFAULT_2"
    assertEqual(
        fun2.arguments[1].default_value, val1)
    assertEqual(
        fun2.arguments[2].default_value, val2)


def test_unnamed_enum_patcher(global_ns):
    fix_unnamed = global_ns.free_function("fix_unnamed")
    assert fix_unnamed.arguments[0].default_value == "int(::fx::unnamed)"


def test_function_call_patcher(global_ns):
    fix_function_call = global_ns.free_function("fix_function_call")
    default_val = fix_function_call.arguments[0].default_value
    output_verion = config.xml_generator_from_xml_file.xml_output_version
    if config.xml_generator_from_xml_file.is_castxml1 or \
            float(output_verion) >= 1.137:
        val = "function_call::calc(1, 2, 3)"
    else:
        val = "calc(1, 2, 3)"
    assert default_val == val


def test_fundamental_patcher(global_ns):
    fcall = global_ns.free_function("fix_fundamental")
    if config.__cxx_std.is_cxx11_or_greater:
        val = "(unsigned int)(::fundamental::spam::eggs)"
    else:
        val = "(unsigned int)(::fundamental::eggs)"
    assert fcall.arguments[0].default_value == val


def test_constructor_patcher(global_ns):
    typedef__func = global_ns.free_function("typedef__func")
    default_val = typedef__func.arguments[0].default_value
    val = "typedef_::alias()"
    assert default_val == val
