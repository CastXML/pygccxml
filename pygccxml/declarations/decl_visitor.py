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
defines declarations visitor class interface
"""


class decl_visitor_t(object):

    """
    declarations visitor interface

    All functions within this class should be redefined in derived classes.
    """

    def __init__(self):
        object.__init__(self)

    def visit_member_function(self):
        raise NotImplementedError()

    def visit_constructor(self):
        raise NotImplementedError()

    def visit_destructor(self):
        raise NotImplementedError()

    def visit_member_operator(self):
        raise NotImplementedError()

    def visit_casting_operator(self):
        raise NotImplementedError()

    def visit_free_function(self):
        raise NotImplementedError()

    def visit_free_operator(self):
        raise NotImplementedError()

    def visit_class_declaration(self):
        raise NotImplementedError()

    def visit_class(self):
        raise NotImplementedError()

    def visit_enumeration(self):
        raise NotImplementedError()

    def visit_namespace(self):
        raise NotImplementedError()

    def visit_typedef(self):
        raise NotImplementedError()

    def visit_variable(self):
        raise NotImplementedError()
