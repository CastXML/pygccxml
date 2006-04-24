# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import os
import sys
import copy
import pickle
import unittest
import tempfile
import autoconfig
from pprint import pformat
from sets import Set as set

import time
import pygccxml
from pygccxml.utils import *
from pygccxml.parser import *
from pygccxml.declarations import *

start = time.clock()

wins = parse( [r"C:\Program Files\Microsoft Visual Studio .NET 2003\Vc7\PlatformSDK\Include\windows.h"] )

end = time.clock()

print 'parsing take ', end - start, ' seconds'

#wins = make_flatten( wins )
print 'len:', len(wins)
for decl in wins:
    print decl.__class__.__name__, decl.name
