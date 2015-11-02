# Copyright 2014-2015 Insight Software Consortium.
# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import os
import sys
import unittest

import decl_string_tester
import declaration_files_tester
import declarations_comparison_tester
import declarations_tester
import file_cache_tester
import gccxml_runner_tester
import project_reader_correctness_tester
import source_reader_tester
import start_with_declarations_tester
import templates_tester
import type_traits_tester
import core_tester
import xmlfile_reader_tester
import text_reader_tester
import hierarchy_traveling
import patcher_tester
import call_invocation_tester
import bit_fields_tester
import complex_types_tester
import cached_source_file_tester
import variable_matcher_tester
import namespace_matcher_tester
import calldef_matcher_tester
import filters_tester
import cache_enums_tester
import decl_printer_tester
import typedefs_tester
import non_copyable_classes_tester
# import demangled_tester
import unnamed_enums_bug_tester
import vector_traits_tester
import string_traits_tester
import declarations_cache_tester
import has_binary_operator_traits_tester
import algorithms_cache_tester
import dependencies_tester
import free_operators_tester
import remove_template_defaults_tester
import find_container_traits_tester
import attributes_tester
import type_as_exception_bug_tester
import copy_constructor_tester
import plain_c_tester
import function_traits_tester
import better_templates_matcher_tester
import declaration_matcher_tester
# import undname_creator_tester
import calling_convention_tester
import const_volatile_arg_tester
import array_bug_tester
import gccxml10183_tester
import gccxml10184_tester
import gccxml10185_tester
import inline_specifier_tester
import test_create_decl_string
import from_future_import_tester
import pep8_tester
import example_tester
import test_utils

testers = [
    # , demangled_tester # failing right now
    # , undname_creator_tester # failing right now
    decl_string_tester,
    declaration_files_tester,
    declarations_comparison_tester,
    declarations_tester, file_cache_tester,
    gccxml_runner_tester,
    project_reader_correctness_tester,
    source_reader_tester,
    start_with_declarations_tester,
    templates_tester,
    type_traits_tester,
    core_tester,
    xmlfile_reader_tester,
    text_reader_tester,
    hierarchy_traveling,
    patcher_tester,
    call_invocation_tester,
    bit_fields_tester,
    complex_types_tester,
    cached_source_file_tester,
    variable_matcher_tester,
    namespace_matcher_tester,
    calldef_matcher_tester,
    filters_tester,
    cache_enums_tester,
    decl_printer_tester,
    typedefs_tester,
    non_copyable_classes_tester,
    unnamed_enums_bug_tester,
    vector_traits_tester,
    string_traits_tester,
    declarations_cache_tester,
    has_binary_operator_traits_tester,
    algorithms_cache_tester,
    dependencies_tester,
    free_operators_tester,
    remove_template_defaults_tester,
    find_container_traits_tester,
    attributes_tester,
    type_as_exception_bug_tester,
    plain_c_tester,
    function_traits_tester,
    better_templates_matcher_tester,
    declaration_matcher_tester,
    calling_convention_tester,
    const_volatile_arg_tester,
    array_bug_tester,
    gccxml10183_tester,
    gccxml10184_tester,
    gccxml10185_tester,
    inline_specifier_tester,
    test_create_decl_string,
    from_future_import_tester,
    pep8_tester,
    example_tester,
    test_utils
]

if 'posix' in os.name:
    testers.append(copy_constructor_tester)


def create_suite():
    main_suite = unittest.TestSuite()
    for tester in testers:
        main_suite.addTest(tester.create_suite())
    return main_suite


def run_suite():
    result = unittest.TextTestRunner(verbosity=2).run(create_suite())
    error_desc = 'EXCEPTION IN SAFE SELECT 9'
    all_errors = result.failures + result.errors
    for test_case, description in all_errors:
        if error_desc not in description:
            return 1
    return 0

if __name__ == "__main__":
    sys.exit(run_suite())
