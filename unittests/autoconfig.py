# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import os
import sys
import getpass

#__pychecker__ = 'limit=1000'
#import pychecker.checker

this_module_dir_path = os.path.abspath ( os.path.dirname( sys.modules[__name__].__file__) )

compiler = None
data_directory = os.path.join( this_module_dir_path, 'data' )
build_directory = os.path.join( this_module_dir_path, 'temp' )

gccxml_07_path = os.path.join( this_module_dir_path, '..', '..', 'gccxml_bin', 'v07', sys.platform, 'bin' )
gccxml_09_path = os.path.join( this_module_dir_path, '..', '..', 'gccxml_bin', 'v09', sys.platform, 'bin' )

gccxml_path = gccxml_09_path

gccxml_version = '__GCCXML_07__'
if '09' in gccxml_path:
    gccxml_version = '__GCCXML_09__'

print 'compiler: ', gccxml_version

if sys.platform == 'win32':
    compiler = 'msvc71'

try:
    import pygccxml
    print 'unittests will run on INSTALLED version'
except ImportError:
    sys.path.append( os.path.join( os.curdir, '..' ) )
    import pygccxml
    print 'unittests will run on DEVELOPMENT version'

pygccxml.declarations.class_t.USE_DEMANGLED_AS_NAME = True

class cxx_parsers_cfg:
    gccxml = None
    if os.path.exists( os.path.join( gccxml_path, 'gccxml' ) ) \
       or os.path.exists( os.path.join( gccxml_path, 'gccxml.exe' ) ):
        gccxml = pygccxml.parser.gccxml_configuration_t( gccxml_path=gccxml_path
                                                        , working_directory=data_directory
                                                        , define_symbols=[ gccxml_version ]
                                                        , compiler=compiler )
    pdb_loader = None
    if sys.platform == 'win32':
        from pygccxml.msvc import pdb
        pdb_file = os.path.join( data_directory, 'msvc_build', 'Debug', 'msvc_build.pdb' )
        pdb_loader = pdb.decl_loader_t( pdb_file )
        pdb_loader.read()

def get_pdb_global_ns():
    return cxx_parsers_cfg.pdb_loader.global_ns

#~ try:
    #~ import pydsc
    #~ pydsc.include( r'D:\pygccxml_sources\sources\pygccxml_dev' )
    #~ pydsc.ignore( [ 'Yakovenko'
             #~ , 'Bierbaum'
             #~ , 'org'
             #~ , 'http'
             #~ , 'bool'
             #~ , 'str'
             #~ , 'www'
             #~ , 'param'
             #~ , 'txt'
             #~ , 'decl'
             #~ , 'decls'
             #~ , 'namespace'
             #~ , 'namespaces'
             #~ , 'enum'
             #~ , 'const'
             #~ , 'GCC'
             #~ , 'xcc'
             #~ , 'TODO'
             #~ , 'typedef'
             #~ , 'os'
             #~ , 'normcase'
             #~ , 'normpath'
             #~ , 'scopedef'
             #~ , 'ira'#part of Matthias mail address
             #~ , 'uka'#part of Matthias mail address
             #~ , 'de'#part of Matthias mail address
             #~ , 'dat'#file extension of directory cache
             #~ , 'config'#parameter description
             #~ , 'gccxml'#parameter description
             #~ , 'Py++'
             #~ , 'pygccxml'
             #~ , 'calldef'
             #~ , 'XXX'
             #~ , 'wstring'
             #~ , 'py'
             #~ ] )
#~ except ImportError:
    #~ pass
