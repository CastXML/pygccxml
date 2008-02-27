import os
import sys
import ctypes
import logging
import msvc_details
from ctypes import *
from ctypes.wintypes import ULONG
from ctypes.wintypes import DWORD
from ctypes.wintypes import BOOL
from ctypes.wintypes import BYTE
from ctypes.wintypes import WORD
from ctypes.wintypes import UINT

sys.path.append( r'../..' )

from pygccxml import utils
from pygccxml import declarations


STRING = c_char_p
_libraries = {}
_libraries['msvcr70.dll'] = CDLL(msvc_details.msvcr_path, mode=RTLD_GLOBAL)
_libraries['msbsc70.dll'] = CDLL(msvc_details.msbsc_path, mode=RTLD_GLOBAL)


qyMac = 9
refreshAllOp = 4
qyDervOf = 7
delOp = 1
qyImpMembers = 8
changeOp = 2
qyRefs = 4
qyCalls = 2
changeIinstOp = 3
qyContains = 1
qyCalledBy = 3
noOp = 5
qyBaseOf = 6
qyNil = 0
addOp = 0
qyDefs = 5
PULONG = POINTER(ULONG)
USHORT = c_ushort
PUSHORT = POINTER(USHORT)
UCHAR = c_ubyte
PUCHAR = POINTER(UCHAR)
PSZ = STRING
FLOAT = c_float
PFLOAT = POINTER(FLOAT)
PBOOL = POINTER(BOOL)
LPBOOL = POINTER(BOOL)
PBYTE = POINTER(BYTE)
LPBYTE = POINTER(BYTE)
PINT = POINTER(c_int)
LPINT = POINTER(c_int)
PWORD = POINTER(WORD)
LPWORD = POINTER(WORD)
LPLONG = POINTER(c_long)
PDWORD = POINTER(DWORD)
LPDWORD = POINTER(DWORD)
LPVOID = c_void_p
LPCVOID = c_void_p
INT = c_int
PUINT = POINTER(c_uint)
ULONG_PTR = POINTER(ULONG)
NI = ULONG
IINST = ULONG
IREF = ULONG
IDEF = ULONG
IMOD = USHORT
LINE = USHORT
TYP = BYTE
ATR = USHORT
ATR32 = ULONG
MBF = ULONG
SZ = STRING
SZ_CONST = STRING

class Bsc(Structure):
    pass

# values for enumeration 'OPERATION'
OPERATION = c_int # enum
class IinstInfo(Structure):
    pass
IinstInfo._fields_ = [
    ('m_iinst', IINST),
    ('m_szName', SZ_CONST),
    ('m_ni', NI),
]
class BSC_STAT(Structure):
    pass
BSC_STAT._fields_ = [
    ('cDef', ULONG),
    ('cRef', ULONG),
    ('cInst', ULONG),
    ('cMod', ULONG),
    ('cUseLink', ULONG),
    ('cBaseLink', ULONG),
]
class NiQ(Structure):
    pass
NiQ._fields_ = [
    ('m_iinstOld', IINST),
    ('m_iInfoNew', IinstInfo),
    ('m_op', OPERATION),
    ('m_typ', TYP),
]
pfnNotifyChange = CFUNCTYPE(BOOL, POINTER(NiQ), ULONG, ULONG_PTR)

