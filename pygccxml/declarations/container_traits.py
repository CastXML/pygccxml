# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

"""
defines few algorithms, that deals with different properties of std containers
"""

import calldef
import cpptypes
import namespace 
import templates
import class_declaration
import type_traits
    
class container_traits_impl_t:
    def __init__( self, container_name, value_type_index ):
        self.name = container_name
        self.value_type_index = value_type_index

    def get_container_or_none( self, type ):
        """returns reference to the class declaration or None"""
        type = type_traits.remove_alias( type )
        type = type_traits.remove_cv( type )
        
        cls = None 
        if isinstance( type, cpptypes.declarated_t ):
            cls = type_traits.remove_alias( type.declaration )
        elif isinstance( type, class_declaration.class_t ):
            cls = type
        elif isinstance( type, class_declaration.class_declaration_t ):
            cls = type
        else:
            return
        
        if not cls.name.startswith( self.name + '<' ):
            return 
        
        if not type_traits.impl_details.is_defined_in_xxx( 'std', cls ):
            return
        return cls

    def is_my_case( self, type ):
        return bool( self.get_container_or_none( type ) )
    
    def class_declaration( self, type ):
        cls = self.get_container_or_none( type )
        if not cls:
            raise TypeError( 'Type "%s" is not instantiation of std::%s' % ( type.decl_string, self.name ) )
        return cls
    
    def value_type( self, type ):
        cls = self.class_declaration( type )
        if isinstance( cls, class_declaration.class_t ):
            value_type = cls.typedef( "value_type", recursive=False ).type
            return type_traits.remove_declarated( value_type )
        else:
            value_type_str = templates.args( cls.name )[self.value_type_index]
            ref = type_traits.impl_details.find_value_type( cls.top_parent, value_type_str )
            if None is ref:
                raise RuntimeError( "Unable to find out %s '%s' value type." 
                                    % ( self.name, cls.decl_string ) )
            return ref

def create_traits_class( container_name, value_type_index ):
    class xxx_traits:
        impl = container_traits_impl_t( container_name, value_type_index )

        @staticmethod
        def is_my_case( type ):
            return xxx_traits.impl.is_my_case( type )
        
        @staticmethod
        def class_declaration( type ):
            return xxx_traits.impl.class_declaration( type )
        
        @staticmethod
        def value_type( type ):
            return xxx_traits.impl.value_type( type )
    
    return xxx_traits

vector_traits = create_traits_class( 'vector', 0 )
list_traits = create_traits_class( 'list', 0 )
map_traits = create_traits_class( 'map', 1 )
multimap_traits = create_traits_class( 'multimap', 1 )
hash_map_traits = create_traits_class( 'hash_map', 1 )
hash_multimap_traits = create_traits_class( 'hash_multimap', 1 )