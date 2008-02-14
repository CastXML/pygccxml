import os
import sys
import ctypes
import comtypes
import comtypes.client
from sets import Set as set

msdia_dll = r'C:\Program Files\Microsoft Visual Studio .NET 2003\Visual Studio SDKs\DIA SDK\bin\msdia71.dll'
msdia_dll = r'D:\Program Files\Microsoft Visual Studio .NET 2003\Visual Studio SDKs\DIA SDK\bin\msdia71.dll'

msdia_dll = 'msdia80.dll'

msdia = comtypes.client.GetModule( msdia_dll )

control_pdb = r'C:\dev\produce_pdb\Debug\produce_pdb.pdb' 
control_pdb = r'xxx.pdb' 

ds = comtypes.client.CreateObject( msdia.DiaSource )
ds.loadDataFromPdb(control_pdb)
session = ds.openSession()

root_symbol = session.globalScope

print root_symbol

SymTagEnum = 12

def AsDiaSymbol( x ):
    return ctypes.cast( x, ctypes.POINTER( msdia.IDiaSymbol ) )

def print_enums( smb ):
    enums = smb.findChildren( SymTagEnum, None, 0 )
    for enum in iter( enums ):
        enum = AsDiaSymbol( enum )      
        if 'shared_consts' not in enum.name:
            continue                        
        print 'name: ', enum.name
        if enum.container:
            print 'container: ', enum.container.name
        if enum.classParent:            
            print 'parent: ', enum.classParent.name
        if enum.lexicalParent:
            print 'lexical parent: ', enum.lexicalParent.Name
        #~ print 'enum: ', enum.symIndexId
        #~ f = session.findFile( internal_smb, internal_smb.name, 0 )
        #~ print 'name: ', internal_smb.name
        #~ print f
        
        values = enum.findChildren( msdia.SymTagData, None, 0 ) 
        for v in iter(values):            
            v = AsDiaSymbol(v)
            if v.classParent.symIndexId !=  enum.symIndexId:
                continue
            print '  value %s(%d): ' % ( v.name, v.value )

def print_nss( smb, offset ):
    symbols = smb.findChildren( msdia.SymTagUDT, None, 0 )
    for internal_smb in iter( symbols ):
        internal_smb = ctypes.cast( internal_smb, ctypes.POINTER( msdia.IDiaSymbol ) )
        if internal_smb.classParentId == smb.symIndexId:
            print ' ' * offset, internal_smb.name
            print_nss( internal_smb, offset + 1 )

def print_files( session ):
    files = iter( session.findFile( None, '', 0 ) )
    for f in files:
        f = ctypes.cast( f, ctypes.POINTER(msdia.IDiaSourceFile) )
        print 'File: ', f.fileName

#~ print_files( session )
print_enums( root_symbol )
