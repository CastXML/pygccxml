# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

from pygccxml import utils
from pygccxml import declarations
from pygccxml import parser

import os
import sys
import warnings
warnings.simplefilter("error", Warning)
# Find out the file location within the sources tree
this_module_dir_path = os.path.abspath(
    os.path.dirname(sys.modules[__name__].__file__))

# Find out the c++ parser
generator_path, generator_name = utils.find_xml_generator()

# Configure the xml generator
xml_generator_config = parser.xml_generator_configuration_t(
    xml_generator_path=generator_path,
    xml_generator=generator_name)

# The c++ file we want to parse
filename = "example.hpp"
filename = this_module_dir_path + "/" + filename

file_config = parser.file_configuration_t(
    data=filename,
    content_type=parser.CONTENT_TYPE.CACHED_SOURCE_FILE)

project_reader = parser.project_reader_t(xml_generator_config)
decls = project_reader.read_files(
    [file_config],
    compilation_mode=parser.COMPILATION_MODE.FILE_BY_FILE)

global_namespace = declarations.get_global_namespace(decls)

value = global_namespace.namespace("ns")
print("My name is: " + value.name)
