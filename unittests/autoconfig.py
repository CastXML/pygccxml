# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import os
import sys

#__pychecker__ = 'limit=1000'
#import pychecker.checker

data_directory = ''
gccxml_path = ''
package_directory = ''

if sys.platform == 'linux2':
    gccxml_path = r'/home/roman/gccxml/bin'
elif sys.platform == 'win32':
    gccxml_path = r'C:\Tools\GCC_XML\bin\gccxml.exe'
else:
    raise RuntimeError( 'There is no configuration for "%s" platform.' % sys.platform )

try:
    import pygccxml
    print 'unittests will run on installed version'
    package_directory = os.path.split( pygccxml.__file__ )[0]
    data_directory = os.path.join( package_directory, 'unittests/data' )    
except ImportError:
    def pygccxml_location():
        global __name__
        location = os.path.split( os.path.realpath( __name__ ) )[0]
        location = os.path.normpath( os.path.join( location, '../..' ) )
        return location
    package_directory = pygccxml_location()
    data_directory = os.path.join( package_directory, 'pygccxml',  'unittests', 'data' )
    print 'unittests will run on development version'
    print '    package location: %s' % package_directory
    print '    data location   : %s' % data_directory
    sys.path.append( package_directory )
    sys.path.append( os.path.join(package_directory, 'pydsc' ) )

try:
    import pydsc
    #test only pygccxml
    pydsc.doc_checker.filter.append( package_directory )
    pydsc.doc_checker.filter_type = pydsc.FILTER_TYPE.INCLUDE
    #
    map( pydsc.doc_checker.speller.ignore_always
         , [ 'Yakovenko'
             , 'Bierbaum'
             , 'org'
             , 'http'
             , 'bool'
             , 'str'
             , 'www'
             , 'param' 
             , 'txt'
             , 'decl'
             , 'decls' 
             , 'namespace'
             , 'namespaces'
             , 'enum'
             , 'const'
             , 'GCC'
             , 'xcc'
             , 'TODO'
             , 'typedef'
             , 'os'
             , 'normcase'
             , 'normpath'
             , 'scopedef'
             , 'ira'#part of Matthias mail address
             , 'uka'#part of Matthias mail address
             , 'de'#part of Matthias mail address
             , 'dat'#file extension of directory cache
             , 'config'#parameter description
             , 'gccxml'#parameter description
             , 'pyplusplus'
             , 'pygccxml'
             , 'calldef'
             , 'XXX'
             , 'wstring'
             ] )
except ImportError:
    pass