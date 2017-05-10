# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import os
import sys

# Find out the file location within the sources tree
this_module_dir_path = os.path.abspath(
    os.path.dirname(sys.modules[__name__].__file__))
# Add pygccxml package to Python path
sys.path.append(os.path.join(this_module_dir_path, '..', '..'))


from pygccxml import parser  # nopep8
from pygccxml import declarations  # nopep8
from pygccxml import utils  # nopep8

# Find out the xml generator (gccxml or castxml)
generator_path, generator_name = utils.find_xml_generator()

# Configure the xml generator
config = parser.xml_generator_configuration_t(
    xml_generator_path=generator_path,
    xml_generator=generator_name,
    compiler="gcc")

# Parsing source file
decls = parser.parse([this_module_dir_path + '/example.hpp'], config)
global_ns = declarations.get_global_namespace(decls)

# Get object that describes unittests namespace
unittests = global_ns.namespace('unittests')

print('"unittests" declarations: \n')
declarations.print_declarations(unittests)

# Print all base and derived class names
for class_ in unittests.classes():
    print('class "%s" hierarchy information:' % class_.name)
    print('\tbase classes   : ', repr([
        base.related_class.name for base in class_.bases]))
    print('\tderived classes: ', repr([
        derive.related_class.name for derive in class_.derived]))
    print('\n')

# Pygccxml has very powerfull query api:

# Select multiple declarations
run_functions = unittests.member_functions('run')
print('the namespace contains %d "run" member functions' % len(run_functions))
print('they are: ')
for f in run_functions:
    print('\t' + declarations.full_name(f))

# Select single declaration - all next statements will return same object
# vector< unittests::test_case* >

# You can select the class using "full" name
test_container_1 = global_ns.class_('::unittests::test_suite')
# You can define your own "match" criteria
test_container_2 = global_ns.class_(lambda decl: 'suite' in decl.name)

is_same_object = test_container_1 is test_container_2
print(
    "Does all test_container_* refer to the same object? " +
    str(is_same_object))
