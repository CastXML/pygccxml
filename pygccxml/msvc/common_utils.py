# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import re
import ctypes
import ctypes.wintypes
from .. import declarations

class UNDECORATE_NAME_OPTIONS:
    UNDNAME_COMPLETE = 0x0000 #Enables full undecoration.
    UNDNAME_NO_LEADING_UNDERSCORES = 0x0001 #Removes leading underscores from Microsoft extended keywords.
    UNDNAME_NO_MS_KEYWORDS = 0x0002 #Disables expansion of Microsoft extended keywords.
    UNDNAME_NO_FUNCTION_RETURNS = 0x0004 #Disables expansion of return type for primary declaration.
    UNDNAME_NO_ALLOCATION_MODEL = 0x0008 #Disables expansion of the declaration model.
    UNDNAME_NO_ALLOCATION_LANGUAGE = 0x0010 #Disables expansion of the declaration language specifier.
    UNDNAME_RESERVED1 = 0x0020 #RESERVED.
    UNDNAME_RESERVED2 = 0x0040 #RESERVED.
    UNDNAME_NO_THISTYPE = 0x0060 #Disables all modifiers on the this type.
    UNDNAME_NO_ACCESS_SPECIFIERS = 0x0080 #Disables expansion of access specifiers for members.
    UNDNAME_NO_THROW_SIGNATURES = 0x0100 #Disables expansion of "throw-signatures" for functions and pointers to functions.
    UNDNAME_NO_MEMBER_TYPE = 0x0200 #Disables expansion of static or virtual members.
    UNDNAME_NO_RETURN_UDT_MODEL = 0x0400 #Disables expansion of the Microsoft model for UDT returns.
    UNDNAME_32_BIT_DECODE = 0x0800 #Undecorates 32-bit decorated names.
    UNDNAME_NAME_ONLY = 0x1000 #Gets only the name for primary declaration; returns just [scope::]name. Expands template params.
    UNDNAME_TYPE_ONLY = 0x2000 #Input is just a type encoding; composes an abstract declarator.
    UNDNAME_HAVE_PARAMETERS = 0x4000 #The real template parameters are available.
    UNDNAME_NO_ECSU = 0x8000 #Suppresses enum/class/struct/union.
    UNDNAME_NO_IDENT_CHAR_CHECK = 0x10000 #Suppresses check for valid identifier characters.
    UNDNAME_NO_PTR64 = 0x20000 #Does not include ptr64 in output.

    UNDNAME_SCOPES_ONLY = UNDNAME_NO_LEADING_UNDERSCORES \
                          | UNDNAME_NO_MS_KEYWORDS \
                          | UNDNAME_NO_FUNCTION_RETURNS \
                          | UNDNAME_NO_ALLOCATION_MODEL \
                          | UNDNAME_NO_ALLOCATION_LANGUAGE \
                          | UNDNAME_NO_ACCESS_SPECIFIERS \
                          | UNDNAME_NO_THROW_SIGNATURES \
                          | UNDNAME_NO_MEMBER_TYPE \
                          | UNDNAME_NO_ECSU \
                          | UNDNAME_NO_IDENT_CHAR_CHECK

    SHORT_UNIQUE_NAME = UNDNAME_NO_MS_KEYWORDS | UNDNAME_NO_ACCESS_SPECIFIERS | UNDNAME_NO_ECSU

#~ The following code doesn't work - access violation

#~__unDName definition was taken from:
#~http://www.tech-archive.net/Archive/VC/microsoft.public.vc.language/2006-02/msg00754.html

#~ msvcrxx = ctypes.windll.msvcr90
#~ free_type = ctypes.CFUNCTYPE( None, ctypes.c_void_p ) #free type
#~ malloc_type = ctypes.CFUNCTYPE( ctypes.c_void_p, ctypes.c_uint ) #malloc type
#~ __unDName = msvcrxx.__unDName
#~ __unDName.argtypes = [ ctypes.c_char_p #undecorated name
                       #~ , ctypes.c_char_p #decorated name
                       #~ , ctypes.c_int #sizeof undecorated name
                       #~ , malloc_type
                       #~ , free_type
                       #~ , ctypes.c_ushort #flags
                     #~ ]
