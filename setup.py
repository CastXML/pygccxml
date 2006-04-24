# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import os
from distutils import sysconfig
from distutils.core import setup

setup( name="pygccxml"
       , description="GCC-XML generated file reader"
       , author="Roman Yakovenko"
       , packages=[ 'pygccxml'
                    , 'pygccxml.declarations'
                    , 'pygccxml.parser'
                    , 'pygccxml.utils' ]
)
