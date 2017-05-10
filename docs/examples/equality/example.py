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

# Search for the function called func1
criteria = declarations.calldef_matcher(name="func1")
func1a = declarations.matcher.get_single(criteria, ns_namespace)

# Search for the function called func2
criteria = declarations.calldef_matcher(name="func2")
func2a = declarations.matcher.get_single(criteria, ns_namespace)

# You can also write a loop on the declaration tree
func1b = None
for decl in ns_namespace.declarations:
    if decl.name == "func1":
        func1b = decl

# The declarations can be compared (prints (True, False))
print(func1a == func1b, func1a == func2a)
