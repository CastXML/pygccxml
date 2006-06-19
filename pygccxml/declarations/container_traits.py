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
import class_declaration
import type_traits

class impl_details:
    @staticmethod
    def get_container_or_none( type, container_name ):
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
        
        if not cls.name.startswith( container_name + '<' ):
            return 
        
        if not type_traits.impl_details.is_defined_in_xxx( 'std', cls ):
            return
        return cls
    
class vector_traits:
    CONTAINER_NAME = 'vector'
    
    @staticmethod
    def is_vector( type ):
        """
        Returns True if type represents instantiation of std class vector, otherwise False."""
        return not( None is impl_details.get_container_or_none( type, vector_traits.CONTAINER_NAME ) )
    
    @staticmethod
    def class_declaration( type ):
        """returns reference to the class declaration, """
        cls = impl_details.get_container_or_none( type, vector_traits.CONTAINER_NAME )
        if not cls:
            raise TypeError( 'Type "%s" is not instantiation of std::vector' % type.decl_string )
        return cls
    
    @staticmethod
    def value_type( type ):
        """returns reference to value_type of the vector"""
        cls = vector_traits.class_declaration( type )
        if isinstance( cls, class_declaration.class_t ):
            return type_traits.remove_declarated( cls.typedef( "value_type", recursive=False ).type )
        else:
            value_type_str = templates.args( cls.name )[0]
            ref = type_traits.impl_details.find_value_type( cls.top_parent, value_type_str )
            if None is ref:
                raise RuntimeError( "Unable to find out vector value type. vector class is: %s" % cls.decl_string )
            return ref

