# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

"""
contains classes that allows to extract different information from binary files
( .pdb, .map, .dll, .bsc, .so ) and integrate it with existing declarations tree
"""

import undname
from parsers import merge_information

def undecorate_blob( blob ):
    """returns undecorated\unmangled string, created from blob"""
    return undname.undname_creator_t().undecorate_blob( blob )
