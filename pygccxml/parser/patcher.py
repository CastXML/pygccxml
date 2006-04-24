# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

from pygccxml import declarations

class patcher_base_t(object):
    def __init__( self, decls ):
        object.__init__( self )
        self.__decls = decls   

    def _get_decls(self):
        return self.__decls
    decls = property( _get_decls )

    def patch_it(self):
        raise NotImplementedError()

class default_argument_patcher_t( patcher_base_t ):
    def __init__( self, decls ):
        patcher_base_t.__init__( self, decls )

    def patch_it(self):
        for decl in declarations.make_flatten( self.decls ):
            if not isinstance( decl, declarations.calldef_t ):
                continue
            for arg in decl.arguments:
                if not arg.default_value:
                    continue
                fixer = self.__find_fixer( decl, arg )
                if fixer:
                    arg.default_value = fixer( decl, arg )

    def __find_fixer(self, func, arg):
        if not arg.default_value:
            return False
        elif self.__is_unqualified_enum( func, arg ):
            return self.__fix_unqualified_enum
        elif self.__is_double_call( func, arg ):
            return self.__fix_double_call       
        elif self.__is_invalid_integral( func, arg ):
            return self.__fix_invalid_integral
        elif self.__is_constructor_call( func, arg ):
            return self.__fix_constructor_call
        else:
            return None

    def __join_names( self, prefix, suffix ):
        if prefix == '::':
            return '::' + suffix
        else:
            return prefix + '::' + suffix
  
    def __is_unqualified_enum(self, func, arg):
        type_ = declarations.remove_reference( declarations.remove_cv( arg.type ) )        
        if not declarations.is_enum( type_ ):
            return False
        return type_.declaration.values.has_key( arg.default_value )

    def __fix_unqualified_enum( self, func, arg):
        type_ = declarations.remove_reference( declarations.remove_cv( arg.type ) )
        enum_type = type_.declaration
        return self.__join_names( enum_type.parent.decl_string, arg.default_value )

    def __is_invalid_integral(self, func, arg):
        type_ = declarations.remove_reference( declarations.remove_cv( arg.type ) )        
        return declarations.is_integral( type_ )

    def __fix_invalid_integral(self, func, arg):
        try:
            int( arg.default_value )
            return arg.default_value
        except:
            pass
        
        try:
            int( arg.default_value, 16 )
            default_value = arg.default_value.lower()
            found_hex = filter( lambda ch: ch in 'abcdef', default_value )
            if found_hex and not default_value.startswith( '0x' ):
                int( '0x' + default_value, 16 )
                return '0x' + default_value
        except:
            pass
        
        #may be we deal with enum
        parent = func.parent
        while parent:
            found = self.__find_enum( parent, arg.default_value )
            if found:
                if declarations.is_fundamental( arg.type ) and ' ' in arg.type.decl_string:
                    template = '(%s)(%s)'
                else:
                    template = '%s(%s)'
                return template % ( arg.type.decl_string
                                    , self.__join_names( found.parent.decl_string, arg.default_value ) )
            else:
                parent = parent.parent
        return arg.default_value

    def __find_enum( self, scope, default_value ):
        #this algorithm could be improved: it could take into account
        #1. unnamed namespaced
        #2. location within files
        enums = filter( lambda decl: isinstance( decl, declarations.enumeration_t )
                        , scope.declarations )
        for enum_decl in enums:
            if default_value in enum_decl.values.keys():
                return enum_decl
            if default_value in enum_decl.values.values():
                return enum_decl
        else:
            return None

    def __is_double_call( self, func, arg ):
        call_invocation = declarations.call_invocation
        dv = arg.default_value
        found1 = call_invocation.find_args( dv )
        if found1 == call_invocation.NOT_FOUND:
            return False
        found2 = call_invocation.find_args( dv, found1[1] + 1 )
        if found2 == call_invocation.NOT_FOUND:
            return False
        args1 = call_invocation.args( dv[ found1[0] : found1[1] + 1 ] )
        args2 = call_invocation.args( dv[ found2[0] : found2[1] + 1 ] )
        return len(args1) == len(args2)
    
    def __fix_double_call( self, func, arg ):
        call_invocation = declarations.call_invocation
        dv = arg.default_value
        found1 = call_invocation.find_args( dv )
        found2 = call_invocation.find_args( dv, found1[1] + 1 )
        #args1 = call_invocation.args( dv[ found1[0] : found1[1] + 1 ] )
        args2 = call_invocation.args( dv[ found2[0] : found2[1] + 1 ] )
        return call_invocation.join( dv[:found1[0]], args2 )

    def __is_constructor_call( self, func, arg ):
        call_invocation = declarations.call_invocation
        dv = arg.default_value
        if not call_invocation.is_call_invocation( dv ):
            return False
        name = call_invocation.name( dv )
        base_type = declarations.base_type( arg.type )
        if not isinstance( base_type, declarations.declarated_t ):
            return False
        decl = base_type.declaration
        return decl.name == name \
               or ( isinstance( decl, declarations.class_t ) \
                    and name in map( lambda typedef: typedef.name, decl.typedefs ) )

    def __fix_constructor_call( self, func, arg ):
        call_invocation = declarations.call_invocation
        dv = arg.default_value
        if not call_invocation.is_call_invocation( dv ):
            return False
        base_type = declarations.base_type( arg.type )
        decl = base_type.declaration
        name, args = call_invocation.split( dv )
        if decl.name != name:
            #we have some alias to the class
            relevant_typedefs = filter( lambda typedef: typedef.name == name
                                        , decl.typedefs )
            if 1 == len( relevant_typedefs ):
                f_q_name = self.__join_names( declarations.full_name( relevant_typedefs[0].parent )
                                              , name )
            else:#in this case we can not say which typedef user uses:
                f_q_name = self.__join_names( declarations.full_name( decl.parent )
                                              , decl.name )
        else:
            f_q_name = self.__join_names( declarations.full_name( decl.parent ), name )
            
        return call_invocation.join( f_q_name, args )

def patch_it(decls):
    patcher = default_argument_patcher_t( decls )
    patcher.patch_it()
    return patcher.decls
    