# values for enumeration '_qy_'
_qy_ = c_int # enum
QY = _qy_
Bsc._fields_ = [
]
BSCOpen = _libraries['msbsc70.dll'].BSCOpen
BSCOpen.restype = BOOL
BSCOpen.argtypes = [SZ_CONST, POINTER(POINTER(Bsc))]
BSCClose = _libraries['msbsc70.dll'].BSCClose
BSCClose.restype = BOOL
BSCClose.argtypes = [POINTER(Bsc)]
BSCIinstInfo = _libraries['msbsc70.dll'].BSCIinstInfo
BSCIinstInfo.restype = BOOL
BSCIinstInfo.argtypes = [POINTER(Bsc), IINST, POINTER(SZ), POINTER(TYP), POINTER(ATR)]
BSCIrefInfo = _libraries['msbsc70.dll'].BSCIrefInfo
BSCIrefInfo.restype = BOOL
BSCIrefInfo.argtypes = [POINTER(Bsc), IREF, POINTER(SZ), POINTER(LINE)]
BSCIdefInfo = _libraries['msbsc70.dll'].BSCIdefInfo
BSCIdefInfo.restype = BOOL
BSCIdefInfo.argtypes = [POINTER(Bsc), IDEF, POINTER(SZ), POINTER(LINE)]
BSCImodInfo = _libraries['msbsc70.dll'].BSCImodInfo
BSCImodInfo.restype = BOOL
BSCImodInfo.argtypes = [POINTER(Bsc), IMOD, POINTER(SZ)]
BSCSzFrTyp = _libraries['msbsc70.dll'].BSCSzFrTyp
BSCSzFrTyp.restype = SZ
BSCSzFrTyp.argtypes = [POINTER(Bsc), TYP]
BSCSzFrAtr = _libraries['msbsc70.dll'].BSCSzFrAtr
BSCSzFrAtr.restype = SZ
BSCSzFrAtr.argtypes = [POINTER(Bsc), ATR]
BSCGetIinstByvalue = _libraries['msbsc70.dll'].BSCGetIinstByvalue
BSCGetIinstByvalue.restype = BOOL
BSCGetIinstByvalue.argtypes = [POINTER(Bsc), SZ, TYP, ATR, POINTER(IINST)]
BSCGetOverloadArray = _libraries['msbsc70.dll'].BSCGetOverloadArray
BSCGetOverloadArray.restype = BOOL
BSCGetOverloadArray.argtypes = [POINTER(Bsc), SZ, MBF, POINTER(POINTER(IINST)), POINTER(ULONG)]
BSCGetUsedByArray = _libraries['msbsc70.dll'].BSCGetUsedByArray
BSCGetUsedByArray.restype = BOOL
BSCGetUsedByArray.argtypes = [POINTER(Bsc), IINST, MBF, POINTER(POINTER(IINST)), POINTER(ULONG)]
BSCGetUsesArray = _libraries['msbsc70.dll'].BSCGetUsesArray
BSCGetUsesArray.restype = BOOL
BSCGetUsesArray.argtypes = [POINTER(Bsc), IINST, MBF, POINTER(POINTER(IINST)), POINTER(ULONG)]
BSCGetBaseArray = _libraries['msbsc70.dll'].BSCGetBaseArray
BSCGetBaseArray.restype = BOOL
BSCGetBaseArray.argtypes = [POINTER(Bsc), IINST, POINTER(POINTER(IINST)), POINTER(ULONG)]
BSCGetDervArray = _libraries['msbsc70.dll'].BSCGetDervArray
BSCGetDervArray.restype = BOOL
BSCGetDervArray.argtypes = [POINTER(Bsc), IINST, POINTER(POINTER(IINST)), POINTER(ULONG)]
BSCGetMembersArray = _libraries['msbsc70.dll'].BSCGetMembersArray
BSCGetMembersArray.restype = BOOL
BSCGetMembersArray.argtypes = [POINTER(Bsc), IINST, MBF, POINTER(POINTER(IINST)), POINTER(ULONG)]
BSCGetDefArray = _libraries['msbsc70.dll'].BSCGetDefArray
BSCGetDefArray.restype = BOOL
BSCGetDefArray.argtypes = [POINTER(Bsc), IINST, POINTER(POINTER(IREF)), POINTER(ULONG)]
BSCGetRefArray = _libraries['msbsc70.dll'].BSCGetRefArray
BSCGetRefArray.restype = BOOL
BSCGetRefArray.argtypes = [POINTER(Bsc), IINST, POINTER(POINTER(IREF)), POINTER(ULONG)]
BSCGetModuleContents = _libraries['msbsc70.dll'].BSCGetModuleContents
BSCGetModuleContents.restype = BOOL
BSCGetModuleContents.argtypes = [POINTER(Bsc), IMOD, MBF, POINTER(POINTER(IINST)), POINTER(ULONG)]
BSCGetModuleByName = _libraries['msbsc70.dll'].BSCGetModuleByName
BSCGetModuleByName.restype = BOOL
BSCGetModuleByName.argtypes = [POINTER(Bsc), SZ, POINTER(IMOD)]
BSCGetAllModulesArray = _libraries['msbsc70.dll'].BSCGetAllModulesArray
BSCGetAllModulesArray.restype = BOOL
BSCGetAllModulesArray.argtypes = [POINTER(Bsc), POINTER(POINTER(IMOD)), POINTER(ULONG)]
BSCDisposeArray = _libraries['msbsc70.dll'].BSCDisposeArray
BSCDisposeArray.restype = None
BSCDisposeArray.argtypes = [POINTER(Bsc), c_void_p]
BSCFormatDname = _libraries['msbsc70.dll'].BSCFormatDname
BSCFormatDname.restype = SZ
BSCFormatDname.argtypes = [POINTER(Bsc), SZ]
BSCFInstFilter = _libraries['msbsc70.dll'].BSCFInstFilter
BSCFInstFilter.restype = BOOL
BSCFInstFilter.argtypes = [POINTER(Bsc), IINST, MBF]
BSCIinstFrIref = _libraries['msbsc70.dll'].BSCIinstFrIref
BSCIinstFrIref.restype = IINST
BSCIinstFrIref.argtypes = [POINTER(Bsc), IREF]
BSCIinstFrIdef = _libraries['msbsc70.dll'].BSCIinstFrIdef
BSCIinstFrIdef.restype = IINST
BSCIinstFrIdef.argtypes = [POINTER(Bsc), IDEF]
BSCIinstContextIref = _libraries['msbsc70.dll'].BSCIinstContextIref
BSCIinstContextIref.restype = IINST
BSCIinstContextIref.argtypes = [POINTER(Bsc), IREF]
BSCGetStatistics = _libraries['msbsc70.dll'].BSCGetStatistics
BSCGetStatistics.restype = BOOL
BSCGetStatistics.argtypes = [POINTER(Bsc), POINTER(BSC_STAT)]
BSCGetModuleStatistics = _libraries['msbsc70.dll'].BSCGetModuleStatistics
BSCGetModuleStatistics.restype = BOOL
BSCGetModuleStatistics.argtypes = [POINTER(Bsc), IMOD, POINTER(BSC_STAT)]
BSCFCaseSensitive = _libraries['msbsc70.dll'].BSCFCaseSensitive
BSCFCaseSensitive.restype = BOOL
BSCFCaseSensitive.argtypes = [POINTER(Bsc)]
BSCSetCaseSensitivity = _libraries['msbsc70.dll'].BSCSetCaseSensitivity
BSCSetCaseSensitivity.restype = BOOL
BSCSetCaseSensitivity.argtypes = [POINTER(Bsc), BOOL]
BSCGetAllGlobalsArray = _libraries['msbsc70.dll'].BSCGetAllGlobalsArray
BSCGetAllGlobalsArray.restype = BOOL
BSCGetAllGlobalsArray.argtypes = [POINTER(Bsc), MBF, POINTER(POINTER(IINST)), POINTER(ULONG)]
BSCSzFrAtr2 = _libraries['msbsc70.dll'].BSCSzFrAtr2
BSCSzFrAtr2.restype = SZ
BSCSzFrAtr2.argtypes = [POINTER(Bsc), ATR32]
BSCIinstInfo2 = _libraries['msbsc70.dll'].BSCIinstInfo2
BSCIinstInfo2.restype = BOOL
BSCIinstInfo2.argtypes = [POINTER(Bsc), IINST, POINTER(SZ), POINTER(TYP), POINTER(ATR32)]
BSCGetIinstByvalue2 = _libraries['msbsc70.dll'].BSCGetIinstByvalue2
BSCGetIinstByvalue2.restype = BOOL
BSCGetIinstByvalue2.argtypes = [POINTER(Bsc), SZ, TYP, ATR32, POINTER(IINST)]
OpenBSCQuery = _libraries['msbsc70.dll'].OpenBSCQuery
OpenBSCQuery.restype = BOOL
OpenBSCQuery.argtypes = [POINTER(Bsc)]
CloseBSCQuery = _libraries['msbsc70.dll'].CloseBSCQuery
CloseBSCQuery.restype = BOOL
CloseBSCQuery.argtypes = []
BOB = ULONG
InitBSCQuery = _libraries['msbsc70.dll'].InitBSCQuery
InitBSCQuery.restype = BOOL
InitBSCQuery.argtypes = [QY, BOB]
BobNext = _libraries['msbsc70.dll'].BobNext
BobNext.restype = BOB
BobNext.argtypes = []
BobFrName = _libraries['msbsc70.dll'].BobFrName
BobFrName.restype = BOB
BobFrName.argtypes = [SZ]
LszNameFrBob = _libraries['msbsc70.dll'].LszNameFrBob
LszNameFrBob.restype = SZ
LszNameFrBob.argtypes = [BOB]
CLS = USHORT

