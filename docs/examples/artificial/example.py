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

# We have just one declaration in ns, which is our Test class:
classTest = ns.declarations[0]
print(classTest.name, type(classTest))
# > 'Test', <class 'pygccxml.declarations.class_declaration.class_t'

# Loop over the two constructors:
for constructor in classTest.constructors():
    print(str(constructor), constructor.is_artificial)
# > ns::Test::Test() [constructor], False
# > ns::Test::Test(ns::Test const & arg0) [constructor], True
