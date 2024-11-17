# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest

from . import autoconfig


from pygccxml import parser
from pygccxml import declarations

TEST_FILES = "core_ns_join_1.hpp"


def __check_result(decls):
    E11 = declarations.find_declaration(decls, fullname='::E11')
    assert E11 is not None
    ns12 = declarations.find_declaration(decls, fullname='::ns::ns12')
    assert ns12 is not None
    E13 = declarations.find_declaration(ns12.declarations, name='E13')
    assert E13 is not None
    E14 = declarations.find_declaration(decls, name='E14')
    assert E14 is None


def test_simple_start_with_declarations():
    config = autoconfig.cxx_parsers_cfg.config.clone()
    config.start_with_declarations.extend(['E11', 'ns::ns12::E13'])
    decls = parser.parse([TEST_FILES], config)
    __check_result(decls)


def test_project_reader_file_by_file_start_with_declarations():
    config = autoconfig.cxx_parsers_cfg.config.clone()
    config.start_with_declarations.extend(['E11', 'ns::ns12::E13'])
    reader = parser.project_reader_t(config)
    decls = reader.read_files(
        [parser.file_configuration_t(
            TEST_FILES, config.start_with_declarations)],
        parser.COMPILATION_MODE.FILE_BY_FILE)
    __check_result(decls)


def test_project_reader_all_at_once_start_with_declarations():
    config = autoconfig.cxx_parsers_cfg.config.clone()
    config.start_with_declarations.extend(['E11', 'ns::ns12::E13'])
    reader = parser.project_reader_t(config)
    decls = reader.read_files(
        [parser.file_configuration_t(
            TEST_FILES, config.start_with_declarations)],
        parser.COMPILATION_MODE.ALL_AT_ONCE)
    __check_result(decls)
