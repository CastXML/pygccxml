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

function_ptr = global_namespace.variables()[0]

# Print the name of the function pointer
print(function_ptr.name)
# > myFuncPointer

# Print the type of the declaration
print(function_ptr.decl_type)
# > void (*)( int,double )

# Print the real type of the declaration (it's just a pointer)
print(type(function_ptr.decl_type))
# > <class 'pygccxml.declarations.cpptypes.pointer_t'>

# Check if this is a function pointer
print(declarations.is_calldef_pointer(function_ptr.decl_type))
# > True

# Remove the pointer part, to access the function's type
f_type = declarations.remove_pointer(function_ptr.decl_type)

# Print the type
print(type(f_type))
# > <class 'pygccxml.declarations.cpptypes.free_function_type_t'>

# Print the return type and the arguments of the function
print(f_type.return_type)
# > void

# Print the return type and the arguments
print(str(f_type.arguments_types[0]), str(f_type.arguments_types[1]))
# > int, double
