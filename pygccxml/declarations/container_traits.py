# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

"""
defines few algorithms, that deals with different properties of std containers
"""

#import typedef
import calldef
import cpptypes
#import variable
#import algorithm
import namespace 
#import templates
#import enumeration
import class_declaration
#from sets import Set as set
#import types as build_in_types
import type_traits

def is_defined_in_xxx( xxx, cls ):
    if not cls.parent:
        return False
    
    if not isinstance( cls.parent, namespace.namespace_t ):
        return False
    
    if xxx != cls.parent.name:
        return False

    xxx_ns = cls.parent
    if not xxx_ns.parent:
        return False
    
    if not isinstance( xxx_ns.parent, namespace.namespace_t ):
        return False
    
    if '::' != xxx_ns.parent.name:
        return False
    
    global_ns = xxx_ns.parent
    return None is global_ns.parent

class vector_traits:

    @staticmethod
    def declaration_or_none( type ):
        global is_defined_in_std
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
        
        if not cls.name.startswith( 'vector<' ):
            return 
        
        if not is_defined_in_xxx( 'std', cls ):
            return
        return cls

    @staticmethod
    def is_vector( type ):
        """
        Returns True if type represents instantiation of std class vector,
        otherwise False.
        """
        return not( None is vector_traits.declaration_or_none( type ) )

    
    @staticmethod
    def class_declaration( type ):
        """returns reference to the class declaration, """
        cls = vector_traits.declaration_or_none( type )
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
            if not value_type_str.startswith( '::' ):
                value_type_str = '::' + value_type_str
            found = cls.top_parent.decls( name=value_type_str
                                          , function=lambda decl: not isinstance( decl, calldef.calldef_t )
                                          ,  allow_empty=True )
            if not found:
                if cpptypes.FUNDAMENTAL_TYPES.has_key( value_type_str ):
                    return cpptypes.FUNDAMENTAL_TYPES[value_type_str]
            if len( found ) == 1:
                return found[0]
            else:
                raise RuntimeError( "Unable to find out vector value type. vector class is: %s" % cls.decl_string )