#~ __unDName.restype = ctypes.c_char_p
#~ def undecorate_name( name, options=None ):
    #~ if not name:
        #~ return ''
    #~ if options is None:
        #~ options = UNDECORATE_NAME_OPTIONS.SHORT_UNIQUE_NAME
    #~ buffer_size = 1024 * 32
    #~ undecorated_name = ctypes.create_string_buffer('\0' * buffer_size) #should be enouph for any symbol
    #~ __unDName( undecorated_name
               #~ , str(name)
               #~ , buffer_size
               #~ , malloc_type( msvcrxx.malloc )
               #~ , free_type( msvcrxx.free )
               #~ , options )
    #~ return undecorated_name.value

class undname_creator:
    __undname = ctypes.windll.dbghelp.UnDecorateSymbolName
    __undname.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint, ctypes.c_uint]
    __clean_ecsu = re.compile( r'(?:(^|\W))(?:(class|enum|struct|union))' )

    def undecorate_blob( self, name, options=None ):
        if options is None:
            options = UNDECORATE_NAME_OPTIONS.SHORT_UNIQUE_NAME
        buffer = ctypes.create_string_buffer(1024*16)
        res = self.__undname( str(name), buffer, ctypes.sizeof(buffer), options)
        if res:
            undname = str(buffer[:res])
            if UNDECORATE_NAME_OPTIONS.UNDNAME_NO_ECSU & options:
                undname = self.__clean_ecsu.sub( '', undname )
            return undname.strip()
        else:
            return name

    def __remove_leading_scope( self, s ):
        if s and s.startswith( '::' ):
            return s[2:]
        else:
            return s

    def __format_type_as_undecorated( self, type_ ):
        result = []
        type_ = declarations.remove_alias( type_ )
        result.append( self.__remove_leading_scope( type_.decl_string ) )
        return ' '.join( result )

    def __format_args_as_undecorated( self, argtypes ):
        if not argtypes:
            return 'void'
        else:
            return ','.join( map( self.__format_type_as_undecorated, argtypes ) )

    def undecorated_decl(self, calldef):
        """returns string, which contains full function name formatted exactly as
        result of dbghelp.UnDecorateSymbolName, with UNDNAME_NO_MS_KEYWORDS | UNDNAME_NO_ACCESS_SPECIFIERS | UNDNAME_NO_ECSU
        options.
        """
        calldef_type = calldef.function_type()

        result = []
        is_mem_fun = isinstance( calldef, declarations.member_calldef_t )
        if is_mem_fun and calldef.virtuality != declarations.VIRTUALITY_TYPES.NOT_VIRTUAL:
            result.append( 'virtual ' )
        if calldef_type.return_type:
            result.append( self.__format_type_as_undecorated( calldef.return_type ) )
            result.append( ' ' )
        if is_mem_fun:
            result.append( self.__remove_leading_scope( calldef.parent.decl_string ) + '::')

        result.append( calldef.name )
        if isinstance( calldef, ( declarations.constructor_t, declarations.destructor_t) ) \
           and declarations.templates.is_instantiation( calldef.parent.name ):
            result.append( '<%s>' % ','.join( declarations.templates.args( calldef.parent.name ) ) )

        result.append( '(%s)' % self.__format_args_as_undecorated( calldef_type.arguments_types ) )
        if is_mem_fun and calldef.has_const:
            result.append( 'const' )
        return ''.join( result )

undecorate_blob = undname_creator().undecorate_blob
undecorate_decl = undname_creator().undecorated_decl

class exported_symbols:
    map_file_re = re.compile( r' +\d+    (?P<decorated>.+) \((?P<undecorated>.+)\)$' )
    @staticmethod
    def load_from_map_file( fname ):
        """returns dictionary { decorated symbol : orignal declaration name }"""
        result = {}
        f = open( fname )
        exports_started = False
        for line in f:
            if not exports_started:
                exports_started = bool( 'Exports' == line.strip() )
            if not exports_started:
                continue
            line = line.rstrip()
            found = exported_symbols.map_file_re.match( line )
            if found:
                result[ found.group( 'decorated' ) ] = found.group( 'undecorated' )
        return result

#~ quick & dirty test
#~ symbols = exported_symbols.load_from_map_file( r'D:\dev\language-binding\sources\pygccxml_dev\unittests\data\msvc\Release\mydll.map' )
#~ for decorated, undecorated in symbols.iteritems():
    #~ print '---------------------------------------------------------------------'
    #~ print decorated
    #~ print undecorated
    #~ print undecorate_blob( decorated )
    #~ print '====================================================================='

