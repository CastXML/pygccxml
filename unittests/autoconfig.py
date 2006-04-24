# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import os
import sys

#__pychecker__ = 'limit=1000'
#import pychecker.checker

gccxml_path = 'gccxml'
data_directory = os.path.abspath( os.path.join( os.curdir, 'data' ) )

try:
    import pygccxml
    print 'unittests will run on INSTALLED version'
    package_directory = os.path.split( pygccxml.__file__ )[0]   
except ImportError:
    sys.path.append( os.path.join( os.curdir, '..' ) )
    import pygccxml
    print 'unittests will run on DEVELOPMENT version'

#try:
    #import pydsc
    ##test only pygccxml
    #pydsc.doc_checker.filter.append( package_directory )
    #pydsc.doc_checker.filter_type = pydsc.FILTER_TYPE.INCLUDE
    ##
    #map( pydsc.doc_checker.speller.ignore_always
         #, [ 'Yakovenko'
             #, 'Bierbaum'
             #, 'org'
             #, 'http'
             #, 'bool'
             #, 'str'
             #, 'www'
             #, 'param' 
             #, 'txt'
             #, 'decl'
             #, 'decls' 
             #, 'namespace'
             #, 'namespaces'
             #, 'enum'
             #, 'const'
             #, 'GCC'
             #, 'xcc'
             #, 'TODO'
             #, 'typedef'
             #, 'os'
             #, 'normcase'
             #, 'normpath'
             #, 'scopedef'
             #, 'ira'#part of Matthias mail address
             #, 'uka'#part of Matthias mail address
             #, 'de'#part of Matthias mail address
             #, 'dat'#file extension of directory cache
             #, 'config'#parameter description
             #, 'gccxml'#parameter description
             #, 'pyplusplus'
             #, 'pygccxml'
             #, 'calldef'
             #, 'XXX'
             #, 'wstring'
             #] )
#except ImportError:
    #pass