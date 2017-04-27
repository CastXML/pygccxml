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
    xml_generator=generator_name,
    castxml_epic_version=1)

# The c++ file we want to parse
filename = "example.hpp"
filename = this_module_dir_path + "/" + filename

decls = parser.parse([filename], xml_generator_config)
global_namespace = declarations.get_global_namespace(decls)

a1 = global_namespace.variable("a1")
print(str(a1.decl_type), type(a1.decl_type))
# > 'A', <class 'pygccxml.declarations.cpptypes.declarated_t'>

print(declarations.is_elaborated(a1.decl_type))
# > False

a2 = global_namespace.variable("a2")
print(str(a2.decl_type), type(a2.decl_type))
# > 'class ::A', <class 'pygccxml.declarations.cpptypes.elaborated_t'>

print(declarations.is_elaborated(a2.decl_type))
# > True

base = declarations.remove_elaborated(a2.decl_type)
print(str(base), type(base))
# > 'A', <class 'pygccxml.declarations.cpptypes.declarated_t'>

# The same can be done with function arguments:
fun = global_namespace.free_function("function")
print(type(fun.arguments[0].decl_type), type(fun.arguments[1].decl_type))
# > <class 'pygccxml.declarations.cpptypes.declarated_t'>,
#   <class 'pygccxml.declarations.cpptypes.elaborated_t'>
