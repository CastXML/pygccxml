import os
import sys
import comtypes
import comtypes.client
from sets import Set as set

comtypes.client.gen_dir = r'D:\dev\language-binding\sources\pygccxml_dev\pygccxml\parser\gen'
print comtypes.client.GetModule( r'D:\Program Files\Microsoft Visual Studio .NET 2003\Visual Studio SDKs\DIA SDK\bin\msdia71.dll' )

#~ MODULE_IDENTIFIER = ('{106173A0-0173-4e5c-84E7-E915422BE997}', 0, 2, 0)
#~ MODULE_PATH = r'Lib\site-packages\win32com\gen_py\106173A0-0173-4e5c-84E7-E915422BE997x0x2x0.py'

#~ try:
    #~ full_module_path = os.path.split( sys.executable )[0]
    #~ full_module_path = os.path.join( full_module_path, MODULE_PATH )
    #~ if os.path.exists( full_module_path ):
        #~ os.remove( full_module_path )
        #~ print(full_module_path, " removed successfully")
#~ except Exception, error:
    #~ print 'Exception:',  str(error)

#~ msdia = win32com.client.gencache.EnsureModule( *MODULE_IDENTIFIER )

#ds = comtypes.client.CreateObject( "{e60afbee-502d-46ae-858f-8272a09bd707}" )
#print dir( ds )
#ds.loadDataFromPdb( 'xxx.pdb' )

#~ ds = msdia.DiaSource()
#~ ds.loadDataFromPdb( 'xxx.pdb' )
#~ session = ds.openSession()
#~ print 'done'
