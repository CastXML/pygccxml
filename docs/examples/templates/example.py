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

class_t_decl = []
for d in ns.declarations:
    if isinstance(d, declarations.class_declaration_t):
        class_declaration_t = d
    if isinstance(d, declarations.class_t):
        class_t_decl.append(d)
    if isinstance(d, declarations.free_function_t):
        free_function_t_decl = d

print(class_t_decl[0])
# > ns::B [struct]

print(class_t_decl[1])
# > ns::D [struct]

print(class_declaration_t)
# > ns::T<ns::B::D, bool> [class declaration]

print(free_function_t_decl)
# > ns::T<ns::B::D, bool> ns::function() [free function]

print(declarations.templates.is_instantiation(class_declaration_t.name))
# > True

name, parameter_list = declarations.templates.split(class_declaration_t.name)
print(name, parameter_list)
# > 'T', ['ns::B::D', 'bool']
