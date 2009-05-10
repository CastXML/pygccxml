#!/usr/bin/env python
# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

from distutils.core import setup

setup( name = "pygccxml",
       version = "1.1.0",
       description = "GCC-XML generated file reader",
       author = "Roman Yakovenko",
       author_email = "roman.yakovenko@gmail.com",
       url = 'http://www.language-binding.net/pygccxml/pygccxml.html',
       packages = [ 'pygccxml',
                    'pygccxml.declarations',
                    'pygccxml.parser',
                    'pygccxml.binary_parsers',
                    'pygccxml.utils' ]
)
