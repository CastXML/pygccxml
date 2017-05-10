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

# Find the location of the xml generator (castxml or gccxml)
generator_path, generator_name = utils.find_xml_generator()

# Configure the xml generator
xml_generator_config = parser.xml_generator_configuration_t(
    xml_generator_path=generator_path,
    xml_generator=generator_name)

# The c++ file we want to parse
filename = "example.hpp"
filename = this_module_dir_path + "/" + filename

# Parse the c++ file
decls = parser.parse([filename], xml_generator_config)

global_namespace = declarations.get_global_namespace(decls)

ns_namespace = global_namespace.namespace("ns")

int_type = declarations.cpptypes.int_t()
double_type = declarations.cpptypes.double_t()

for decl in ns_namespace.declarations:
    print(decl)

# This prints all the declarations in the namespace declaration tree:
# ns::a [variable]
# ns::b [variable]
# ns::c [variable]
# double ns::func2(double a) [free function]

# Let's search for specific declarations
for decl in ns_namespace.declarations:
    if decl.name == "b":
        print(decl)
    if isinstance(decl, declarations.free_function_t):
        print(decl)

# This prints:
# ns::b [variable]
# double ns::func2(double a) [free function]
