# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import os
import sys
import logging
import tempfile

    
logger = logging.getLogger('pygccxml')
__handler = logging.StreamHandler(sys.stdout)
__handler.setFormatter( logging.Formatter('%(message)s') )
logger.addHandler(__handler) 
logger.setLevel(logging.DEBUG)

def remove_file_no_raise(file_name ):
    try:
        if os.path.exists(file_name):
            os.remove( file_name )
    except Exception, error:
        logger.error( "Error ocured while removing temprorary created file('%s'): %s" 
                      % ( file_name, str( error ) ) )

def create_temp_file_name(suffix, prefix=None, dir=None):    
    if not prefix:
        prefix = tempfile.template
    fd, name = tempfile.mkstemp( suffix=suffix, prefix=prefix, dir=dir )
    file_obj = os.fdopen( fd )
    file_obj.close()
    return name

def normalize_path( some_path ):
    return os.path.normpath( os.path.normcase( some_path ) )
