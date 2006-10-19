import sys

#Directory path, in which you want to install GCC-XML.
#If directory does not exist, it will be created
destination_dir = None

class vc6:
    install_dir = None

class vc7:
    install_dir = None

class vc71:
    install_dir = None
    
class borland55:
    install_dir = None
    
class gcc:
    install_dir = None
    


compilers = []
if 'linux' in sys.platform:
    compilers.append( gcc )
else 'win' in sys.platform:
    compilers.extend( [ vc6, vc7, vc71, borland55 ] )
