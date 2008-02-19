import getpass
import comtypes
import comtypes.client

msdia_path = None
if 'root' == getpass.getuser():
    msdia_path = r'C:\Program Files\Microsoft Visual Studio 9.0\Common7\Packages\Debugger\msdia90.dll'

msdia = comtypes.client.GetModule( msdia_path )

class UdtKind:
   UdtStruct, UdtClass, UdtUnion = ( 0, 1, 2 )

msdia.UdtKind = UdtKind

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


#
#from distutils import ccompiler
#from distutils import msvccompiler
#
#if 'msvc' == ccompiler.get_default_compiler():
#    cc = msvccompiler.MSVCCompiler()
#    cc.initialize()
#    generator = 'NMake Makefiles'
#    native_build = '"%s" /A all' % cc.find_exe( 'nmake.exe' )
#    configure_environment_script = cc.find_exe( 'vsvars32.bat' )
#    if not configure_environment_script:
#        configure_environment_script = cc.find_exe( 'vcvars32.bat' )
#    cl_mapping = { 6.0 : "msvc6", 7.0 : "msvc7", 7.1 : "msvc71", 8.0 : "msvc8" }
#    compiler = cl_mapping[ msvccompiler.get_build_version() ]
#else:
#    raise RuntimeError( "Unable to find out MSDIA dll location")
