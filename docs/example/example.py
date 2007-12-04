# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import sys
#~ sys.path.append('../..') #adding pygccxml to the path

from pygccxml import parser
from pygccxml import declarations

#configure GCC-XML parser
config = parser.config_t( gccxml_path='/home/roman/language-binding/sources/gccxml_bin/v09/linux2/bin' )

#parsing source file
decls = parser.parse( ['example.hpp'], config )
global_ns = declarations.get_global_namespace( decls )

#printing all declarations found in file and its includes
declarations.print_declarations( global_ns )

#print all base and derived class names
for class_ in global_ns.classes():
    print class_.name
    print '\tbases: ', `[base.related_class.name for base in class_.bases]`
    print '\tderived: ', `[derive.related_class.name for derive in class_.derived]`
