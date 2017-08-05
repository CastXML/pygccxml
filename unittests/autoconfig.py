# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import os
import sys
import logging
import warnings
import platform

# Prevents copy.deepcopy RecursionError in some tests (Travis build)
sys.setrecursionlimit(10000)

this_module_dir_path = os.path.abspath(
    os.path.dirname(sys.modules[__name__].__file__))

data_directory = os.path.join(this_module_dir_path, 'data')
build_directory = os.path.join(this_module_dir_path, 'temp')

sys.path.insert(1, os.path.join(os.curdir, '..'))
# The tests are run on the parent pygccxml directory, not the one
# in site-packages. Insert the directory's path.
sys.path.insert(1, "../pygccxml")

from pygccxml import parser  # nopep8
from pygccxml import utils  # nopep8

# We want to make sure we throw an error for ALL the warnings during the
# tests. This will allow us to be notified by the build bots, so that the
# warnings can be fixed.
warnings.simplefilter("error", Warning)

# Set logging level
utils.loggers.set_level(logging.CRITICAL)

# Find out the c++ parser (gccxml or castxml)
generator_path, generator_name = utils.find_xml_generator()


class cxx_parsers_cfg(object):
    config = parser.load_xml_generator_configuration(
        os.path.normpath(this_module_dir_path + '/xml_generator.cfg'),
        xml_generator_path=generator_path,
        working_directory=data_directory,
        xml_generator=generator_name)

    if platform.system() == 'Windows':
        config.define_symbols.append('_HAS_EXCEPTIONS=0')


if cxx_parsers_cfg.config.xml_generator:
    generator_name = cxx_parsers_cfg.config.xml_generator
if cxx_parsers_cfg.config.xml_generator_path:
    generator_path = cxx_parsers_cfg.config.xml_generator_path
