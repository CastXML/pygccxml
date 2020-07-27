# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import os
import sys
import unittest
import platform

from . import decl_string_tester
from . import declaration_files_tester
from . import declarations_comparison_tester
from . import declarations_tester
from . import file_cache_tester
from . import gccxml_runner_tester
from . import project_reader_correctness_tester
from . import source_reader_tester
from . import start_with_declarations_tester
from . import templates_tester
from . import type_traits_tester
from . import core_tester
from . import xmlfile_reader_tester
from . import text_reader_tester
from . import hierarchy_traveling
from . import patcher_tester
from . import call_invocation_tester
from . import bit_fields_tester
from . import complex_types_tester
from . import cached_source_file_tester
from . import variable_matcher_tester
from . import namespace_matcher_tester
from . import calldef_matcher_tester
from . import filters_tester
from . import cache_enums_tester
from . import decl_printer_tester
from . import typedefs_tester
from . import non_copyable_classes_tester
from . import unnamed_enums_bug_tester
from . import vector_traits_tester
from . import string_traits_tester
from . import declarations_cache_tester
from . import has_binary_operator_traits_tester
from . import algorithms_cache_tester
from . import dependencies_tester
from . import free_operators_tester
from . import remove_template_defaults_tester
from . import find_container_traits_tester
from . import attributes_tester
from . import type_as_exception_bug_tester
from . import copy_constructor_tester
from . import plain_c_tester
from . import function_traits_tester
from . import better_templates_matcher_tester
from . import declaration_matcher_tester
from . import calling_convention_tester
from . import const_volatile_arg_tester
from . import array_bug_tester
from . import gccxml10184_tester
from . import gccxml10185_tester
from . import inline_specifier_tester
from . import test_create_decl_string
from . import pep8_tester
from . import example_tester
from . import test_utils
from . import test_va_list_tag_removal
from . import test_copy_constructor
from . import test_cpp_standards
from . import unnamed_classes_tester
from . import test_map_gcc5
from . import test_argument_without_name
from . import test_smart_pointer
from . import test_pattern_parser
from . import test_function_pointer
from . import test_directory_cache
from . import test_config
from . import deprecation_tester
from . import test_xml_generators
from . import test_non_copyable_recursive
from . import test_castxml_wrong_epic
from . import test_elaborated_types
from . import test_order
from . import test_find_noncopyable_vars
from . import test_hash
from . import test_null_comparison

testers = [
    pep8_tester,
    decl_string_tester,
    declaration_files_tester,
    declarations_comparison_tester,
    declarations_tester, file_cache_tester,
    gccxml_runner_tester,
    project_reader_correctness_tester,
    source_reader_tester,
    start_with_declarations_tester,
    templates_tester,
    core_tester,
    xmlfile_reader_tester,
    text_reader_tester,
    hierarchy_traveling,
    call_invocation_tester,
    bit_fields_tester,
    complex_types_tester,
    cached_source_file_tester,
    variable_matcher_tester,
    namespace_matcher_tester,
    calldef_matcher_tester,
    filters_tester,
    cache_enums_tester,
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
    type_as_exception_bug_tester,
    plain_c_tester,
    function_traits_tester,
    better_templates_matcher_tester,
    declaration_matcher_tester,
    calling_convention_tester,
    const_volatile_arg_tester,
    array_bug_tester,
    gccxml10184_tester,
    gccxml10185_tester,
    inline_specifier_tester,
    test_create_decl_string,
    test_copy_constructor,
    unnamed_classes_tester,
    test_map_gcc5,
    test_argument_without_name,
    test_smart_pointer,
    test_pattern_parser,
    test_function_pointer,
    test_directory_cache,
    test_config,
    test_utils,
    test_cpp_standards,
    test_va_list_tag_removal,
    decl_printer_tester,
    attributes_tester,
    type_traits_tester,
    remove_template_defaults_tester,
    patcher_tester,
    find_container_traits_tester,
    deprecation_tester,
    test_xml_generators,
    test_non_copyable_recursive,
    test_castxml_wrong_epic,
    test_elaborated_types,
    test_order,
    test_find_noncopyable_vars,
    test_hash,
    test_null_comparison,
]

if platform.system() != 'Windows':
    # Known to fail under windows with VS2013
    testers.append(example_tester)

if 'posix' in os.name:
    testers.append(copy_constructor_tester)

if os.path.isfile("test_cost.log"):
    # Remove the cost log file when tests are run again.
    # See the parser_test_case which generates this file.
    os.remove("test_cost.log")  # pragma: no cover


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
        if error_desc not in description:  # pragma: no cover
            return 1  # pragma: no cover
    return 0


if __name__ == "__main__":
    sys.exit(run_suite())
