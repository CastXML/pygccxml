# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import os

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations

TEST_FILES1 = [
    'core_types.hpp',
    'core_ns_join_1.hpp',
    'core_ns_join_2.hpp',
    'core_ns_join_3.hpp',
    'core_membership.hpp',
    'core_class_hierarchy.hpp',
    'core_diamand_hierarchy_base.hpp',
    'core_diamand_hierarchy_derived1.hpp',
    'core_diamand_hierarchy_derived2.hpp',
    'core_diamand_hierarchy_final_derived.hpp',
    'core_overloads_1.hpp',
    'core_overloads_2.hpp'
]

TEST_FILES2 = [
    'separate_compilation/data.h',
    'separate_compilation/base.h',
    'separate_compilation/derived.h'
]


def test_correctness():
    for src in TEST_FILES1:
        __test_correctness_impl(src)


def __test_correctness_impl(file_name):
    config = autoconfig.cxx_parsers_cfg.config.clone()
    prj_reader = parser.project_reader_t(config)
    prj_decls = prj_reader.read_files(
        [file_name] * 2,
        compilation_mode=parser.COMPILATION_MODE.FILE_BY_FILE)
    src_reader = parser.source_reader_t(config)
    src_decls = src_reader.read_file(file_name)
    if src_decls != prj_decls:
        s = src_decls[0]
        p = prj_decls[0]
        bdir = autoconfig.build_directory
        with open(os.path.join(bdir, file_name + '.sr.txt'), 'w+') as sr:
            with open(
                    os.path.join(bdir, file_name + '.pr.txt'), 'w+') as pr:

                declarations.print_declarations(
                    s, writer=lambda x: sr.write(l + os.linesep))
                declarations.print_declarations(
                    p, writer=lambda x: pr.write(l + os.linesep))
        raise (
            f"There is a difference between declarations in file {file_name}."
            )


def test_separate_compilation():
    config = autoconfig.cxx_parsers_cfg.config.clone()
    prj_reader = parser.project_reader_t(config)
    prj_decls = prj_reader.read_files(
        TEST_FILES2,
        compilation_mode=parser.COMPILATION_MODE.FILE_BY_FILE)
    src_reader = parser.source_reader_t(config)
    src_decls = src_reader.read_file('separate_compilation/all.h')

    declarations.dump_declarations(
        src_decls,
        os.path.join(
            autoconfig.build_directory, 'separate_compilation.sr.txt'))

    declarations.dump_declarations(
        prj_decls,
        os.path.join(
            autoconfig.build_directory, 'separate_compilation.pr.txt'))

    assert src_decls == prj_decls
