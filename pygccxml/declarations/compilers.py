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
contains enumeration of all compilers supported by the project
"""

GCC_XML_06 = "GCC-XML 0.6"
GCC_XML_07 = "GCC-XML 0.7"
GCC_XML_09 = "GCC-XML 0.9"
GCC_XML_09_BUGGY = "GCC-XML 0.9 BUGGY"
# revision 122:
# After this fix, all constructors and destructors that exist for a class
# are dumped whether the user declared them or not.  Those that were
# implicitly declared by the compiler are marked as "artificial".


def on_missing_functionality(compiler, functionality):
    raise NotImplementedError(
        '"%s" compiler doesn\'t support functionality "%s"' %
        (compiler, functionality))
