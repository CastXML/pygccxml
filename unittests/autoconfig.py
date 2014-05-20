# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import os
import sys
import platform

# os.environ['PYCHECKER'] = '--limit=1000 -q --no-argsused'
# import pychecker.checker

this_module_dir_path = os.path.abspath(
    os.path.dirname(
        sys.modules[__name__].__file__))

data_directory = os.path.join(this_module_dir_path, 'data')
build_directory = os.path.join(this_module_dir_path, 'temp')

gccxml_path = os.path.join(
    this_module_dir_path, '..', '..', 'gccxml_bin', 'v09',
    platform.system(), platform.machine(), 'bin')
if not os.path.exists(gccxml_path):
    gccxml_path = os.path.join(
        this_module_dir_path, '..', '..', 'gccxml_bin', 'v09',
        sys.platform, 'bin')
gccxml_version = '__GCCXML_09__'

sys.path.insert(0, os.path.join(os.curdir, '..'))
import pygccxml
import pygccxml.declarations
import pygccxml.parser

pygccxml.declarations.class_t.USE_DEMANGLED_AS_NAME = True


class cxx_parsers_cfg:
    gccxml = pygccxml.parser.load_gccxml_configuration(
        'gccxml.cfg',
        gccxml_path=gccxml_path,
        working_directory=data_directory,
        compiler=pygccxml.utils.native_compiler.get_gccxml_compiler())

    gccxml.define_symbols.append(gccxml_version)
    if 'nt' == os.name:
        gccxml.define_symbols.append(
            '__PYGCCXML_%s__' %
            gccxml.compiler.upper())
        if 'msvc9' == gccxml.compiler:
            gccxml.define_symbols.append('_HAS_TR1=0')

print(
    'GCCXML configured to simulate compiler %s' %
    cxx_parsers_cfg.gccxml.compiler)
