# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import os
import sys
import timeit
import hotshot
import hotshot.stats

this_module_dir_path = os.path.abspath(
    os.path.dirname(sys.modules[__name__].__file__))

sys.path.insert(1, os.path.join(this_module_dir_path, '../../'))
sys.path.insert(2, os.path.join(this_module_dir_path, '../'))

import autoconfig  # nopep8
from pygccxml import parser  # nopep8
from pygccxml import declarations  # nopep8

dcache_file_name = os.path.join(autoconfig.data_directory, 'pygccxml.cache')
if os.path.exists(dcache_file_name):
    os.remove(dcache_file_name)


def test_on_windows_dot_h():
    he = r"2003\Vc7\PlatformSDK\Include\windows.h"
    windows_header = r"D:\Program Files\Microsoft Visual Studio .NET " + he
    clock_prev = timeit.default_timer()
    dcache = parser.file_cache_t(dcache_file_name)
    reader = parser.source_reader_t(
        parser.xml_generator_configuration_t(
            xml_generator_path=autoconfig.generator_path),
        dcache)
    reader.read_file(windows_header)
    dcache.flush()
    clock_now = timeit.default_timer()
    print('without cache: %f seconds' % (clock_now - clock_prev))

    clock_prev = timeit.default_timer()
    dcache = parser.file_cache_t(dcache_file_name)
    reader = parser.source_reader_t(
        parser.xml_generator_configuration_t(
            xml_generator_path=autoconfig.generator_path),
        dcache)
    reader.read_file(windows_header)
    clock_now = timeit.default_timer()
    print('with cache   : %f seconds' % (clock_now - clock_prev))

#########################################################################
# testing include_std.hpp


def test_source_on_include_std_dot_hpp():
    include_std_header = os.path.join(
        autoconfig.data_directory,
        'include_std.hpp')
    clock_prev = timeit.default_timer()
    dcache = parser.file_cache_t(dcache_file_name)
    reader = parser.source_reader_t(
        parser.xml_generator_configuration_t(
            xml_generator_path=autoconfig.generator_path),
        dcache)
    reader.read_file(include_std_header)
    dcache.flush()
    clock_now = timeit.default_timer()
    print('without cache: %f seconds' % (clock_now - clock_prev))

    clock_prev = timeit.default_timer()
    dcache = parser.file_cache_t(dcache_file_name)
    reader = parser.source_reader_t(
        parser.xml_generator_configuration_t(
            xml_generator_path=autoconfig.generator_path),
        dcache)
    reader.read_file(include_std_header)
    clock_now = timeit.default_timer()
    print('with cache   : %f seconds' % (clock_now - clock_prev))


#########################################################################
# testing include_std.hpp
def test_project_on_include_std_dot_hpp():
    include_std_header = os.path.join(
        autoconfig.data_directory,
        'include_std.hpp')
    clock_prev = timeit.default_timer()
    dcache = parser.file_cache_t(dcache_file_name)
    reader = parser.project_reader_t(
        parser.xml_generator_configuration_t(
            xml_generator_path=autoconfig.generator_path),
        dcache)
    reader.read_files([include_std_header])
    dcache.flush()
    clock_now = timeit.default_timer()
    print('without cache: %f seconds' % (clock_now - clock_prev))

    clock_prev = timeit.default_timer()
    dcache = parser.file_cache_t(dcache_file_name)
    reader = parser.project_reader_t(
        parser.xml_generator_configuration_t(
            xml_generator_path=autoconfig.generator_path),
        dcache)
    reader.read_files([include_std_header])
    clock_now = timeit.default_timer()
    print('with cache   : %f seconds' % (clock_now - clock_prev))


def profile_project():
    include_std_header = os.path.join(
        autoconfig.data_directory,
        'include_std.hpp')
    reader = parser.project_reader_t(
        parser.xml_generator_configuration_t(
            xml_generator_path=autoconfig.generator_path))
    reader.read_files([include_std_header])


def profile_project2():
    he = r"2003\Vc7\PlatformSDK\Include\windows.h"
    include_std_header = r"D:\Program Files\Microsoft Visual Studio .NET " + he
    reader = parser.project_reader_t(
        parser.xml_generator_configuration_t(
            xml_generator_path=autoconfig.generator_path))
    reader.read_files([include_std_header])


def test_on_big_file(file_name, count):
    file_name = os.path.join(autoconfig.data_directory, file_name)
    for i in range(count):
        reader = parser.project_reader_t(
            parser.xml_generator_configuration_t(
                xml_generator_path=autoconfig.generator_path))
        decls = reader.read_files([parser.create_gccxml_fc(file_name)])
        global_ns = declarations.get_global_namespace(decls)
        global_ns.init_optimizer()


if __name__ == "__main__":

    # test_on_windows_dot_h()
    # test_source_on_include_std_dot_hpp()
    # test_project_on_include_std_dot_hpp()
    print('running')
    prof = hotshot.Profile('parser.prof')
    prof.runcall(lambda: test_on_big_file('itkImage.xml', 1))
    stats = hotshot.stats.load("parser.prof")
    stats.sort_stats('time', 'calls')
    stats.print_stats(30)
    print('running - done')
    # print 'loading file'
    # pdata = pstats.Stats('pygccxml.profile')
    # print 'loading file - done'
    # print 'striping dirs'
    # pdata.strip_dirs()
    # print 'striping dirs - done'
    # print 'sorting stats'
    # pdata.sort_stats('time').print_stats(476)
    # print 'sorting stats - done'
    # pdata.print_callers('find_all_declarations')
