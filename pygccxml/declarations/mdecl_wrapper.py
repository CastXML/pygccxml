# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

class call_redirector_t( object ):
    """Internal class used to call some function of objects"""
    def __init__( self, name, decls ):
        object.__init__( self )
        self.name = name
        self.decls = decls
            
    def __call__( self, *arguments, **keywords ):
        for d in self.decls:
            callable_ = getattr(d, self.name)
            callable_( *arguments, **keywords )

class mdecl_wrapper_t( object ):
    """Multiple declarations wrapper. 
    
    The main purpose of this class is to allow an user to work on many 
    declarations, as they were only one single declaration. 
    
    Example: 
    mb = module_builder_t( ... )
    #lets say we want to exclude all member functions, that returns reference to int:
    mb.member_functions( return_type='int &' ).exclude()
    
    "exclude" function will be called on every function that match the criteria.
    """
    
    def __init__( self, decls ):
        """@param decls: list of declarations to operate on.
        @type decls: list of L{declaration wrappers<decl_wrapper_t>}
        """
        object.__init__( self )
        self.__dict__['_decls'] = decls

    def __len__( self ):
        """returns the number of declarations"""
        return len( self._decls )
    
    def __getitem__( self, index ):
        """provides access to declaration"""
        return self._decls[index]
    
    def __ensure_attribute( self, name ):
        invalid_decls = filter( lambda d: not hasattr( d, name ), self._decls )
        if invalid_decls:
            raise RuntimeError( "Not all declarations have '%s' attribute." % name )
        
    def __setattr__( self, name, value ):
        """Updates the value of attribute on all declarations.
        @param name: name of attribute
        @param value: new value of attribute
        """
        self.__ensure_attribute( name )
        for d in self._decls:
            setattr( d, name, value )
            
    def __getattr__( self, name ):
        """@param name: name of method
        """
        return call_redirector_t( name, self._decls )