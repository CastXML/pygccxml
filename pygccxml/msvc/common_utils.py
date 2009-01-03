# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import os
import re
import sys
import ctypes
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
    def __init__( self ):
        import ctypes.wintypes
        self.__undname = ctypes.windll.dbghelp.UnDecorateSymbolName
        self.__undname.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint, ctypes.c_uint]
        self.__clean_ecsu = re.compile( r'(?:(^|\W))(?:(class|enum|struct|union))' )
        self.__fundamental_types = (
              ( 'short unsigned int', 'unsigned short')
            , ( 'short int', 'short' )
            , ( 'long int', 'long' )
            , ( 'long unsigned int', 'unsigned long' )
        )
        self.__calling_conventions = re.compile( r'(?:(^|\s))(?:__(cdecl|clrcall|stdcall|fastcall|thiscall)\s)' )

    def normalize_undecorated( self, undname, options=None ):
        if options is None:
            options = UNDECORATE_NAME_OPTIONS.SHORT_UNIQUE_NAME
        if UNDECORATE_NAME_OPTIONS.UNDNAME_NO_ECSU & options:
            undname = self.__clean_ecsu.sub( '', undname )
        if UNDECORATE_NAME_OPTIONS.UNDNAME_NO_ACCESS_SPECIFIERS & options:
            for prefix in ( 'public: ', 'private: ', 'protected: ' ):
                if undname.startswith( prefix ):
                    undname = undname[ len(prefix): ]
                    break
        if UNDECORATE_NAME_OPTIONS.UNDNAME_NO_MS_KEYWORDS & options:
            undname = self.__calling_conventions.sub( ' ', undname)
        return undname.strip()

    def undecorate_blob( self, name, options=None ):
        if options is None:
            options = UNDECORATE_NAME_OPTIONS.SHORT_UNIQUE_NAME
        buffer = ctypes.create_string_buffer(1024*16)
        res = self.__undname( str(name), buffer, ctypes.sizeof(buffer), options)
        if res:
            return self.normalize_undecorated_blob( str(buffer[:res]) )
        else:
            return name

    def __remove_leading_scope( self, s ):
        if s and s.startswith( '::' ):
            return s[2:]
        else:
            return s

    def __format_type_as_undecorated( self, type_, is_argument ):
        result = []
        type_ = declarations.remove_alias( type_ )
        if declarations.is_array( type_ ):
            result.append( declarations.array_item_type( type_ ).decl_string )
            result.append( '*' )
            if is_argument:
                result.append( 'const' )
        else:
            result.append( self.__remove_leading_scope( type_.decl_string ) )
        return ' '.join( result )

    def __normalize( self, name ):
        for what, with_ in self.__fundamental_types:
            name = name.replace( what, with_ )
        name = name.replace( ', ', ',' )
        return name

    def undecorate_argtypes( self, argtypes ):
        if not argtypes:
            return 'void'
        else:
            formater = lambda type_: self.__format_type_as_undecorated( type_, True )
            return ','.join( map( formater, argtypes ) )

    def __undecorated_calldef( self, calldef ):
        calldef_type = calldef.function_type()

        result = []
        is_mem_fun = isinstance( calldef, declarations.member_calldef_t )
        if is_mem_fun and calldef.virtuality != declarations.VIRTUALITY_TYPES.NOT_VIRTUAL:
            result.append( 'virtual ' )
        if is_mem_fun and calldef.has_static:
            result.append( 'static ' )
        if calldef_type.return_type:
            result.append( self.__format_type_as_undecorated( calldef.return_type, False ) )
            result.append( ' ' )
        if is_mem_fun:
            result.append( self.__remove_leading_scope( calldef.parent.decl_string ) + '::')

        result.append( calldef.name )
        if isinstance( calldef, ( declarations.constructor_t, declarations.destructor_t) ) \
           and declarations.templates.is_instantiation( calldef.parent.name ):
            result.append( '<%s>' % ','.join( declarations.templates.args( calldef.parent.name ) ) )

        result.append( '(%s)' % self.undecorate_argtypes( calldef_type.arguments_types ) )
        if is_mem_fun and calldef.has_const:
            result.append( 'const' )
        return ''.join( result )

    def __undecorated_variable( self, decl ):
        result = []
        is_mem_var = isinstance( decl.parent, declarations.class_t )
        if is_mem_var and decl.type_qualifiers.has_static:
            result.append( 'static ' )
        result.append( self.__format_type_as_undecorated( decl.type, False ) )
        result.append( ' ' )
        if is_mem_var:
            result.append( self.__remove_leading_scope( decl.parent.decl_string ) + '::' )
        result.append( decl.name )
        return ''.join( result )

    def undecorated_decl(self, decl):
        """returns string, which contains full function name formatted exactly as
        result of dbghelp.UnDecorateSymbolName, with UNDNAME_NO_MS_KEYWORDS | UNDNAME_NO_ACCESS_SPECIFIERS | UNDNAME_NO_ECSU
        options.
        """
        name = None
        if isinstance( decl, declarations.calldef_t ):
            name = self.__undecorated_calldef( decl )
        elif isinstance( decl, declarations.variable_t ):
            name = self.__undecorated_variable( decl )
        else:
            raise NotImplementedError()
        return self.__normalize( name )

