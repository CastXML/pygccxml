# =============================================================================
#
#  Copyright 2014 Insight Software Consortium
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

# Copyright 2004-2013 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

"""
template instantiation parser

This module provides functionality necessary to

* :func:`parse <pygccxml.declarations.templates.parse>`
* :func:`split <pygccxml.declarations.templates.split>`
* :func:`join <pygccxml.declarations.templates.join>`
* :func:`normalize <pygccxml.declarations.templates.normalize>`

C++ template instantiations
"""

from . import pattern_parser

__THE_PARSER = pattern_parser.parser_t('<', '>', ',')


def is_instantiation(decl_string):
    """
    returns True if `decl_string` is template instantiation and False otherwise

    :param decl_string: string that should be checked for pattern presence
    :type decl_string: str

    :rtype: bool
    """
    global __THE_PARSER
    return __THE_PARSER.has_pattern(decl_string)


def name(decl_string):
    """
    returns name of instantiated template

    :type decl_string: str
    :rtype: str
    """
    global __THE_PARSER
    return __THE_PARSER.name(decl_string)


def args(decl_string):
    """
    returns list of template arguments

    :type decl_string: `str`
    :rtype: [`str`]
    """
    global __THE_PARSER
    return __THE_PARSER.args(decl_string)


def split(decl_string):
    """returns (name, [arguments] )"""
    global __THE_PARSER
    return __THE_PARSER.split(decl_string)


def split_recursive(decl_string):
    """returns [(name, [arguments])]"""
    global __THE_PARSER
    return __THE_PARSER.split_recursive(decl_string)


def join(name, args):
    """returns name< argument_1, argument_2, ..., argument_n >"""
    global __THE_PARSER
    return __THE_PARSER.join(name, args)


def normalize(decl_string):
    """returns `decl_string`, which contains "normalized" spaces

    this functionality allows to implement comparison of 2 different string
    which are actually same: x::y< z > and x::y<z>
    """
    global __THE_PARSER
    return __THE_PARSER.normalize(decl_string)
