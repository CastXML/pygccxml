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
    """this class implements the functionality needed for convinient work with
    STD container classes.

    Implemented functionality:
        - find out whether a declaration is STD container or not
        - find out container value( mapped ) type

    This class tries to be useful as much, as possible. For example, for class
    declaration( and not definition ) it parsers the class name in order to
    extract all the information.
    """
    def __init__( self, container_name, element_type_index, element_type_typedef ):
        """
        container_name - std container name
        element_type_index - position of value\\mapped type within template
          arguments list
        element_type_typedef - class typedef to the value\\mapped type
        """
        self.name = container_name
        self.element_type_index = element_type_index
        self.element_type_typedef = element_type_typedef

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
        """checks, whether type is STD container or not"""
        return bool( self.get_container_or_none( type ) )

    def class_declaration( self, type ):
        """returns reference to the class declaration"""
        cls = self.get_container_or_none( type )
        if not cls:
            raise TypeError( 'Type "%s" is not instantiation of std::%s' % ( type.decl_string, self.name ) )
        return cls

    def element_type( self, type ):
        """returns reference to the class value\\mapped type declaration"""
        cls = self.class_declaration( type )
        if isinstance( cls, class_declaration.class_t ):
            value_type = cls.typedef( self.element_type_typedef, recursive=False ).type
            return type_traits.remove_declarated( value_type )
        else:
            value_type_str = templates.args( cls.name )[self.element_type_index]
            ref = type_traits.impl_details.find_value_type( cls.top_parent, value_type_str )
            if None is ref:
                raise RuntimeError( "Unable to find out %s '%s' value type."
                                    % ( self.name, cls.decl_string ) )
            return ref


def create_traits_class( container_name, element_type_index, element_type_typedef ):
    """ creates concrete container traits class """

    class xxx_traits:
        """extract information from the container"""

        impl = container_traits_impl_t( container_name, element_type_index, element_type_typedef )

        @staticmethod
        def is_my_case( type ):
            """returns True if type is the container class, otherwise False"""
            return xxx_traits.impl.is_my_case( type )

        @staticmethod
        def class_declaration( type ):
            """returns reference to the container class"""
            return xxx_traits.impl.class_declaration( type )

        @staticmethod
        def element_type( type ):
            """returns reference to container name value\\mapped type class"""
            return xxx_traits.impl.element_type( type )

    return xxx_traits

list_traits = create_traits_class( 'list', 0, 'value_type' )

deque_traits = create_traits_class( 'deque', 0, 'value_type' )

queue_traits = create_traits_class( 'queue', 0, 'value_type' )

priority_queue = create_traits_class( 'priority_queue', 0, 'value_type' )

vector_traits = create_traits_class( 'vector', 0, 'value_type' )

stack_traits = create_traits_class( 'stack', 0, 'value_type' )

map_traits = create_traits_class( 'map', 1, 'mapped_type' )
multimap_traits = create_traits_class( 'multimap', 1, 'mapped_type' )

hash_map_traits = create_traits_class( 'hash_map', 1, 'mapped_type' )
hash_multimap_traits = create_traits_class( 'hash_multimap', 1, 'mapped_type' )

set_traits = create_traits_class( 'set', 0, 'value_type' )
hash_set_traits = create_traits_class( 'hash_set', 0, 'value_type' )

multiset_traits = create_traits_class( 'multiset', 0, 'value_type' )
hash_multiset_traits = create_traits_class( 'hash_multiset', 0, 'value_type' )