if 'win' in sys.platform:
    undecorate_blob = undname_creator().undecorate_blob
    undecorate_decl = undname_creator().undecorated_decl
    undecorate_argtypes = undname_creator().undecorate_argtypes
    normalize_undecorated = undname_creator().normalize_undecorated
else:
    def undecorate_blob( x ):
        raise NotImplementedError()
    def undecorate_decl( x ):
        raise NotImplementedError()
    def undecorate_argtypes( x ):
        raise NotImplementedError()
    def normalize_undecorated( *args ):
        raise NotImplementedError()

import exceptions
class LicenseWarning( exceptions.UserWarning ):
    def __init__( self, *args, **keywd ):
        exceptions.UserWarning.__init__( self, *args, **keywd )

class exported_symbols:
    map_file_re_c = re.compile( r' +\d+    (?P<internall>.+?)(?:\s+exported name\:\s(?P<name>.*)$)')
    map_file_re_cpp = re.compile( r' +\d+    (?P<decorated>.+?) \((?P<undecorated>.+)\)$' )

    @staticmethod
    def load_from_map_file( fname ):
        """returns dictionary { decorated symbol : orignal declaration name }"""
        result = {}
        f = open( fname )
        lines = []
        was_exports = False
        for line in f:
            if was_exports:
                lines.append( line )
            elif 'Exports' == line.strip():
                was_exports = True
            else:
                pass
        index = 0

        while index < len( lines ):
            line = lines[index].rstrip()
            found = exported_symbols.map_file_re_cpp.match( line )
            if found:
                result[ found.group( 'decorated' ) ] = normalize_undecorated( found.group( 'undecorated' ) )
            elif index + 1 < len( lines ):
                two_lines = line + lines[index+1].rstrip()
                found = exported_symbols.map_file_re_c.match( two_lines )
                if found:
                    result[ found.group( 'name' ) ] = found.group( 'name' )
                    index += 1
            else:
                pass
            index += 1
        return result

    @staticmethod
    def load_from_dll_file( fname ):
        import warnings
        warnings.warn( '\n'*2 + '-' * 30 + '>>LICENSE WARNING<<' + '-'*30
                         + '\n"load_from_dll_file" functionality uses code licensed under MIT license.'
                         + '\npygccxml project uses Boost Software License, Version 1.0. '
                         + '\nFor more information about this functionality take a look on get_dll_exported_symbols.py file.'
                         + '\n' + '='*79
                         + '\n' * 2
                       , LicenseWarning )
        import get_dll_exported_symbols
        result = {}
        blobs = get_dll_exported_symbols.read_export_table( fname )
        for blob in blobs:
            result[ blob ] = undecorate_blob( blob )
        return result

    @staticmethod
    def load_from_file( fname ):
        ext = os.path.splitext( fname )[1]
        if '.dll' == ext:
            return exported_symbols.load_from_dll_file( fname )
        elif '.map' == ext:
            return exported_symbols.load_from_map_file( fname )
        else:
            raise RuntimeError( "Don't know how to read exported symbols from file '%s'"
                                % fname )

    @staticmethod
    def is_c_function( decl, blob ):
        return decl.name == blob
