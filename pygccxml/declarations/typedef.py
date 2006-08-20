# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

"""
defines class that describes C++ typedef declaration
"""

import declaration

class typedef_t( declaration.declaration_t ):
    """describes C++ typedef declaration"""

    def __init__( self, name='', parent=None, type=None ):
        declaration.declaration_t.__init__( self, name, parent )
        self._type = type

    def _get__cmp__items( self ):
        return [self.type]

    def __eq__(self, other):
        if not declaration.declaration_t.__eq__( self, other ):
            return False
        return self.type == other.type

    def _get_type(self):
        return self._type
    def _set_type(self, type):
        self._type = type
    type = property( _get_type, _set_type
                     , doc="reference to the original L{type<type_t>}"    )
