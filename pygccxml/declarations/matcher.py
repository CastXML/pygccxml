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

"""implements few "find" algorithms on declarations tree"""

import types
from . import algorithm


class matcher:

    """class-namespace, contains implementation of few "find" algorithms and
    definition of related exception classes"""

    class declaration_not_found_t(RuntimeError):

        """exception, that will be raised, if the declaration could not be
        found"""

        def __init__(self, matcher):
            RuntimeError.__init__(self)
            self.matcher = matcher

        def __str__(self):
            return (
                "Unable to find declaration.  matcher: [%s]" % str(
                    self.matcher)
            )

    class multiple_declarations_found_t(RuntimeError):

        """exception, that will be raised, if more than one declaration was
        found"""

        def __init__(self, matcher):
            RuntimeError.__init__(self)
            self.matcher = matcher

        def __str__(self):
            return (
                "Multiple declarations has been found. matcher: [%s]" % str(
                    self.matcher)
            )

    @staticmethod
    def find(decl_matcher, decls, recursive=True):
        """
        returns a list of declarations that match `decl_matcher` defined
        criteria or None

        :param decl_matcher: Python callable object, that takes one argument -
        reference to a declaration
        :param decls: the search scope, :class:declaration_t object or
        :class:declaration_t objects list t
        :param recursive: boolean, if True, the method will run `decl_matcher`
        on the internal declarations too
        """

        where = []
        if isinstance(decls, list):
            where.extend(decls)
        else:
            where.append(decls)
        if recursive:
            where = algorithm.make_flatten(where)
        return list(filter(decl_matcher, where))

    @staticmethod
    def find_single(decl_matcher, decls, recursive=True):
        """
        returns a reference to the declaration, that match `decl_matcher`
        defined criteria.

        if a unique declaration could not be found the method will return None.

        :param decl_matcher: Python callable object, that takes one argument -
        reference to a declaration
        :param decls: the search scope, :class:declaration_t object or
        :class:declaration_t objects list t
        :param recursive: boolean, if True, the method will run `decl_matcher`
        on the internal declarations too
        """
        answer = matcher.find(decl_matcher, decls, recursive)
        if len(answer) == 1:
            return answer[0]

    @staticmethod
    def get_single(decl_matcher, decls, recursive=True):
        """
        returns a reference to declaration, that match `decl_matcher` defined
        criteria.

        If a unique declaration could not be found, an appropriate exception
        will be raised.

        :param decl_matcher: Python callable object, that takes one argument -
        reference to a declaration
        :param decls: the search scope, :class:declaration_t object or
        :class:declaration_t objects list t
        :param recursive: boolean, if True, the method will run `decl_matcher`
        on the internal declarations too
        """
        answer = matcher.find(decl_matcher, decls, recursive)
        if len(answer) == 1:
            return answer[0]
        elif len(answer) == 0:
            raise matcher.declaration_not_found_t(decl_matcher)
        else:
            raise matcher.multiple_declarations_found_t(decl_matcher)
