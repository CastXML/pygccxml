# =============================================================================
#
#  Copyright Insight Software Consortium
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0.txt
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
# =============================================================================

# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

"""
contains classes that allows to extract different information from binary files
( .map, .dll, .so ) and integrate it with existing declarations tree

The main function of this package is
:func:`pygccxml.binary_parsers.parsers.merge_information`.
"""

from .undname import undname_creator_t
from .parsers import merge_information


def undecorate_blob(blob):
    """Returns undecorated/unmangled string, created from
    blob(exported symbol name)
    """
    return undname_creator_t().undecorate_blob(blob)


def format_decl(decl, hint=None):
    """
    returns string, that represents formatted declaration, according to some
    rules
    :param hint: valid values are: "msvc" and "nm"
    """
    return undname_creator_t().format_decl(decl, hint=hint)
