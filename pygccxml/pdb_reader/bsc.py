import os
import sys
import ctypes
import msvc_details

bsc = ctypes.cdll.LoadLibrary(  msvc_details.msbsc_path )

class bsc_t( object ):
    def __init__( self, bsc_file_path ):
        self.__bsc_file = bsc_file_path