# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations


def test_array_bug_1():
    config = autoconfig.cxx_parsers_cfg.config.clone()
    code = 'int aaaa[2][3][4][5];'
    src_reader = parser.source_reader_t(config)
    global_ns = declarations.get_global_namespace(
        src_reader.read_string(code))
    aaaa_type = global_ns.variable('aaaa').decl_type
    assert 'int [2][3][4][5]' == aaaa_type.decl_string


def test_array_bug_2():
    config = autoconfig.cxx_parsers_cfg.config.clone()
    code = 'int* aaaa[2][3][4][5];'
    src_reader = parser.source_reader_t(config)
    global_ns = declarations.get_global_namespace(
        src_reader.read_string(code))
    aaaa_type = global_ns.variable('aaaa').decl_type
    assert 'int * [2][3][4][5]' == aaaa_type.decl_string


def test_array_bug_3():
    config = autoconfig.cxx_parsers_cfg.config.clone()
    code = 'int aaaa[2];'
    src_reader = parser.source_reader_t(config)
    global_ns = declarations.get_global_namespace(
        src_reader.read_string(code))
    aaaa_type = global_ns.variable('aaaa').decl_type
    assert 'int [2]' == aaaa_type.decl_string


def test_array_bug_4():
    config = autoconfig.cxx_parsers_cfg.config.clone()
    code = 'struct xyz{}; xyz aaaa[2][3];'
    src_reader = parser.source_reader_t(config)
    global_ns = declarations.get_global_namespace(
        src_reader.read_string(code))
    aaaa_type = global_ns.variable('aaaa').decl_type
    assert '::xyz [2][3]' == aaaa_type.decl_string


def test_array_bug_5():
    config = autoconfig.cxx_parsers_cfg.config.clone()
    code = 'char const arr[4] = {};'
    src_reader = parser.source_reader_t(config)
    global_ns = declarations.get_global_namespace(
        src_reader.read_string(code))
    arr_type = global_ns.variable('arr').decl_type
    assert 'char const [4]' == arr_type.decl_string
    assert declarations.is_array(arr_type) is True
    assert declarations.is_const(arr_type) is True


def test_array_bug_6():
    config = autoconfig.cxx_parsers_cfg.config.clone()
    code = 'char volatile arr[4] = {};'
    src_reader = parser.source_reader_t(config)
    global_ns = declarations.get_global_namespace(
        src_reader.read_string(code))
    arr_type = global_ns.variable('arr').decl_type
    assert 'char volatile [4]' == arr_type.decl_string
    assert declarations.is_array(arr_type) is True
    assert declarations.is_volatile(arr_type) is True


def test_array_bug_7():
    config = autoconfig.cxx_parsers_cfg.config.clone()
    code = 'char const volatile arr[4] = {};'
    src_reader = parser.source_reader_t(config)
    global_ns = declarations.get_global_namespace(
        src_reader.read_string(code))
    arr_type = global_ns.variable('arr').decl_type
    assert 'char const volatile [4]' == arr_type.decl_string
    assert declarations.is_array(arr_type) is True
    assert declarations.is_const(arr_type) is True
    assert declarations.is_volatile(arr_type) is True
