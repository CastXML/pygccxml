# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import os
import sys
import getpass

#__pychecker__ = 'limit=1000'
#import pychecker.checker

this_module_dir_path = os.path.abspath ( os.path.dirname( sys.modules[__name__].__file__) )


data_directory = os.path.join( this_module_dir_path, 'data' )
build_directory = os.path.join( this_module_dir_path, 'temp' )

gccxml_path = os.path.join( this_module_dir_path, '..', '..', 'gccxml_bin', 'v09', sys.platform, 'bin' )
gccxml_version = '__GCCXML_09__'

try:
    import pygccxml
    print 'unittests will run on INSTALLED version'
except ImportError:
    sys.path.append( os.path.join( os.curdir, '..' ) )
    import pygccxml
    print 'unittests will run on DEVELOPMENT version'

compiler = pygccxml.utils.native_compiler.get_gccxml_compiler()
compiler = 'msvc71'
print 'GCCXML configured to simulate compiler ', compiler

pygccxml.declarations.class_t.USE_DEMANGLED_AS_NAME = True

class cxx_parsers_cfg:
    keywd = { 'working_directory' : data_directory
              , 'define_symbols' : [ gccxml_version ]
              , 'compiler' : compiler }

    if 'win' in sys.platform:
        keywd['define_symbols'].append( '__PYGCCXML_%s__' % compiler.upper() )
        if 'msvc9' == compiler:
            keywd['define_symbols'].append( '_HAS_TR1=0' )


    if os.path.exists( os.path.join( gccxml_path, 'gccxml' ) ) \
       or os.path.exists( os.path.join( gccxml_path, 'gccxml.exe' ) ):
        keywd[ 'gccxml_path'] = gccxml_path
    gccxml = pygccxml.parser.gccxml_configuration_t( **keywd )

    #~ pdb_loader = None
    #~ if sys.platform == 'win32':
        #~ from pygccxml.msvc import mspdb
        #~ pdb_file = os.path.join( data_directory, 'msvc_build', 'Debug', 'msvc_build.pdb' )
        #~ if os.path.exists( pdb_file ):
            #~ pdb_loader = mspdb.decl_loader_t( pdb_file )
            #~ pdb_loader.read()

#~ def get_pdb_global_ns():
    #~ if cxx_parsers_cfg.pdb_loader:
        #~ return cxx_parsers_cfg.pdb_loader.global_ns

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
