# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import argparse
import multiprocessing as mp
import os
import platform
import sys
import unittest

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
    declarations_tester,
    file_cache_tester,
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


def create_suite(testers):
    main_suite = unittest.TestSuite()
    for tester in testers:
        main_suite.addTest(tester.create_suite())
    return main_suite


def run_suite(indices):
    suite = create_suite([testers[i] for i in indices])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    error_desc = 'EXCEPTION IN SAFE SELECT 9'
    all_errors = result.failures + result.errors
    error_count = 0
    for test_case, description in all_errors:
        if error_desc not in description:  # pragma: no cover
            error_count += 1  # pragma: no cover
    return error_count


def split_item_list(item_list, item_cost_func, num_chunks):
    """Split @p item_list into @p num_chunks such that all chunks have similar
    sum item cost (as computed by @p item_cost_func)."""
    # TODO(eric.cousineau): Just use third party lib?
    # TODO(eric.cousineau): Sort items by cost first, then for each chunk, add
    # first item, then iterate until we exhaust the cost?
    if num_chunks == 1:
        return [item_list]
    item_costs = [item_cost_func(x) for x in item_list]
    cost_total = sum(item_costs)
    chunk_cost_target = cost_total / num_chunks
    chunk_list = []
    chunk = []
    chunk_cost = 0
    for item, item_cost in zip(item_list, item_costs):
        past_cost_target = (chunk_cost >= chunk_cost_target)
        need_more_chunks = (len(chunk_list) + 1 < num_chunks)
        if past_cost_target and need_more_chunks:
            # Store current chunk (with previous item(s)), and start a new
            # chunk.
            chunk_list.append(chunk)
            chunk = []
            chunk_cost = 0
        chunk_cost += item_cost
        chunk.append(item)
    # Append final chunk.
    chunk_list.append(chunk)
    assert len(chunk_list) <= num_chunks, (len(chunk_list), num_chunks)
    return chunk_list


def flatten_suite(suite):
    tests = []
    for test in suite:
        if isinstance(test, unittest.TestSuite):
            tests += flatten_suite(test)
        else:
            tests += [test]
    return tests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-j", "--jobs", type=int, default=0)
    args = parser.parse_args()

    # Consider using an actual parallelization for unittest:
    # https://stackoverflow.com/q/4710142/7829525
    job_count = args.jobs
    indices = list(range(len(testers)))
    if job_count == 0:
        error_counts = [run_suite(indices)]
    else:

        def index_cost(index):
            suite = create_suite([testers[index]])
            tests = flatten_suite(suite)
            return len(tests)

        indices_chunks = split_item_list(indices, index_cost, job_count)
        job_count = len(indices_chunks)
        with mp.Pool(job_count) as pool:
            error_counts = pool.map(run_suite, indices_chunks)
    error_count = sum(error_counts)
    if error_count > 0:
        print()
        print("FAIL: {} total error(s)".format(error_count))
    sys.exit(error_count)


if __name__ == "__main__":
    main()
