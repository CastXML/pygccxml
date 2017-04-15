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

decls = parser.parse([filename], xml_generator_config)
global_namespace = declarations.get_global_namespace(decls)
ns = global_namespace.namespace("ns")

print(ns.declarations[0])
# > ns::B [struct]

print(ns.declarations[1])
# > ns::D [struct]

print(ns.declarations[2])
# > ns::T<ns::B::D, bool> [class declaration]

print(ns.declarations[3])
# > ns::T<ns::B::D, bool> ns::fun() [free function]

print(declarations.templates.is_instantiation(ns.declarations[2].name))
# > True

name, parameter_list = declarations.templates.split(ns.declarations[2].name)
print(name, parameter_list)
# > 'T', ['ns::B::D', 'bool']
