# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

"""
"""

class dependency_info_t( object ):
    def __init__( self, declaration, depend_on_it, access_type=None ):
        object.__init__( self )
        self._declaration = declaration
        self._depend_on_it = depend_on_it
        self._access_type = access_type
        
    @property
    def declaration( self ):
        return self._declaration
    #short name
    decl = declaration

    @property 
    def depend_on_it( self ):
        return self._depend_on_it
    
    def _get_access_type( self ):
        return self._access_type
    def _set_access_type( self, access_type ):
        self._access_type = access_type   
    access_type = property( _get_access_type, _set_access_type )

    def __str__( self ):
        return 'declaration "%s" depends( %s ) on "%s" ' \
               % ( self.declaration, self.access_type, self.depend_on_it )
