import os
import sys
import comtypes
import comtypes.client
import _winreg as win_registry
from distutils import msvccompiler


class binaries_searcher_t:    
    
    def get_msbsc_path( self ):
        relative_path = os.path.dirname( sys.modules[__name__].__file__)
        absolute_path = os.path.abspath (relative_path)
        return os.path.join( absolute_path, 'msbsc70.dll' )
        
    def get_msvcr_path( self ):
        relative_path = os.path.dirname( sys.modules[__name__].__file__)
        absolute_path = os.path.abspath (relative_path)
        return os.path.join( absolute_path, 'msvcr70.dll' )
    
    def get_msdia_path( self ):
        vss_installed = self.__get_installed_vs_dirs()
        msdia_dlls = self.__get_msdia_dll_paths( vss_installed )
        if 1 == len(msdia_dlls):
            return msdia_dlls[0]
        else:
            #TODO find the highest version and use it.
            pass
    
    def __get_msdia_dll_paths( self, vss_installed ):
        msdia_dlls = []        
        for vs in vss_installed:
            debug_dir = os.path.join( vs, 'Common7', 'Packages', 'Debugger' )
            files = filter( lambda f: f.startswith( 'msdia' ) and f.endswith( '.dll' )
                            , os.listdir( debug_dir ) )
            if not files:
                continue
            msdia_dlls.extend([ os.path.join( debug_dir, f ) for f in files ])
        if not msdia_dlls:
            raise RuntimeError( 'pygccxml unable to find out msdiaXX.dll location' )
        return msdia_dlls
    
    def __get_installed_vs_dirs( self ):
        vs_reg_path = 'Software\Microsoft\VisualStudio\SxS\VS7'
        values = self.read_values( win_registry.HKEY_LOCAL_MACHINE, vs_reg_path )
        return [ values.values()[0] ]
    
    def read_keys(self, base, key):
        return msvccompiler.read_keys(base, key)

    def read_values(self, base, key):
        return msvccompiler.read_values(base, key)

bs = binaries_searcher_t()

msdia_path = bs.get_msdia_path()  
print 'msdia path: ', msdia_path

msbsc_path = bs.get_msbsc_path()  
print 'msbsc path: ', msbsc_path

msvcr_path = bs.get_msvcr_path()
print 'msvcr path: ', msvcr_path

comtypes_client_gen_dir = comtypes.client.gen_dir
try:
    comtypes.client.gen_dir = None
    msdia = comtypes.client.GetModule( msdia_path )
finally:
    comtypes.client.gen_dir = comtypes_client_gen_dir

#Adding code, that was not generated for some reason.

class UdtKind:
   UdtStruct, UdtClass, UdtUnion = (0, 1, 2)

class CV_access_e:
   CV_private, CV_protected, CV_public = (1, 2, 3)

msdia.UdtKind = UdtKind
msdia.CV_access_e = CV_access_e

class NameSearchOptions:
   nsNone               = 0
   nsfCaseSensitive     = 0x1
   nsfCaseInsensitive   = 0x2
   nsfFNameExt          = 0x4
   nsfRegularExpression = 0x8
   nsfUndecoratedName   = 0x10

   # For backward compabibility:
   nsCaseSensitive           = nsfCaseSensitive
   nsCaseInsensitive         = nsfCaseInsensitive
   nsFNameExt = nsfFNameExt
   nsRegularExpression       = nsfRegularExpression | nsfCaseSensitive
   nsCaseInRegularExpression = nsfRegularExpression | nsfCaseInsensitive

msdia.NameSearchOptions = NameSearchOptions
