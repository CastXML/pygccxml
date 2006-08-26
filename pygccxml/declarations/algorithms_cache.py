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
        self.full_name = None
        self.access_type = None
        self.declaration_path = None
    
    def reset( self ):
        self.full_name = None
        self.access_type = None
        self.declaration_path = None

    def reset_name_based( self ):
        self.full_name = None
        self.declaration_path = None
    
    def reset_access_type( self ):
        self.access_type = None
        
class type_traits_cache_t( object ):
    def __init__( self ):
        object.__init__( self )
        self.remove_alias = None
        
