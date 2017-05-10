# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

from timeit import Timer

stmt = """
import unittest
from test_parser import create_suite
unittest.TextTestRunner(verbosity=2).run( create_suite() )
"""

timer = Timer(stmt)
print(timer.timeit(3))
