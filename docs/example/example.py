# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import os
import sys

#find out the file location within the sources tree
this_module_dir_path = os.path.abspath ( os.path.dirname( sys.modules[__name__].__file__) )
#find out gccxml location
gccxml_09_path = os.path.join( this_module_dir_path, '..', '..', '..', 'gccxml_bin', 'v09', sys.platform, 'bin' )
#add pygccxml package to Python path
sys.path.append( os.path.join( this_module_dir_path, '..', '..' ) )


from pygccxml import parser
from pygccxml import declarations

#configure GCC-XML parser
config = parser.config_t( gccxml_path=gccxml_09_path, compiler='msvc71' )

#parsing source file
decls = parser.parse( ['example.hpp'], config )
global_ns = declarations.get_global_namespace( decls )

#get object that describes unittests namespace
unittests = global_ns.namespace( 'unittests' )

print '"unittests" declarations: \n'
declarations.print_declarations( unittests )


#print all base and derived class names
for class_ in unittests.classes():
    print 'class "%s" hierarchy information:' % class_.name
    print '\tbase classes   : ', `[base.related_class.name for base in class_.bases]`
    print '\tderived classes: ', `[derive.related_class.name for derive in class_.derived]`
    print '\n'


#pygccxml has very powerfull query api:

#select multiple declarations
run_functions = unittests.member_functions( 'run' )
print 'the namespace contains %d "run" member functions' % len(run_functions)
print 'they are: '
for f in run_functions:
    print '\t' + declarations.full_name( f )


#select single declaration - all next statements will return same object
#vector< unittests::test_case* >

#you can select the class using "full" name
test_container_1 = global_ns.class_( '::unittests::test_suite' )
#you can define your own "match" criteria
test_container_2 = global_ns.class_( lambda decl: 'suite' in decl.name )

is_same_object = test_container_1 is test_container_2
print "Does all test_container_* refer to the same object? ", str(is_same_object)
