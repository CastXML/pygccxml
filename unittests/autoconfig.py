# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import os
import sys
import getpass



#~ os.environ['PYCHECKER'] = '--limit=1000 -q --no-argsused'
#~ import pychecker.checker

this_module_dir_path = os.path.abspath ( os.path.dirname( sys.modules[__name__].__file__) )

sys.path.append( os.path.abspath( os.path.join( this_module_dir_path, '..', '..', 'pydsc_dev' ) ) )

import pydsc
pydsc.ignore_dictionary( 'ignore_dictionary.txt' )
pydsc.set_text_preprocessor( pydsc.sphinx_preprocessor )
pydsc.include_paths( os.path.join( this_module_dir_path, '..', '..', 'pygccxml_dev' ) )

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


pygccxml.declarations.class_t.USE_DEMANGLED_AS_NAME = True

class cxx_parsers_cfg:
    gccxml = pygccxml.parser.load_gccxml_configuration( 'gccxml.cfg'
                                                        , gccxml_path=gccxml_path
                                                        , working_directory=data_directory
                                                        , compiler=pygccxml.utils.native_compiler.get_gccxml_compiler() )

    gccxml.define_symbols.append( gccxml_version )
    if 'win' in sys.platform:
        gccxml.define_symbols.append( '__PYGCCXML_%s__' % gccxml.compiler.upper() )
        if 'msvc9' == gccxml.compiler:
            gccxml.define_symbols.append( '_HAS_TR1=0' )

print 'GCCXML configured to simulate compiler ', cxx_parsers_cfg.gccxml.compiler
