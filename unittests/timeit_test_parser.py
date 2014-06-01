#! /usr/bin/python
# Copyright 2004-2013 Roman Yakovenko
# Copyright 2014 Insight Software Consortium
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

from timeit import Timer

stmt = """
import unittest
from test_parser import create_suite
unittest.TextTestRunner(verbosity=2).run( create_suite() )
"""

timer = Timer(stmt)
print(timer.timeit(3))
