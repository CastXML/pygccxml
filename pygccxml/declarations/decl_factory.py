# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

"""
defines declarations factory class
"""

from calldef import member_function_t
from calldef import constructor_t
from calldef import destructor_t
from calldef import member_operator_t
from calldef import casting_operator_t
from calldef import free_function_t
from calldef import free_operator_t
from enumeration import enumeration_t
from namespace import namespace_t
from class_declaration import class_t
from class_declaration import class_declaration_t
from typedef import typedef_t
from variable import variable_t

class decl_factory_t(object):
    """
    declarations factory class
    """
    def __init__(self):
        object.__init__(self)
    
    def create_member_function( self, *arguments, **keywords ):
        return member_function_t(*arguments, **keywords)
        
    def create_constructor( self, *arguments, **keywords ):
        return constructor_t(*arguments, **keywords)
    
    def create_destructor( self, *arguments, **keywords ):
        return destructor_t(*arguments, **keywords)
    
    def create_member_operator( self, *arguments, **keywords ):
        return member_operator_t(*arguments, **keywords)
    
    def create_casting_operator( self, *arguments, **keywords ):
        return casting_operator_t(*arguments, **keywords)
    
    def create_free_function( self, *arguments, **keywords ):
        return free_function_t(*arguments, **keywords)
    
    def create_free_operator( self, *arguments, **keywords ):
        return free_operator_t(*arguments, **keywords)

    def create_class_declaration(self, *arguments, **keywords ):
        return class_declaration_t(*arguments, **keywords)
        
    def create_class( self, *arguments, **keywords ):
        return class_t(*arguments, **keywords)
        
    def create_enumeration( self, *arguments, **keywords ):
        return enumeration_t(*arguments, **keywords)
        
    def create_namespace( self, *arguments, **keywords ):
        return namespace_t(*arguments, **keywords)
        
    def create_typedef( self, *arguments, **keywords ):
        return typedef_t(*arguments, **keywords)
        
    def create_variable( self, *arguments, **keywords ):
        return variable_t(*arguments, **keywords)
