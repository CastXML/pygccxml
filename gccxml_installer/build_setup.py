import os
import sys

class settings:
    gccxml_cvs_dir = ""
    gccxml_bin_dir = ""    
    destination_dir = ""
    gccxml_version = "0.7"
    
#Deploy layout:
#root
#  / bin
#    - gccxml.exe
#    - gccxml_cc1plus.exe
#    - gccxml_vcupdate.bat
#  / doc
#    - Copyright.txt
#    - gccxml.html
#    - gccxml.txt
#  / share
#   / gccxml + version
#     - gccxml_config # contains gccxml compiler
#     / Borland
#       * contains patches relevant for Borland compiler
#       * "as is" copy of directory from cvs layout
#     / Vc6
#     / Vc7
#     / Vc71
#       * contains patches relevant for Vc6 compiler
#       * Patches created by running vcInstall + vcPatch programs from /VcInstall
#       * directory
#  /VcInstall
#   * I am not sure whether this directory should be installed or not

def makedirs( path ):
    if not os.path.exists( path ):
        os.makedirs( path )
    return path

bin_dir_dest = makedirs( os.path.join( settings.destination_dir, 'bin' ) )
bin_dir_source = settings.gccxml_bin_dir
if sys.platform

