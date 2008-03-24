import ctypes
from . import enums
import ctypes.wintypes
from .. import config as msvc_cfg
from pygccxml import declarations

def guess_class_type( udt_kind ):
    if enums.UdtKind.UdtStruct == udt_kind:
        return declarations.CLASS_TYPES.STRUCT
    elif enums.UdtKind.UdtClass == udt_kind:
        return declarations.CLASS_TYPES.CLASS
    else:
        return declarations.CLASS_TYPES.UNION

def guess_access_type( access_type ):
    if enums.CV_access_e.CV_private == access_type:
        return declarations.ACCESS_TYPES.PRIVATE
    elif enums.CV_access_e.CV_protected == access_type:
        return declarations.ACCESS_TYPES.PROTECTED
    else:
        return declarations.ACCESS_TYPES.PUBLIC

class full_name_splitter_t( object ):
    def __init__( self, full_name ):
        self.__full_name = full_name
        self.__identifiers = self.__split_scope_identifiers()
        self.__scope_identifiers = None

    @property
    def name( self ):
        return self.__identifiers[-1]

    @property
    def scope_names( self ):
        if None is self.__scope_identifiers:
            self.__scope_identifiers = []# ['::']
            for i in range( len(self.__identifiers) - 1):
                self.__scope_identifiers.append( '::'.join( self.__identifiers[0:i+1] ) )
        return self.__scope_identifiers

    @property
    def identifiers( self ):
        return self.__identifiers

    def __split_scope_identifiers( self ):
        try:
            result = []
            tmp = self.__full_name.split( '::' )
            tmp.reverse()
            while tmp:
                token = tmp.pop()
                less_count = token.count( '<' )
                greater_count = token.count( '>' )
                if less_count != greater_count:
                    while less_count != greater_count and tmp:
                        next_token = tmp.pop()
                        token = token + '::' + next_token
                        less_count += next_token.count( '<' )
                        greater_count += next_token.count( '>' )
                result.append( token )
            return result
        except Exception, err:
            msg = 'Unable to split scope for identifiers. The full scope name is: "%s". Error: %s'
            msg = msg % ( self.__full_name, str(err) )
            raise RuntimeError( msg )

__name_splitters = {}
def get_name_splitter( full_name ):
    try:
        return __name_splitters[full_name]
    except KeyError:
        splitter = full_name_splitter_t( full_name )
        __name_splitters[full_name] = splitter
        return splitter


#__unDName definition was taken from:
#http://www.tech-archive.net/Archive/VC/microsoft.public.vc.language/2006-02/msg00754.html
msvcrxx = ctypes.CDLL( msvc_cfg.msvcr_path, mode=ctypes.RTLD_GLOBAL)

free_type = ctypes.CFUNCTYPE( None, ctypes.c_void_p ) #free type
malloc_type = ctypes.CFUNCTYPE( ctypes.c_void_p, ctypes.c_uint ) #malloc type


__unDName = msvcrxx.__unDName
__unDName.argtypes = [ ctypes.c_char_p #undecorated name
                       , ctypes.c_char_p #decorated name
                       , ctypes.c_int #sizeof undecorated name
                       , malloc_type
                       , free_type
                       , ctypes.c_ushort #flags
                     ]
__unDName.restype = ctypes.c_char_p


def undecorate_name( name, options=None ):
    if options is None:
        options = enums.UndecorateNameOptions.UNDNAME_NO_ECSU
    buffer_size = 1024 * 32
    undecorated_name = ctypes.create_string_buffer('\0' * buffer_size) #should be enouph for any symbol
    __unDName( undecorated_name
               , name
               , buffer_size
               , malloc_type( msvcrxx.malloc )
               , free_type( msvcrxx.free )
               , options )
    return undecorated_name.value


if '__main__' == __name__:
    name = "boost::detail::is_base_and_derived_impl2<engine_objects::universal_base_t,engine_objects::erroneous_transactions_file_configuration_t>::Host"
    fnsp = full_name_splitter_t( name )
    for x in fnsp.scope_names:
        print x

    fnsp = full_name_splitter_t( 'x' )
    for x in fnsp.scope_names:
        print x
