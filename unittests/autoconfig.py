# Copyright 2014-2016 Insight Software Consortium.
# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import os
import sys
import logging
import warnings

this_module_dir_path = os.path.abspath(
    os.path.dirname(sys.modules[__name__].__file__))

data_directory = os.path.join(this_module_dir_path, 'data')
build_directory = os.path.join(this_module_dir_path, 'temp')

sys.path.insert(1, os.path.join(os.curdir, '..'))
# The tests are run on the parent pygccxml directory, not the one
# in site-packages. Insert the directory's path.
sys.path.insert(1, "../pygccxml")

import pygccxml  # nopep8
import pygccxml.declarations  # nopep8
import pygccxml.parser  # nopep8
import pygccxml.utils  # nopep8

# We want to make sure we throw an error for ALL the warnings during the
# tests. This will allow us to be notified by the build bots, so that the
# warnings can be fixed.
warnings.simplefilter("error", Warning)

# Set logging level
pygccxml.utils.loggers.set_level(logging.INFO)

# Find out the c++ parser (gccxml or castxml)
generator_path, generator_name = pygccxml.utils.find_xml_generator()

pygccxml.declarations.class_t.USE_DEMANGLED_AS_NAME = True


class cxx_parsers_cfg(object):
    gccxml = pygccxml.parser.load_xml_generator_configuration(
        'xml_generator.cfg',
        xml_generator_path=generator_path,
        working_directory=data_directory,
        compiler=pygccxml.utils.native_compiler.get_gccxml_compiler(),
        xml_generator=generator_name)

    if generator_name == 'gccxml':
        gccxml.define_symbols.append('__GCCXML_09__')

    if 'nt' == os.name:
        gccxml.define_symbols.append(
            '__PYGCCXML_%s__' %
            gccxml.compiler.upper())
        if 'msvc9' == gccxml.compiler:
            gccxml.define_symbols.append('_HAS_TR1=0')

if cxx_parsers_cfg.gccxml.xml_generator:
    generator_name = cxx_parsers_cfg.gccxml.xml_generator
if cxx_parsers_cfg.gccxml.xml_generator_path:
    generator_path = cxx_parsers_cfg.gccxml.xml_generator_path

print(
    '%s configured to simulate compiler %s' %
    (generator_name.title(), cxx_parsers_cfg.gccxml.compiler))
