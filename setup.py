#!/usr/bin/env python
# Copyright 2004-2013 Roman Yakovenko
# Copyright 2014 Insight Software Consortium
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

from distutils.core import setup

setup(name="pygccxml",
      version="v1.5.2",
      description="GCC-XML generated file reader",
      author="GCC-XML maintainers",
      author_email="gccxml@gccxml.org",
      packages=['pygccxml',
                'pygccxml.declarations',
                'pygccxml.parser',
                'pygccxml.binary_parsers',
                'pygccxml.utils']
      )
