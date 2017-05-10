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

# Search for the function by name
criteria = declarations.calldef_matcher(name="func1")
func1 = declarations.matcher.get_single(criteria, ns_namespace)

# Search for functions which return an int
criteria = declarations.calldef_matcher(return_type="int")
func2 = declarations.matcher.get_single(criteria, ns_namespace)

# Search for functions which return an int, using the cpptypes class
criteria = declarations.calldef_matcher(return_type=int_type)
func3 = declarations.matcher.get_single(criteria, ns_namespace)

print(func1)
print(func2)
print(func3)

# This prints:
# int ns::func1(int a) [free function]
# int ns::func1(int a) [free function]
# int ns::func1(int a) [free function]

# Search for functions which return a double. Two functions will be found
criteria = declarations.calldef_matcher(return_type=double_type)
func4 = declarations.matcher.find(criteria, ns_namespace)

print(len(func4))
print(func4[0])
print(func4[1])

# This prints:
# 2
# double ns::func2(double a) [free function]
# double ns::func3(double a) [free function]

# Finally, look for variables by name and by type
criteria = declarations.variable_matcher(name="a")
var_a1 = declarations.matcher.find(criteria, ns_namespace)

criteria = declarations.variable_matcher(decl_type=int_type)
var_a2 = declarations.matcher.find(criteria, ns_namespace)

print(var_a1[0])
print(var_a2[0])
print(var_a2[1])

# This prints:
# ns::a [variable]
# ns::a [variable]
# ns::b [variable]
