# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

"""
defines few algorithms, that deals with different properties of std containers
"""

import types
import calldef
import cpptypes
import namespace
import templates
import type_traits
import class_declaration

def __remove_basic_string( cls_name ):
    strings = { 
          'std::string' : ( 'std::basic_string<char,std::char_traits<char>,std::allocator<char> >'
                            , 'std::basic_string<char, std::char_traits<char>, std::allocator<char> >' )
        , 'std::wstring' : ( 'std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> >'
                             , 'std::basic_string<wchar_t, std::char_traits<wchar_t>, std::allocator<wchar_t> >' ) }
    
    new_name = cls_name
    for short_name, long_names in strings.iteritems():
        for lname in long_names:
            new_name = new_name.replace( lname, short_name )
    return new_name

def __remove_defaults_recursive( cls_name ):    
    global find_container_traits
    if not cls_name.startswith( 'std::' ):
        return cls_name
    no_std_cls_name = cls_name[5:]    
    c_traits = find_container_traits( no_std_cls_name )
    if not c_traits:        
        return cls_name
    return 'std::' + c_traits.remove_defaults( no_std_cls_name )

def __remove_allocator( cls_name ):
    cls_name = __remove_basic_string( cls_name )
    # "vector<int,std::allocator<int> >" 
    c_name, c_args = templates.split( cls_name )
    #"vector", [ "int", "std::allocator<int>" ]
    if 2 != len( c_args ):
        return 
    a_name, a_args = templates.split( c_args[1] )
    if 'allocator' not in a_name:
        return 
    if 1 != len( a_args ):
        return 
    if c_args[0].strip() != a_args[0]:
        return 
    value_type = __remove_defaults_recursive( c_args[0] )
    return templates.join( c_name, [value_type] )

def __remove_container( cls_name, default_container_name='deque' ):
    cls_name = __remove_basic_string( cls_name )
    # "vector<int,std::allocator<int> >" 
    c_name, c_args = templates.split( cls_name )
    #"vector", [ "int", "std::allocator<int>" ]
    if 2 != len( c_args ):
        return 
    dc_no_defaults = __remove_defaults_recursive( c_args[1] )   
    if dc_no_defaults != templates.join( 'std::' + default_container_name, [c_args[0]] ):
        return    
    value_type = __remove_defaults_recursive( c_args[0] )
    return templates.join( c_name, [value_type] )    

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

    

def create_traits_class( container_name
                         , element_type_index
                         , element_type_typedef
                         , remove_defaults_=None ):
    """ creates concrete container traits class """

    class xxx_traits:
        """extract information from the container"""

        impl = container_traits_impl_t( container_name, element_type_index, element_type_typedef )
        
        @staticmethod
        def name():
            return xxx_traits.impl.name
        
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

        @staticmethod
        def remove_defaults( type_or_string ):            
            name = None           
            if not isinstance( type_or_string, types.StringTypes ):
                name = xxx_traits.class_declaration( type_or_string ).name
            else:
                name = type_or_string
            if not remove_defaults_:
                return name                
            no_defaults = remove_defaults_( name )
            if not no_defaults:
                return name
            else:
                return no_defaults
    return xxx_traits

list_traits = create_traits_class( 'list', 0, 'value_type', __remove_allocator )

deque_traits = create_traits_class( 'deque', 0, 'value_type', __remove_allocator )

queue_traits = create_traits_class( 'queue', 0, 'value_type', __remove_container )

priority_queue = create_traits_class( 'priority_queue', 0, 'value_type' )

vector_traits = create_traits_class( 'vector', 0, 'value_type', __remove_allocator )

stack_traits = create_traits_class( 'stack', 0, 'value_type', __remove_container )

map_traits = create_traits_class( 'map', 1, 'mapped_type' )
multimap_traits = create_traits_class( 'multimap', 1, 'mapped_type' )

hash_map_traits = create_traits_class( 'hash_map', 1, 'mapped_type' )
hash_multimap_traits = create_traits_class( 'hash_multimap', 1, 'mapped_type' )

set_traits = create_traits_class( 'set', 0, 'value_type' )
hash_set_traits = create_traits_class( 'hash_set', 0, 'value_type' )

multiset_traits = create_traits_class( 'multiset', 0, 'value_type' )
hash_multiset_traits = create_traits_class( 'hash_multiset', 0, 'value_type' )

container_traits = (
      list_traits
    , deque_traits
    , queue_traits
    , priority_queue
    , vector_traits
    , stack_traits
    , map_traits
    , multimap_traits
    , hash_map_traits
    , hash_multimap_traits 
    , set_traits
    , hash_set_traits 
    , multiset_traits
    , hash_multiset_traits )
    
def find_container_traits( cls_or_string ):
    if isinstance( cls_or_string, types.StringTypes ):
        if not templates.is_instantiation( cls_or_string ):
            return None        
        name = templates.name( cls_or_string )
        for cls_traits in container_traits:        
            if cls_traits.name() == name:
                return cls_traits       
    else:
        for cls_traits in container_traits:        
            if cls_traits.is_my_case( cls ):
                return cls_traits