class MBF:
    mbfNil       = 0x000
    mbfVars      = 0x001
    mbfFuncs     = 0x002
    mbfMacros    = 0x004
    mbfTypes     = 0x008
    mbfClass     = 0x010
    mbfIncl      = 0x020
    mbfMsgMap    = 0x040
    mbfDialogID  = 0x080
    mbfLibrary   = 0x100
    mbfImport    = 0x200
    mbfTemplate  = 0x400
    mbfNamespace = 0x800
    mbfAll       = 0xFFF

class bsc_reader_t( object ):
    def __init__( self, bsc_file ):
        self.logger = utils.loggers.pdb_reader
        self.logger.setLevel(logging.DEBUG)

        self.__bsc_file = bsc_file   
        self.__bsc = pointer( Bsc() )
        self.logger.debug( 'openning bsc file "%s"', self.__bsc_file )
        if not BSCOpen( self.__bsc_file, byref( self.__bsc ) ):
            self.logger.debug( 'unable to open bsc file "%s"', self.__bsc_file )
            raise RuntimeError( "Unable to open bsc file '%s'" % self.__bsc_file )
        self.logger.debug( 'openning bsc file "%s" - done', self.__bsc_file )
        
        self.__instances = []

    def query_all_instances( self ):
        instances_len = ULONG(0)        
        instances = pointer( IINST() )

        self.logger.debug( 'call BSCGetAllGlobalsArray function' )        
        if not BSCGetAllGlobalsArray( self.__bsc, MBF.mbfAll, byref( instances ), byref( instances_len ) ):
            self.logger.debug( 'call BSCGetAllGlobalsArray function - failure' )
            raise RuntimeError( "Unable to load all globals symbols" )
        self.logger.debug( 'call BSCGetAllGlobalsArray function - success' )            
        self.logger.debug( 'instances_len: %d', instances_len.value )
        for i in range( instances_len.value ):
            print i
            self.__instances.append( i )        
        
    def print_stat( self ):
        stat = BSC_STAT()
        BSCGetStatistics( self.__bsc, byref( stat ) )
        for f, t in stat._fields_:
            print '%s: %s' % ( f, str( getattr( stat, f) ) )
    
    def __del__( self ):
        BSCClose( self.__bsc )




if __name__ == '__main__':
    #for i in range( 1000 ):
    control_bsc = r'xxx.bsc'
    reader = bsc_reader_t( control_bsc )
    reader.print_stat()
    reader.query_all_instances()
        
        
