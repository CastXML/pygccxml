# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

"""
defines class, that describes C++ enum
"""

import declaration

class enumeration_t( declaration.declaration_t ):
    """
    describes C++ enum
    """
    def __init__( self, name='', parent=None, values=None ):
        declaration.declaration_t.__init__( self, name, parent )
        if not values:
            values = {}
        self._values = values # dict name(str) -> value(int)

    def __eq__(self, other):
        if not declaration.declaration_t.__eq__( self, other ):
            return False
        return self.values == other.values

    def _get__cmp__items( self ):
        return [self.values]

    def _get_values(self):
        return self._values
    def _set_values(self, values):
        self._values = values
    values = property( _get_values, _set_values
                       , doc="dictionary that contains mapping between name and value, { name(str) : value(int) }")

