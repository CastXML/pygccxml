# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

"""
defines class that will keep results of different calculations.
"""

class algorithms_cache_t( object ):
    def __init__( self ):
        object.__init__( self )
        self._enabled = True

    def disable( self ):
        self._enabled = False

    def enable( self ):
        self._enabled = True

    @property
    def enabled( self ):
        return self._enabled

class declaration_algs_cache_t( algorithms_cache_t ):
    def __init__( self ):
        algorithms_cache_t.__init__( self )
        self._full_name = None
        self._access_type = None
        self._demangled_name = None
        self._declaration_path = None

    def _get_full_name( self ):
        if self.enabled:
            return self._full_name
        return None
    def _set_full_name( self, fname ):
        self._full_name = fname
    full_name = property( _get_full_name, _set_full_name )

    def _get_access_type( self ):
        if self.enabled:
            return self._access_type
        return None
    def _set_access_type( self, access_type ):
        self._access_type = access_type
    access_type = property( _get_access_type, _set_access_type )

    def _get_demangled_name( self ):
        if self.enabled:
            return self._demangled_name
        return None
    def _set_demangled_name( self, demangled_name ):
        self._demangled_name = demangled_name
    demangled_name = property( _get_demangled_name, _set_demangled_name )

    def _get_declaration_path( self ):
        if self.enabled:
            return self._declaration_path
        return None
    def _set_declaration_path( self, declaration_path ):
        self._declaration_path = declaration_path
    declaration_path = property( _get_declaration_path, _set_declaration_path )

    def reset( self ):
        self.full_name = None
        self.access_type = None
        self.demangled_name = None
        self.declaration_path = None

    def reset_name_based( self ):
        self.full_name = None
        self.demangled_name = None
        self.declaration_path = None

    def reset_access_type( self ):
        self.access_type = None

#Introducing next cache to the type broke unit test. I should find out why.
#~ class type_algs_cache_t( algorithms_cache_t ):
    #~ def __init__( self ):
        #~ algorithms_cache_t.__init__( self )
        #~ self._remove_alias = None

    #~ def _get_remove_alias( self ):
        #~ if self.enabled:
            #~ return self._remove_alias
        #~ return None
    #~ def _set_remove_alias( self, remove_alias ):
        #~ self._remove_alias = remove_alias
    #~ remove_alias = property( _get_remove_alias, _set_remove_alias )

