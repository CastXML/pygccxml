# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

from pygccxml import parser
from pygccxml import declarations

#configure GCC-XML parser
config = parser.config_t( gccxml_path=r'/home/roman/gccxml/bin/gccxml' )
#parsing source file
global_ns = parser.parse( ['core_class_hierarchy.hpp'], config )
#printing all declarations found in file and its includes
declarations.print_declarations( global_ns )
#selecting all classes
all_decls = declarations.make_flatten( global_ns )
all_classes = filter( lambda decl: isinstance( decl, declarations.class_t )
                      , all_decls )
#print all base and derived class names
for class_ in all_classes:
    print class_.name
    print '\tbases: ', `[base.related_class.name for base in class_.bases]`
    print '\tderived: ', `[derive.related_class.name for derive in class_.derived]`
