# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import os
import sys
import autoconfig
from pygccxml import *

class printer_t( declarations.decl_visitor_t ):
    JUSTIFY = 20
    INTEND_SIZE = 4
    
    def __init__( self, level=0 ):
        declarations.decl_visitor_t.__init__(self)
        self.__inst = None
        self.__level = level

    def _get_level(self):
        return self.__level
    level = property( _get_level )
    
    def _get_inst(self):
        return self.__inst
    def _set_inst(self, inst):
        self.__inst = inst
    instance = property( _get_inst, _set_inst )
    
    def __nice_decl_name( self, inst ):
        name = inst.__class__.__name__
        if name.endswith( '_t' ):
            name = name[:-len('_t')]
        return name.replace( '_', ' ' )

    def __print_decl_header(self):
        header = self.__nice_decl_name( self.__inst ) + ": '%s'" % self.__inst.name 
        print ' ' * self.level * self.INTEND_SIZE + header.ljust( self.JUSTIFY )
        curr_level = self.level + 1 
        if self.__inst.location:
            location = 'location: '
            print ' ' * curr_level * self.INTEND_SIZE + location.ljust( self.JUSTIFY )
            curr_level += 1
            file = 'file: ' + "'%s'" % self.__inst.location.file_name
            print ' ' * curr_level * self.INTEND_SIZE + file.ljust( self.JUSTIFY )
            line = 'line: ' + "'%s'" % self.__inst.location.line
            print ' ' * curr_level * self.INTEND_SIZE + line.ljust( self.JUSTIFY )
        curr_level = self.level + 1
        artificial = 'artificial: ' + "'%s'" % str(self.__inst.is_artificial)      
        print ' ' * curr_level * self.INTEND_SIZE + artificial.ljust( self.JUSTIFY )

    def visit_member_function( self ):
        self.__print_decl_header()

    def visit_constructor( self ):
        self.__print_decl_header()

    def visit_destructor( self ):
        self.__print_decl_header()        

    def visit_member_operator( self ):
        self.__print_decl_header()        

    def visit_casting_operator( self ):
        self.__print_decl_header()        

    def visit_free_function( self ):
        self.__print_decl_header()

    def visit_free_operator( self ):
        self.__print_decl_header()

    def visit_class_declaration(self ):
        self.__print_decl_header()

    def visit_class(self ):
        self.__print_decl_header()
        curr_level = self.level + 1
        class_type = 'class type: ' + "'%s'" % str(self.__inst.class_type)        
        print ' ' * curr_level * self.INTEND_SIZE + class_type.ljust( self.JUSTIFY )
        
        def print_hierarchy(hierarchy_type, classes, curr_level):
            print ' ' * curr_level * self.INTEND_SIZE + hierarchy_type.ljust( self.JUSTIFY )
            curr_level += 1
            for class_ in classes:
                class_str = 'class: ' + "'%s'" % str(class_.related_class.decl_string)        
                print ' ' * curr_level * self.INTEND_SIZE + class_str.ljust( self.JUSTIFY )
                access = 'access: ' + "'%s'" % str(class_.access) 
                print ' ' * (curr_level + 1)* self.INTEND_SIZE + access.ljust( self.JUSTIFY )
        
        if self.__inst.bases:
            print_hierarchy( 'base classes: ', self.__inst.bases, curr_level )
            
        if self.__inst.derived:
            print_hierarchy( 'derived classes: ', self.__inst.derived, curr_level )

        def print_members(members_type, members, curr_level):
            print ' ' * curr_level * self.INTEND_SIZE + members_type.ljust( self.JUSTIFY )
            curr_level += 1
            for member in members:
                prn = printer_t( curr_level + 1 )
                prn.instance = member
                declarations.apply_visitor( prn, member )
                
        print_members( 'public: ', self.__inst.public_members, curr_level )
        print_members( 'protected: ', self.__inst.protected_members, curr_level )
        print_members( 'private: ', self.__inst.private_members, curr_level )
        
    def visit_enumeration(self):
        self.__print_decl_header()
        curr_level = self.level + 1
        print ' ' * curr_level * self.INTEND_SIZE + 'values: '.ljust( self.JUSTIFY )
        curr_level += 1
        for name, value in self.__inst.values.items():
            print ' ' * curr_level * self.INTEND_SIZE, name, ':', value

    def visit_namespace(self ):
        self.__print_decl_header()
        for decl in self.__inst.declarations:
            prn = printer_t( self.level + 1 )
            prn.instance = decl
            declarations.apply_visitor( prn, decl )
            
    def visit_typedef(self ):
        self.__print_decl_header()
        curr_level = self.level + 1
        print ' ' * curr_level * self.INTEND_SIZE + 'alias to: ', self.__inst.type.decl_string

    def visit_variable(self ):
        self.__print_decl_header()
        curr_level = self.level + 1
        print ' ' * curr_level * self.INTEND_SIZE, 'type: ', self.__inst.type.decl_string
        print ' ' * curr_level * self.INTEND_SIZE, 'value: ', self.__inst.value
    
if __name__ == "__main__":
    include_std_header = os.path.join( autoconfig.data_directory, 'include_std.hpp' )
    include_std_header = os.path.join( autoconfig.data_directory, 'include_all.hpp' )
    decls = parser.parse( [include_std_header] )
    prn = printer_t()
    for decl in decls:
        prn.instance = decl
        declarations.apply_visitor( prn, decl )

