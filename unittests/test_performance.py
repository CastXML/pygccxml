# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import os
import sys
import time
import hotshot
import hotshot.stats
import autoconfig
from pygccxml import *



dcache_file_name = os.path.join( autoconfig.data_directory, 'pygccxml.cache' )
if os.path.exists(dcache_file_name):
    os.remove(dcache_file_name)

def test_on_windows_dot_h():
    windows_header = r"D:\Program Files\Microsoft Visual Studio .NET 2003\Vc7\PlatformSDK\Include\windows.h"
    clock_prev = time.clock()
    dcache = parser.file_cache_t(dcache_file_name)
    reader = parser.source_reader_t( parser.config_t(gccxml_path=autoconfig.gccxml_path), dcache )
    reader.read_file(windows_header)
    dcache.flush()
    clock_now = time.clock()
    print('without cache: %f seconds' % ( clock_now - clock_prev ))

    clock_prev = time.clock()
    dcache = parser.file_cache_t(dcache_file_name)
    reader = parser.source_reader_t( parser.config_t(gccxml_path=autoconfig.gccxml_path), dcache )
    reader.read_file(windows_header)
    clock_now = time.clock()
    print('with cache   : %f seconds' % ( clock_now - clock_prev ))

#-########################################################################################
#- testing include_std.hpp
def test_source_on_include_std_dot_hpp():
    include_std_header = os.path.join( autoconfig.data_directory, 'include_std.hpp' )
    clock_prev = time.clock()
    dcache = parser.file_cache_t(dcache_file_name)
    reader = parser.source_reader_t( parser.config_t(gccxml_path=autoconfig.gccxml_path), dcache )
    reader.read_file(include_std_header)
    dcache.flush()
    clock_now = time.clock()
    print('without cache: %f seconds' % ( clock_now - clock_prev ))

    clock_prev = time.clock()
    dcache = parser.file_cache_t(dcache_file_name)
    reader = parser.source_reader_t( parser.config_t(gccxml_path=autoconfig.gccxml_path), dcache )
    reader.read_file(include_std_header)
    clock_now = time.clock()
    print('with cache   : %f seconds' % ( clock_now - clock_prev ))


#-########################################################################################
#- testing include_std.hpp
def test_project_on_include_std_dot_hpp():
    include_std_header = os.path.join( autoconfig.data_directory, 'include_std.hpp' )
    clock_prev = time.clock()
    dcache = parser.file_cache_t(dcache_file_name)
    reader = parser.project_reader_t( parser.config_t(gccxml_path=autoconfig.gccxml_path), dcache )
    reader.read_files([include_std_header])
    dcache.flush()
    clock_now = time.clock()
    print('without cache: %f seconds' % ( clock_now - clock_prev ))

    clock_prev = time.clock()
    dcache = parser.file_cache_t(dcache_file_name)
    reader = parser.project_reader_t( parser.config_t(gccxml_path=autoconfig.gccxml_path), dcache )
    reader.read_files([include_std_header])
    clock_now = time.clock()
    print('with cache   : %f seconds' % ( clock_now - clock_prev ))

def profile_project():
    include_std_header = os.path.join( autoconfig.data_directory, 'include_std.hpp' )
    reader = parser.project_reader_t( parser.config_t(gccxml_path=autoconfig.gccxml_path) )
    reader.read_files([include_std_header])

def profile_project2():
    include_std_header = r"D:\Program Files\Microsoft Visual Studio .NET 2003\Vc7\PlatformSDK\Include\windows.h"
    reader = parser.project_reader_t( parser.config_t(gccxml_path=autoconfig.gccxml_path) )
    reader.read_files([include_std_header])

def test_on_big_file( file_name, count ):
    file_name = os.path.join( autoconfig.data_directory, file_name )
    for i in range( count ):
        reader = parser.project_reader_t( parser.config_t(gccxml_path=autoconfig.gccxml_path) )
        decls = reader.read_files([parser.create_gccxml_fc( file_name )])
        global_ns = declarations.get_global_namespace( decls )
        global_ns.init_optimizer()

def parse_big_file():
    reader = parser.project_reader_t( parser.config_t(gccxml_path=autoconfig.gccxml_path) )
    reader.read_files([parser.create_gccxml_fc( os.path.join( autoconfig.data_directory, 'big.xml' ) )])
    reader.read_files([parser.create_gccxml_fc( os.path.join( autoconfig.data_directory, 'big.xml' ) )])
    reader.read_files([parser.create_gccxml_fc( os.path.join( autoconfig.data_directory, 'big.xml' ) )])


if __name__ == "__main__":

    #~ test_on_windows_dot_h()
    #~ test_source_on_include_std_dot_hpp()
    #~ test_project_on_include_std_dot_hpp()
    print('running')
    prof = hotshot.Profile( 'parser.prof' )
    prof.runcall( lambda:  test_on_big_file( 'big2.xml', 1 ) )
    stats = hotshot.stats.load("parser.prof")
    stats.sort_stats('time', 'calls')
    stats.print_stats(30)
    print('running - done')
    #~ print 'loading file'
    #~ pdata = pstats.Stats('pygccxml.profile')
    #~ print 'loading file - done'
    #~ print 'striping dirs'
    #~ pdata.strip_dirs()
    #~ print 'striping dirs - done'
    #~ print 'sorting stats'
    #~ pdata.sort_stats('time').print_stats(476)
    #~ print 'sorting stats - done'
    #pdata.print_callers('find_all_declarations')
