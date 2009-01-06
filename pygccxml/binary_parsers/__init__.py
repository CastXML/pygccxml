# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import sys
import undname
from parsers import merge_information

def undecorate_blob( blob ):
    return undname.undname_creator_t().undecorate_blob( blob )
