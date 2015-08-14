# Copyright 2014-2015 Insight Software Consortium.
# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import os
import sys
import logging

this_module_dir_path = os.path.abspath(
    os.path.dirname(sys.modules[__name__].__file__))

data_directory = os.path.join(this_module_dir_path, 'data')
build_directory = os.path.join(this_module_dir_path, 'temp')

sys.path.insert(0, os.path.join(os.curdir, '..'))
# The tests are run on the parent pygccxml directory, not the one
# in site-packages. Insert the directory's path.
sys.path.insert(0, "../pygccxml")

import pygccxml  # nopep8
import pygccxml.declarations  # nopep8
import pygccxml.parser  # nopep8
import pygccxml.utils  # nopep8

# Set logging level
logger = pygccxml.utils.loggers.cxx_parser
logger.setLevel(logging.INFO)

# Find out the c++ parser (gccxml or castxml)
parser_path, parser_name = pygccxml.utils.find_cpp_parser()

pygccxml.declarations.class_t.USE_DEMANGLED_AS_NAME = True


class cxx_parsers_cfg:
    gccxml = pygccxml.parser.load_gccxml_configuration(
        'gccxml.cfg',
        gccxml_path=parser_path,
        working_directory=data_directory,
        compiler=pygccxml.utils.native_compiler.get_gccxml_compiler(),
        xml_generator=parser_name)

    if parser_name == 'gccxml':
        gccxml.define_symbols.append('__GCCXML_09__')

    if 'nt' == os.name:
        gccxml.define_symbols.append(
            '__PYGCCXML_%s__' %
            gccxml.compiler.upper())
        if 'msvc9' == gccxml.compiler:
            gccxml.define_symbols.append('_HAS_TR1=0')

print(
    '%s configured to simulate compiler %s' %
    (parser_name.title(), cxx_parsers_cfg.gccxml.compiler))
