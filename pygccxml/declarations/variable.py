# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import declaration 

class variable_t( declaration.declaration_t ):
    def __init__( self
                  , name=''
                  , parent=None
                  , type=None
                  , type_qualifiers=None
                  , value=None
                  , bits=None):
        declaration.declaration_t.__init__( self, name, parent )
        self._type = type
        self._type_qualifiers = type_qualifiers
        self._value = value
        self._bits = bits

    def _get__cmp__items( self ):
        return [ self.type, self.type_qualifiers, self.value ]
        
    def __eq__(self, other):
        if not declaration.declaration_t.__eq__( self, other ):
            return False
        return self.type == other.type \
               and self.type_qualifiers == other.type_qualifiers \
               and self.value == other.value \
               and self.bits == other.bits

    def _get_type(self):
        return self._type
    def _set_type(self, type):
        self._type = type
    type = property( _get_type, _set_type )

    def _get_type_qualifiers(self):
        return self._type_qualifiers
    def _set_type_qualifiers(self, type_qualifiers):
        self._type_qualifiers = type_qualifiers
    type_qualifiers = property( _get_type_qualifiers, _set_type_qualifiers )

    def _get_value(self):
        return self._value
    def _set_value(self, value):
        self._value = value
    value = property( _get_value, _set_value )

    def _get_bits(self):
        return self._bits
    def _set_bits(self, bits):
        self._bits = bits
    bits = property( _get_bits, _set_bits )
